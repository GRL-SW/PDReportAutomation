import Globals
from bs4 import BeautifulSoup

def get_comments(details,comments,folder_name,keyword):
    for d in details:
        if keyword in d:
            d_list = d.split('\n')
            comment_tmp = d_list[2] + ":" + d_list[3]
            if comment_tmp not in comments[folder_name]:
                comments[folder_name].append(comment_tmp)
    return comments

def set_comments_key(comments,folder_name):
    if folder_name not in comments.keys():
        comments[folder_name] = []

    return comments

def get_result(data,soup_list):
    key = data[2].split(",")
    # print(data[2])
    for soup in soup_list:
        tables = soup.find_all('table')

        summary = []
        details = []
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
            elif key[0] in t.text:
                # # print("in")
                for tr in tr_list:
                    # # print(tr.text)
                    details.append(tr.text)

        # # print("Summary:",summary)
        # # print("Details:",details)

        if "[Info Only]" in data[2] and "Comment" not in Globals.CURRENT_TABLE:
            Globals.RESULT_DATA[str(data[0])] = "Info Only"
            continue

        if Globals.RESULT_DATA[str(data[0])] == "FAIL":
            if "Passed" in "#".join(summary):
                Globals.RESULT_DATA[str(data[0])] = "PASS"
        else:
            if "Passed" in "#".join(summary):
                # # print("PASS")
                Globals.RESULT_DATA[str(data[0])] = "PASS"
            elif "Not Applicable" in "#".join(summary):
                # # print("NA")
                Globals.RESULT_DATA[str(data[0])] = "N/A"
            elif "Failed" in "#".join(summary):
                # # print("FAIL")
                Globals.RESULT_DATA[str(data[0])] = "FAIL"
            elif "Error" in "#".join(summary):
                # # print("FAIL")
                Globals.RESULT_DATA[str(data[0])] = "FAIL"

def get_comment(data,file_list):
    key = data[2].split(",")
    comments = {}

    for idx,file in enumerate(file_list):
        # print(file)
        folder_name_list = file.split("\\")
        folder_name = folder_name_list[len(folder_name_list)-2]
        
        soup = Globals.SOUP_LIST[idx]
        tables = soup.find_all('table')

        summary = []
        details = []
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
            elif key[0] in t.text:
                # # print("in")
                for tr in tr_list:
                    # # print(tr.text)
                    details.append(tr.text)

        # # print("Summary:",summary)
        # # print("Details:",details)

        if "Passed" in "#".join(summary):
            Globals.RESULT_DATA[str(data[0])] = ""
            continue
                
        if "Not Applicable" in "#".join(summary):
            comments = set_comments_key(comments,folder_name)
            comments = get_comments(details,comments,folder_name,"SKIPPED")
                
        if "Failed" in "#".join(summary):
            comments = set_comments_key(comments,folder_name)
            comments = get_comments(details,comments,folder_name,"FAILED")
                
                    
        elif "Error" in "#".join(summary):
            comments = set_comments_key(comments,folder_name)
            comments = get_comments(details,comments,folder_name,"FAILED")

    if "Comment" in Globals.CURRENT_TABLE:
        # print("Update Comment")
        if len(comments) != 0:
            # # print(comments)
            string = ""
            for folder in comments:
                # # print(data[0],":",folder,":",comments[folder])
                if "Type-C Functional Testing" in Globals.CURRENT_TABLE:
                    if string == "":
                        string = folder + ":" + "\n".join(comments[folder])
                    else:
                        string = string + '\n' + folder + ":" + "\n".join(comments[folder])
                elif "USB Power Delivery Compliance Test Merged":
                    if string == "":
                        string = "Ellisys" + ":" + "\n".join(comments[folder])
                    else:
                        string = string + '\n' + folder + ":" + "\n".join(comments[folder])
            # # print(string)

            Globals.RESULT_DATA[str(data[0])] = string
        else:
            Globals.RESULT_DATA[str(data[0])] = ""
    return

def get_value(data,file_list,soup_list):
    if "Comment" in Globals.CURRENT_TABLE:
        get_comment(data,file_list)
    else:
        
        get_result(data,soup_list)
    return True