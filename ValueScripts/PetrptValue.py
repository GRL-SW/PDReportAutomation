import Globals

def get_result(data,file_list):
    result_list = []
    for file in file_list:
        result = "N/A"
        with open(file, 'rb') as f:
            lines = f.readlines()
        pure_text = []
        for line in lines:
            pure_text.append(str(line).replace('b\'',"").replace('\\r\\n\'',""))

            for text in pure_text:
                if data[2] in text and "Pass" in text:
                    result = "PASS"
                    # print(result)
                    break
                elif data[2] in text and "Fail" in text:
                    result = "FAIL"
                    # print(result)
                    break
        if result != "N/A":
            result_list.append(result)

    print(result_list)

    if len(result_list) == 0:
        return
    elif "Fail" in result_list:
        Globals.RESULT_DATA[str(data[0])] = "FAIL"

    elif "Fail" not in result_list and "N/A" not in result_list:
        Globals.RESULT_DATA[str(data[0])] = "PASS"

    
def get_value(data,file_list):
    if "Comment" in Globals.CURRENT_TABLE:
        Globals.RESULT_DATA[str(data[0])] = ""
        pass
    else:
        get_result(data,file_list)
    
            