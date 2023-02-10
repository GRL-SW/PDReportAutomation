from unittest import result
import Globals
from bs4 import BeautifulSoup
from datetime import datetime
import ValueScripts.HtmlCommonlib as HtmlCommonLib

def get_result_list(data,soup_list):
    result_list = []
    for i,soup in enumerate(soup_list):
        tables = soup.find_all('table')
        result = "N/A"

        if len(tables) < 4:

            continue
        else:
            target_table = tables[3]
         
        tr_list = target_table.find_all('tr')

        if data[2] in target_table.text:
            for tr in tr_list:
                if data[2] in tr.text:
                    if "PASS" in tr.text:
                        result = "PASS"
                    elif "FAIL" in tr.text:
                        result = "FAIL"
                    break
        result_list.append(result)

    return result_list

def get_result(data,soup_list):
    result_list = get_result_list(data,soup_list)
    if "PASS" not in result_list and "FAIL" not in result_list:
        return
    elif "COMMON." not in data[2]:
        if "PASS" in result_list:
            Globals.RESULT_DATA[str(data[0])] = "PASS"
        else:
            Globals.RESULT_DATA[str(data[0])] = "FAIL"
    else:
        if "FAIL" in result_list:
            Globals.RESULT_DATA[str(data[0])] = "FAIL"
        else:
            Globals.RESULT_DATA[str(data[0])] = "PASS"
    return

def chk_keyword(tr):
    stop_loop = False
    item_name = ""
    for keyword in Globals.ALL_KEYWORDS:
        # # print(rd_list,":",keyword)
        if keyword.strip() in tr:
            stop_loop = True
            item_name = keyword
            break

    # # print(stop_loop,":",item_name)

    return stop_loop,item_name

def get_comment(data,soup_list):
    result_list = get_result_list(data,soup_list)
    print(result_list)
    
    fail_comment_idx = fail_comment_idx = HtmlCommonLib.set_fail_idx(data,result_list)
    print(fail_comment_idx)
    
    comments = {}
    if len(fail_comment_idx) == 0:
        Globals.RESULT_DATA[str(data[0])] = ""
        return
    
    for fci in fail_comment_idx:
        tables = soup_list[fci].find_all('table')
        if len(tables) < 4:
            return
        else:
            target_table = tables[3]

        if data[2] not in target_table.text:
            break

        folder_name_list = Globals.DATA_FILE[fci].split("\\")
        port_name = folder_name_list[len(folder_name_list)-3]
        # print(port_name)
        tr_list = target_table.find_all('tr')
        port_dic = {"PA":"Port 1","PB":"Port 2"}
        for tr_idx,tr in enumerate(tr_list):
            if data[2] in tr.text:
                if "FAIL" in tr.text:
                    j=tr_idx
                    if port_name not in comments.keys():
                        comments[port_dic[port_name]] = []
                    while j < len(tr_list):
                        stop_loop = False
                        if j != tr_idx:
                            stop_loop,item_name = chk_keyword(tr_list[j].text)
                        # print(stop_loop)
                        if stop_loop == True:
                            break  

                        if "FAIL" in tr_list[j].text and j != tr_idx:
                            stop_loop,item_name = chk_keyword(tr_list[j])
                            string = tr_list[j].text.replace("\n\xa0 ","").replace("FAIL  \n&nbsp","").replace("\n","")                        
                            print("FAIL:",string)
                            if string not in comments[port_dic[port_name]]:
                                comments[port_dic[port_name]].append(string)
                        j = j + 1   

    # print(comments)

    if len(comments) > 0:
        string = ""
        for folder in comments:
            if "2 Port" in Globals.CURRENT_TABLE and string == "":
                string = "(" + folder+ ")" + "\n".join(comments[folder])
            elif "2 Port" in Globals.CURRENT_TABLE and string != "":
                string = string + "\n" + "(" + folder+ ")" + "\n".join(comments[folder])
            elif string == "":
                string = "\n".join(comments[folder])
            else:
                string = string + "\n".join(comments[folder]) + "\n"

        print(string)

        Globals.RESULT_DATA[str(data[0])] = "C2:\n" + string
    else:
        Globals.RESULT_DATA[str(data[0])] = ""

    return    


def get_value(data,soup_list):
    if "Comment" in Globals.CURRENT_TABLE:
        # print("select comment")
        get_comment(data,soup_list)
    else:
        get_result(data,soup_list)