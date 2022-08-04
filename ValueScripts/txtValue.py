from matplotlib.pyplot import text
import Globals

def get_pure_text(file):
    pure_text = []
    with open(file, 'rb') as f:
        lines = f.readlines()
    for line in lines:
        pure_text.append(str(line).replace('b\'',"").replace('\\r\\n\'',""))

    return pure_text

def chk_keywords(pure_text,keyword):
    for text in pure_text:
        if keyword in text:
            return True

    return False

def test_result(pure_text,keyword):
    result = "N/A"
    for i,text in enumerate(pure_text):
        key_line = 0
        if keyword in text:
            key_line = i
            result = pure_text[i+1]

    print("Result:",result)

    return result

def get_result(data,file_list):
    
    for file in file_list:
        print(file)
        result_list = []
        result = "N/A"
       
        pure_text = get_pure_text(file)
        keywords = data[2].split(",")
        if chk_keywords(pure_text,keywords[0]):
            result = test_result(pure_text,keywords[1])

        if result != "N/A":
            result_list.append(result)

    if len(result_list) == 0:
            return
    elif "FAIL" in result_list:
        Globals.RESULT_DATA[str(data[0])] = "FAIL"

    elif "FAIL" not in result_list:
        Globals.RESULT_DATA[str(data[0])] = "PASS"

def get_msg_list(pure_text,keywords):
    msg_list = []
    for text in pure_text:  
        if keywords[2] in text or keywords[3] in text:
            msg_list.append(text.replace("\\n",""))

    return msg_list

def fail_msg(file_list,data):
    port_name = ""
    current_port = ""
    msg_list = []
    fail_msg = []
    keywords = data[2].split(",")
    # print(keywords[1],":",keywords[2])
    for file in file_list:
        pure_text = get_pure_text(file)
        if "2 Port" in Globals.CURRENT_TABLE:
            path_list = file.split("\\")
            port_name = path_list[len(path_list)-3]
            fail_msg = get_msg_list(pure_text,keywords)
            if current_port != port_name:
                current_port = port_name
                string = "("+current_port + '):\n'+'\n'.join(fail_msg)
                msg_list.append(string)
            else:
                string = '\n'.join(fail_msg)
        else:
            msg_list = get_msg_list(pure_text,keywords)


    return '\n'.join(msg_list)

def get_comment(data,file_list):
        
    for file in file_list:
        print(file)
        result_list = []
        result = "N/A"
       
        pure_text = get_pure_text(file)
        keywords = data[2].split(",")
        if chk_keywords(pure_text,keywords[0]):
            result = test_result(pure_text,keywords[1])

        if result != "N/A":
            result_list.append(result)

    print(result_list)

    if len(result_list) == 0:
            return
    elif "FAIL" in result_list:
        comment = fail_msg(file_list,data)
        Globals.RESULT_DATA[str(data[0])] = comment
    elif "FAIL" not in result_list:
        Globals.RESULT_DATA[str(data[0])] = ""

    
def get_value(data,file_list):
    if "Comment" in Globals.CURRENT_TABLE:
        get_comment(data,file_list)
    else:
        get_result(data,file_list)
    
            