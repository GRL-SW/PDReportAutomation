import Globals
from bs4 import BeautifulSoup
from datetime import datetime

def get_rawdata(soup):
    raw_data=[]

    tables = soup.find_all('table')
    if len(tables) < 4:
        return
    else:
        target_table = tables[3]

    tr_list = target_table.find_all('tr')
    for tr in tr_list:
        print(tr.text.replace('\n',"###"))

    

def get_result(data,soup_list):
    for i,soup in enumerate(soup_list):
        tables = soup.find_all('table')
        
        if len(tables) < 4:

            continue
        else:
            target_table = tables[3]
         
        tr_list = target_table.find_all('tr')
        # if data[0] == 55237:
        #     # print(target_table.text)
        #     for tr in tr_list:
        #         print(tr.text.replace("\n","###"))

        if data[2] in target_table.text:
            # print(i,":",data[2],":in")
            for tr in tr_list:
                # print(tr.text)
                # print(tr.text,":",data[2])
                if data[2] in tr.text:
                    if Globals.RESULT_DATA[str(data[0])] == "FAIL":
                        if "PASS" in tr.text:
                            Globals.RESULT_DATA[str(data[0])] = "PASS"
                    else:
                        if "PASS" in tr.text:
                            Globals.RESULT_DATA[str(data[0])] = "PASS"
                        elif "FAIL" in tr.text:
                            Globals.RESULT_DATA[str(data[0])] = "FAIL"
                    break
        else:
            # print(i,":",data[2],":out!!!!!!!")
            pass

    return

def chk_keyword(tr):
    stop_loop = False
    item_name = ""
    for keyword in Globals.ALL_KEYWORDS:
        # print(rd_list,":",keyword)
        if keyword.strip() in tr:
            stop_loop = True
            item_name = keyword
            break

    # print(stop_loop,":",item_name)

    return stop_loop,item_name

def get_comment(data,soup_list,):
    comments = {}
    get_comment = False
    for i,soup in enumerate(soup_list):
        tables = soup.find_all('table')
        if len(tables) < 4:
            return
        else:
            target_table = tables[3]
        folder_name_list = Globals.DATA_FILE[i].split("\\")
        port_name = folder_name_list[len(folder_name_list)-3]

        tr_list = target_table.find_all('tr')
        for tr_idx,tr in enumerate(tr_list):
            if data[2] in tr.text:
                if "FAIL" in tr.text:
                    get_comment = True
                    j=tr_idx
                    if port_name not in comments.keys():
                        comments[port_name] = []
                    while j < len(tr_list):
                        stop_loop = False
                        if j != tr_idx:
                            stop_loop,item_name = chk_keyword(tr_list[j].text)
                        print(stop_loop)
                        if stop_loop == True:
                            break  

                        if "FAIL" in tr_list[j].text and j != tr_idx:
                            stop_loop,item_name = chk_keyword(tr_list[j])
                            string = tr_list[j].text.replace("\n\xa0 ","").replace("FAIL  \n&nbsp","").replace("\n","")
                            
                            print("FAIL:",string)

                            comments[port_name].append(string)
                        j = j + 1
                else:
                    get_comment = False

    print(comments)

    if len(comments) > 0 and get_comment == True:
        string = ""
        for folder in comments:
            if "2 Port" in Globals.CURRENT_TABLE and string == "":
                string = "(" + folder+ ")" + "\n".join(comments[folder])
            if "2 Port" in Globals.CURRENT_TABLE and string != "":
                string = string + "\n" + "(" + folder+ ")" + "\n".join(comments[folder])
            elif string == "":
                string = "\n".join(comments[folder])
            else:
                string = string + "\n".join(comments[folder]) + "\n"

        
        Globals.RESULT_DATA[str(data[0])] = "C2:" + string
    else:
        Globals.RESULT_DATA[str(data[0])] = ""

        # for item in Globals.ALL_KEYWORDS:
        #     print(item)

    return    


def get_value(data,soup_list):
    if "Comment" in Globals.CURRENT_TABLE:
        print("select comment")
        get_comment(data,soup_list)
    else:
        get_result(data,soup_list)