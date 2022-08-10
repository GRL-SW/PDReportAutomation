# import Globals
from bs4 import BeautifulSoup
from datetime import datetime

from matplotlib.pyplot import table
import Globals

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
        if data[2] in h4:
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

def get_result_list(h6_dict,keyword_line_list,result_line_list):
    result_list = []
    if len(keyword_line_list) != 0 and len(result_line_list) != 0:
        for h6 in h6_dict:
            for rll in result_line_list:
                if rll in h6_dict[h6]:
                    if "PASS" in h6:
                        result_list.append("PASS")
                    if "FAIL" in h6:
                        result_list.append("FAIL")

    return result_list

def get_result(data,file_list):

    result_list = []
    set_result = False

    for file in file_list:
        # print(file)
        set_result = False
        
        with open(file, 'rb') as f:
            lines = f.readlines()

        h4_dict,h6_dict,table_dict,h4_lines,h6_lines,table_lines = set_info(lines)

        keyword_line_list,result_line_list,table_line_list = get_target_lines(data,h4_dict,h4_lines,table_lines)
        # # print(keyword_line_list,":",result_line_list)
        result_list_tmp = get_result_list(h6_dict,keyword_line_list,result_line_list)
        
        for rlt in result_list_tmp:
            if "FAIL" == rlt:
                result_list.append("FAIL")
                set_result = True
                break
        if set_result == False:
            result_list.append("PASS")

    if "PASS" in result_list:
        Globals.RESULT_DATA[str(data[0])] = "PASS"
    if len(result_list) != 0 and "PASS" not in result_list:
        Globals.RESULT_DATA[str(data[0])] = "FAIL"
    else:
        return 

def get_comment(data,file_list,soup_list):
    
    comments_list = []
    comments = ""
    current_port = ""

    if Globals.RESULT_DATA[str(data[0])] == "FAIL":
        for idx,file in enumerate(file_list):
            # # print(file)
        
            with open(file, 'rb') as f:
                lines = f.readlines()

            h4_dict,h6_dict,table_dict,h4_lines,h6_lines,table_lines = set_info(lines)

            # # print(table_lines)

            keyword_line_list,result_line_list,table_list = get_target_lines(data,h4_dict,h4_lines,table_lines)
            
            tables = soup_list[idx].find_all("table")

            
            for t in tables:
                tr_list = t.find_all('tr')
                for tr in tr_list:
                    if "FAIL" in tr.text:
                        # text_list = tr.text.replace('\n',",")
                        # # print(text_list)

                        text_list = tr.text.split('\n')

                        string = ""

                        for text in text_list:
                            if text != "" and text != "FAIL":
                                string = string + text + " "
                        if string not in comments_list:
                            comments_list.append(string)
            if "2 Port" in Globals.CURRENT_TABLE:
                path_list = file.split("\\")
                port_name = path_list[len(path_list)-3]
                if current_port != port_name:
                    # # print(current_port,":",port_name)
                    current_port = port_name
                    
                    
                    if comments == "":
                        comments = 'MQP:\n('+current_port + '):\n'+'\n'.join(comments_list)
                    else:
                        comments = comments+'\n' +"("+current_port + '):\n'+'\n'.join(comments_list)
                    
                    # # print(comments)
                    # # print("-------")

                else:
                    if comments == "":
                        comments = 'MQP:\n'+'\n'.join(comments_list)
                    else:
                        comments = comments +'\n'.join(comments_list)

            else:
                if comments == "":
                        comments = '\n'.join(comments_list)
                else:
                    comments = comments + '\n' + '\n'.join(comments_list)
        
        # # print("*************************************************************************")
        # # print(comments)
        Globals.RESULT_DATA[str(data[0])] = comments

    elif Globals.RESULT_DATA[str(data[0])] == "PASS":
        Globals.RESULT_DATA[str(data[0])] = ""
    else:
        Globals.RESULT_DATA[str(data[0])] = ""
    
def get_value(data,file_list,soup_list):
    if "Comment" in Globals.CURRENT_TABLE:
        comment_need = get_result(data,file_list)
        get_comment(data,file_list,soup_list)
    else:
        get_result(data,file_list)
    
    return True
