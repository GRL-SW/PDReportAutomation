import Globals
from bs4 import BeautifulSoup
from datetime import datetime
import ValueScripts.HtmlCommonlib as HtmlCommonLib

def set_info(lines):
    h4_dict = {}
    h6_dict = {}
    table_dict = {}
    h4_lines = []
    h6_lines = []
    table_lines = []
    for i,line in enumerate(lines):
        if "<h4>" in str(line):
            if str(line) not in h4_dict.keys():
                h4_dict[str(line)] = []
                
            h4_dict[str(line)].append(i)
            h4_lines.append(i)

        if "<h6>" in str(line):
            if str(line) not in h6_dict.keys():
                h6_dict[str(line)] = []
                
            h6_dict[str(line)].append(i)
            h6_lines.append(i)

        if "<table id=\"t02\">" in str(line):
            if str(line) not in table_dict.keys():
                table_dict[str(line)] = []
                
            table_dict[str(line)].append(i)
            table_lines.append(i)

    # # print("-------H4-------")
    # for text in h4_dict:
    #     # print(text,":",h4_dict[text])
    # # print("-------H6-------")
    # for text in h6_dict:
    #     # print(text,":",h6_dict[text])
    # # print("------TABLE------")
    # for text in table_dict:
    #     # print(text,":",table_dict[text])

    return h4_dict,h6_dict,table_dict,h4_lines,h6_lines,table_lines

def get_target_lines(data,h4_dict,h4_lines,table_lines):
    keyword_line_list = []
    result_line_list = []
    table_line_list = []
    key_idx = []
    for h4 in h4_dict:
        h4_text = (h4.split(" "))[0]
        # print(h4_text)
        if data[2] == h4_text.replace("b'<h4>",""):
            # # print(h4)
            keyword_line = h4_dict[h4]
            
            if len(keyword_line) == 1:
                key_idx = []
                keyword_line_list.append(keyword_line[0])

                for idx,hl in enumerate(h4_lines):
                    if keyword_line[0] == hl:
                        key_idx.append(idx)
                        if hl != h4_lines[len(h4_lines)-1]:
                            key_idx.append(idx+1)
                        else:
                            key_idx.append(idx)

                # # print("key_idx:",key_idx)
                # # print(h4_lines[key_idx[0]],":",h4_lines[key_idx[1]])

                result_line_list.append(keyword_line[0]+1)

                for t_idx ,tl in enumerate(table_lines):
                    if tl >= h4_lines[key_idx[0]]+2 and tl <= h4_lines[key_idx[1]]:
                        table_line_list.append(t_idx)

    # # print(table_line_list)


    return keyword_line_list,result_line_list,table_line_list

def get_result_tmp(h6_dict,keyword_line_list,result_line_list):
    result_list = []
    if len(keyword_line_list) != 0 and len(result_line_list) != 0:
        for h6 in h6_dict:
            for rll in result_line_list:
                if rll in h6_dict[h6]:
                    if "PASS" in h6:
                        result_list.append("PASS")
                    elif "FAIL" in h6:
                        result_list.append("FAIL")
                    elif "NOT COMPLETE" in h6:
                        result_list.append("FAIL")

    return result_list

def get_result_list(data,file_list):
    result_list = []
    set_result = False

    for file in file_list:
        print(file)
        set_result = False
        
        with open(file, 'rb') as f:
            lines = f.readlines()

        h4_dict,h6_dict,table_dict,h4_lines,h6_lines,table_lines = set_info(lines)

        keyword_line_list,result_line_list,table_line_list = get_target_lines(data,h4_dict,h4_lines,table_lines)
        # # print(keyword_line_list,":",result_line_list)
        result_list_tmp = get_result_tmp(h6_dict,keyword_line_list,result_line_list)
        # print("result_tmp",result_list_tmp)
        for rlt in result_list_tmp:
            if "FAIL" == rlt:
                result_list.append("FAIL")
                set_result = True
                break
        if set_result == False and len(result_list_tmp) != 0:
            result_list.append("PASS")
        elif len(result_list_tmp) == 0:
            result_list.append("NA")

    return result_list

def get_result(data,file_list):

    result_list = get_result_list(data,file_list)

    print(result_list)
    
    if "COMMON." in data[2]:
        if "FAIL" in result_list:
            Globals.RESULT_DATA[str(data[0])] = "FAIL"
        elif "FAIL" not in result_list and "PASS" not in result_list:
            Globals.RESULT_DATA[str(data[0])] = "PASS"
        else:
            return 
    else:
        if "PASS" in result_list:
            Globals.RESULT_DATA[str(data[0])] = "PASS"
        if "FAIL" in result_list and "PASS" not in result_list:
            Globals.RESULT_DATA[str(data[0])] = "FAIL"
        else:
            return 

def get_comment(data,file_list,soup_list):
    
    comments_list = []
    comments = ""
    current_port = ""

    result_list = get_result_list(data,file_list)
    print(result_list)
    
    fail_comment_idx = HtmlCommonLib.set_fail_idx(data,result_list)

    print(fail_comment_idx)

    if len(fail_comment_idx) == 0:
        Globals.RESULT_DATA[str(data[0])] = ""
        return

    current_port = ""

    for fci in fail_comment_idx:
        comments_list = []
    
        with open(Globals.DATA_FILE[fci], 'rb') as f:
            lines = f.readlines()        
        h4_dict,h6_dict,table_dict,h4_lines,h6_lines,table_lines = set_info(lines)

        # # print(table_lines)

        keyword_line_list,result_line_list,table_list = get_target_lines(data,h4_dict,h4_lines,table_lines)
        
        tables = soup_list[fci].find_all('table',{'id':'t02'})
        print(table_list)
        string_list = []
        for t in table_list:
            tr_list = tables[t].find_all('tr')
            for tr in tr_list:
                if "FAIL" in tr.text or "NOT COMPLETE" in tr.text:
                    # text_list = tr.text.replace('\n',",")
                    # # print(text_list)

                    text_list = tr.text.split('\n')
                    # print(text_list)

                    for text in text_list:
                        if  text != "" and text != "FAIL" and text != "NOT COMPLETE" and text != "Detailed report":
                            print(text)
                            string_list.append(text)
        
        string_list = list(set(string_list))
        # for string in string_list:
            # print(string)
        if '\n'.join(string_list) not in comments_list:
            comments_list.append('\n'.join(string_list))
        print("comment list:",comments_list)
            
        if "2 Port" in Globals.CURRENT_TABLE and len(comments_list)!=0:
            path_list = Globals.DATA_FILE[fci].split("\\")
            port_name = path_list[len(path_list)-3]
            if current_port != port_name:
                # # print(current_port,":",port_name)
                port_dic = {"PA":"Port 1","PB":"Port 2"}
                current_port = port_name
                
                
                if comments == "":
                    comments = 'MQP:\n('+ port_dic[current_port] + '):\n'+'\n'.join(comments_list)
                else:
                    comments = comments+'\n' +"("+ port_dic[current_port] + '):\n'+'\n'.join(comments_list)

            else:
                if comments == "":
                    comments = 'MQP:\n'+'\n'.join(comments_list)
                else:
                    comments = comments +'\n'.join(comments_list)

        elif len(comments_list)!=0:
            if comments == "":
                    comments = 'MQP:\n'.join(comments_list)
            else:
                comments = comments + '\n' + '\n'.join(comments_list)


    print("*************************************************************************")
    print(comments)

    if comments != "":
        Globals.RESULT_DATA[str(data[0])] = comments

    elif Globals.RESULT_DATA[str(data[0])] == "PASS":
        Globals.RESULT_DATA[str(data[0])] = ""
    else:
        Globals.RESULT_DATA[str(data[0])] = ""
    
def get_value(data,file_list,soup_list):
    if "Comment" in Globals.CURRENT_TABLE:
        get_comment(data,file_list,soup_list)
    else:
        get_result(data,file_list)
    
    return True
