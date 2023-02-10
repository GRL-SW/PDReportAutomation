from enum import unique
import Globals
import Commonlib
from bs4 import BeautifulSoup
import ValueScripts.HtmlCommonlib as HtmlCommonLib

def get_raw_data(soup):
    raw_data_list=[]
    target_index = []
    tables = soup.find_all('table',{'id':'tbl_main'})

    for tab in tables:
        tr_list = tab.find_all('tr')
        cols = (tr_list[0].text).split('\n')
        # # print(cols)
        for i in range(1,len(cols)-1):
            target_index.append(i)

        target_index = list(set(target_index))

        for t in tr_list[1:]:
            string = ""
            # # print(t.find_all('td'))
            
            td_list = t.find_all('td')
            # if len(td_list) < 3:
                # print(td_list)
            for i in range(0,len(target_index)):
                
                if i == len(target_index) - 1:
                    string = string + t.find_all('td')[i].text
                else:
                    string = string + t.find_all('td')[i].text+"//"
            raw_data_list.append(string)
    return raw_data_list

def chk_keyword(rd_list):
    stop_loop = False
    item_name = ""
    for keyword in Globals.ALL_KEYWORDS:
        # # print(rd_list,":",keyword)
        if keyword.strip() in rd_list[0].strip():
            stop_loop = True
            item_name = rd_list[0]
            break

    # # print(stop_loop,":",item_name)

    return stop_loop,item_name

def get_result_list(data,file_list):
    result_list = []
    set_result = False
    for file in file_list:
        print(file)
        set_result = False
        with open(file, 'r', encoding='utf-8', errors="ignore") as f:
            html_doc = f.read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        raw_data = get_raw_data(soup)
        # # print(raw_data)

        for rd in raw_data:
            rd_list = rd.split("//")
            if data[2] in rd_list[0]:
                if rd_list[1] == "Pass":
                    result_list.append("PASS")
                    set_result = True
                elif rd_list[1] == "Fail":
                    result_list.append("FAIL")
                    set_result = True

        if set_result == False:
            result_list.append("NA")

        print(result_list)
    return result_list

def get_comment(data,file_list):
    comments = {}
    fail_comment_idx = []
    
    result_list = get_result_list(data,file_list)
    print(result_list)
    
    fail_comment_idx = HtmlCommonLib.set_fail_idx(data,result_list)

    print(fail_comment_idx)

    for fci in fail_comment_idx:
        raw_data = get_raw_data(Globals.SOUP_LIST[fci])
        folder_name_list = Globals.DATA_FILE[fci].split("\\")
        if "USB Power Delivery Compliance Test Merged" in Globals.CURRENT_TABLE:
            folder_name = folder_name_list[len(folder_name_list)-3]
        else:
            folder_name = folder_name_list[len(folder_name_list)-2]
        # # print(raw_data)
        # print(file,":",data[2])
        for i,rd in enumerate(raw_data):
            rd_list = rd.split("//")
            if data[2] in rd_list[0]:
                if rd_list[1] == "Fail" or rd_list[1] == "N/A":
                    j=i
                    if folder_name not in comments.keys():
                        comments[folder_name] = []
                    while j < len(raw_data):
                        stop_loop = False
                        rd_list_tmp = raw_data[j].split("//")
                        if j != i:
                            stop_loop,item_name = chk_keyword(rd_list_tmp)

                        if stop_loop == True:
                            break
                        
                        if "Fail" in raw_data[j] and rd_list[1] == "Fail":
                            stop_loop,item_name = chk_keyword(rd_list_tmp)
                            string = ""
                            if stop_loop == False:
                                string = rd_list_tmp[0] + "-" + rd_list_tmp[2]
                            else:
                                string = rd_list_tmp[2]

                            # print("Fail:",string)

                            comments[folder_name].append(string)
                        elif rd_list[1] == "N/A" and "N/A" in raw_data[j]:
                            stop_loop,item_name = chk_keyword(rd_list_tmp)
                            string = ""
                            if stop_loop == False:
                                string = rd_list_tmp[0] + "-" + rd_list_tmp[2]
                            else:
                                string = rd_list_tmp[2]

                            # print("N/A:",string)
                            comments[folder_name].append(string)
                        
                            
                        j = j + 1

        if len(fail_comment_idx) == 0:
            Globals.RESULT_DATA[str(data[0])] = ""
            return

        if len(comments) != 0:
            # # print(comments)
            string = ""

            if "2 Port" in Globals.CURRENT_TABLE and "USB Power Delivery Compliance Test Merged" in Globals.CURRENT_TABLE:
                port_dic = {"PA":"Port 1","PB":"Port 2"}
                for folder in comments:
                    print(data[0],":",folder,":",comments[folder])
                    if string == "":
                        string = "LeCroy:\n(" + port_dic[folder] + "):" + "\n".join(comments[folder])
                    else:
                        string = string + '\n(' + port_dic[folder] + "):" + "\n".join(comments[folder])

            elif "Type-C Functional Testing" in Globals.CURRENT_TABLE:
                for folder in comments:
                    print(data[0],":",folder,":",comments[folder])
                    if string == "":
                        string = folder + ":" + "\n".join(comments[folder])
                    else:
                        string = string + '\n' + folder + ":" + "\n".join(comments[folder])
 
            print(string)
            Globals.RESULT_DATA[str(data[0])] = string
            # else:
                # Globals.RESULT_DATA[str(data[0])] = ""

            # if "PASS" in result:
            #     Globals.RESULT_DATA[str(data[0])] = ""



def get_result(data,file_list):
    result_list = get_result_list(data,file_list)

    if len(result_list) != 0:
        if "COMMON." in result_list:
            if "FAIL" in result_list:
                Globals.RESULT_DATA[str(data[0])] = "FAIL"
            elif "FAIL" not in result_list and "PASS" in result_list:
                Globals.RESULT_DATA[str(data[0])] = "PASS"
        else:
            if "PASS" not in result_list and "FAIL" in result_list:
                Globals.RESULT_DATA[str(data[0])] = "FAIL"
            elif "FAIL" not in result_list and "PASS" in result_list:
                Globals.RESULT_DATA[str(data[0])] = "PASS"

def get_value(data,file_list):
    if "Comment" in Globals.CURRENT_TABLE:
        get_comment(data,file_list)
    else:
        get_result(data,file_list)
    return True


