import Globals
from bs4 import BeautifulSoup
import ValueScripts.HtmlCommonlib as HtmlCommonLib

def get_comments(details,comments,folder_name):
    for d in details:
        if "ERROR" in d or "FAILED" in d:
            d_list = d.split('\n')
            comment_tmp = d_list[2] + ":" + d_list[3]
            if comment_tmp not in comments[folder_name]:
                comments[folder_name].append(comment_tmp)
    return comments

def set_comments_key(comments,folder_name):
    if folder_name not in comments.keys():
        comments[folder_name] = []

    return comments

def get_summary_list(key,soup):
    summary = []
    tables = soup.find_all('table')
    for t in tables:
        # # print(t.text)
        tr_list = t.find_all('tr')
        # # print(t.text,":","USB Type-C Functional Tests" in t.text)
        # # print(Globals.CURRENT_TABLE,":","Type-C Functional Testing" in Globals.CURRENT_TABLE)

        # # print("Merged USB PD" in t.text)
        # # print("USB Power Delivery Compliance Test Merged" in Globals.CURRENT_TABLE)

        if "USB Type-C Functional Tests" in t.text and "Type-C Functional Testing" in Globals.CURRENT_TABLE:
            for tr in tr_list:
                if key[0] in tr.text:
                    summary.append(tr.text)
        elif "Merged USB PD" in t.text and "USB Power Delivery Compliance Test Merged" in Globals.CURRENT_TABLE:
            for tr in tr_list:
                if key[0] in tr.text:
                    summary.append(tr.text)
        elif "COMMON.CHECK.PD" in t.text and "USB Power Delivery Compliance Test Merged" in Globals.CURRENT_TABLE:
            for tr in tr_list:
                if key[0] in tr.text:
                    summary.append(tr.text)
        elif "COMMON.PROC.PD" in t.text and "USB Power Delivery Compliance Test Merged" in Globals.CURRENT_TABLE:
            for tr in tr_list:
                if key[0] in tr.text:
                    summary.append(tr.text)

    return summary

def get_detail(key,soup):
    details = []
    tables = soup.find_all('table')
    
    for t in tables:
        # # print(t.text)
        tr_list = t.find_all('tr')
        if key[0] in t.text:
            # # print("in")
            for tr in tr_list:
                # # print(tr.text)
                details.append(tr.text)

    return details


def get_result_list(data,soup_list):
    key = data[2].split(",")
    result_list = []
    for soup in soup_list:
        summary = get_summary_list(key,soup)
        if "Passed" in "#".join(summary):
            result_list.append("PASS")
        elif "Not Applicable" in "#".join(summary):
            result_list.append("N/A")
        elif "Failed" in "#".join(summary):
            result_list.append("FAIL")
        elif "Error" in "#".join(summary):
            result_list.append("FAIL")
        else:
            result_list.append("N/A")
    return result_list

def get_result(data,soup_list):
    key = data[2].split(",")
    # print(data[2])
    result_list = get_result_list(data,soup_list)
    print(result_list)

    if "COMMON." not in data[2]:
        if "PASS" in result_list:
            Globals.RESULT_DATA[str(data[0])] = "PASS"
        elif "FAIL" in result_list and "PASS" not in result_list:
            Globals.RESULT_DATA[str(data[0])] = "FAIL"
    else:
        if "FAIL" in result_list:
            Globals.RESULT_DATA[str(data[0])] = "FAIL"
        elif "PASS" in result_list and "FAIL" not in result_list:
            Globals.RESULT_DATA[str(data[0])] = "PASS"
    return

def get_comment(data,file_list):
    key = data[2].split(",")
    comments = {}
    result_list = get_result_list(data,Globals.SOUP_LIST)
    print(result_list)

    fail_comment_idx = HtmlCommonLib.set_fail_idx(data,result_list)

    print(fail_comment_idx)

    if len(fail_comment_idx) == 0:
        Globals.RESULT_DATA[str(data[0])] = ""
        return

    for fci in fail_comment_idx:
        details = get_detail(key,Globals.SOUP_LIST[fci])
        summary = get_summary_list(key,Globals.SOUP_LIST[fci])

        folder_name_list = Globals.DATA_FILE[fci].split("\\")
        if "USB Power Delivery Compliance Test Merged" in Globals.CURRENT_TABLE:
            folder_name = folder_name_list[len(folder_name_list)-3]
        else:
            folder_name = folder_name_list[len(folder_name_list)-2]

        if "Failed" in "#".join(summary):
            comments = set_comments_key(comments,folder_name)
            comments = get_comments(details,comments,folder_name)
                
                    
        elif "Error" in "#".join(summary):
            print("Error find")
            comments = set_comments_key(comments,folder_name)
            comments = get_comments(details,comments,folder_name)

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
def get_value(data,file_list,soup_list,reload):
    if "Comment" in Globals.CURRENT_TABLE:
        get_comment(data,file_list)
    else:
        
        get_result(data,soup_list)
    return True