import Globals

def get_pure_text(file):
    with open(file, 'rb') as f:
        lines = f.readlines()
    pure_text = []
    for line in lines:
        pure_text.append(str(line).replace('b\'',"").replace('\\r\\n\'',""))

    return pure_text

def build_info(pure_text,data):
    detail_info = []
    summary_info = ""
    get_summary = False
    start_getvalue = False
    for text in pure_text:
        if get_summary == False:
            if "Opening script: " in text and data[2] in text:
                detail_info.append(text)
                start_getvalue = True
            elif start_getvalue == True and "End of Script" in text:
                detail_info.append(text)
                start_getvalue = False
                get_summary = True
            elif start_getvalue == True:
                detail_info.append(text)
        else:
            if "Pass - " in text or "FAIL - " in text and data[2] in text:
                summary_info = text
    
    # # print("-----DETAIL-----")           
    # for text in detail_info:
    #     # print(text)

    # # print("-----SUMMARY-----")
    # # print(summary_info)

    # # print("***************************************************")

    return detail_info,summary_info

def chk_pass_result(detail_info):
    pass_value = True
    for key in detail_info:
        for text in detail_info:
            if "automatic pass" in text:
                return False

    return pass_value

def fail_msg(detail_info):
    re_fail_msg = []
    for msg in detail_info:
        if "FAIL: " in msg:
            tmp = msg.split("FAIL: ")[1]
            if tmp not in re_fail_msg:
                re_fail_msg.append(tmp)
    
    return re_fail_msg


def get_result(data,file_list):
    result_list = []
    summary_get = False
    for file in file_list:
        # # print(file)
        pure_text = get_pure_text(file)
        result = "N/A"
        detail_info,summary_info = build_info(pure_text,data)
        # print("summary:",summary_info)
        
        if "Pass" in summary_info:
            if chk_pass_result(detail_info):
                result = "PASS"
        elif "FAIL" in summary_info:
            result = "FAIL"

        if result != "N/A":
            result_list.append(result)

    # print(result_list)

    if len(result_list) == 0:
        return
    elif "FAIL" in result_list:
        Globals.RESULT_DATA[str(data[0])] = "FAIL"

    elif "FAIL" not in result_list:
        Globals.RESULT_DATA[str(data[0])] = "PASS"

def chk_insert(msg_list,string):
    for msg in msg_list:
        if string in msg:
            return False

    return True

def get_comment(data,file_list):
    re_fail_msg = []
    port_name = ""
    current_port = ""
    string = ""
    msg = []
    insert_msg = True

    for file in file_list:
        # print(file)
        pure_text = get_pure_text(file)
        result = "N/A"
        detail_info,summary_info = build_info(pure_text,data)
       

        if "FAIL" in summary_info:
            re_fail_msg = list(set(fail_msg(detail_info)))
            # print("re:",re_fail_msg)

        if len(re_fail_msg) == 0:
            msg = []
        else:
            if "2 Port" in Globals.CURRENT_TABLE:
                path_list = file.split("\\")
                port_name = path_list[len(path_list)-4]
                if current_port != port_name:
                    current_port = port_name
                    string = "("+current_port + '):\n'+'\n'.join(re_fail_msg)
                else:
                    string = '\n'.join(re_fail_msg)
                    insert_msg = chk_insert(msg,string)
                    # print("insert_msg:",insert_msg)
            else:
                string = '\n'.join(re_fail_msg)

            if insert_msg == True:
                msg.append(string)
            else:
                insert_msg = True
    
    # print("msg:",msg)

    if len(msg) == 0:
        Globals.RESULT_DATA[str(data[0])] = ""
    else:
        Globals.RESULT_DATA[str(data[0])] = '\n'.join(msg)

    return

    
def get_value(data,file_list):
    if "Comment" in Globals.CURRENT_TABLE:
        get_comment(data,file_list)
    else:
        get_result(data,file_list)
    
            