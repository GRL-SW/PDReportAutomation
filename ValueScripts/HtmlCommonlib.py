import Globals

def set_fail_idx(data,result_list):
    fail_comment_idx = []
    current_port = ""
    current_folder = ""
    result_tmp = []
    idx_tmp = []

    for i,rl in enumerate(result_list):
        if "2 Port" in Globals.CURRENT_TABLE:
            folder_name_list = Globals.DATA_FILE[i].split("\\")
            port_name = folder_name_list[len(folder_name_list)-3]
            if current_port != port_name:
                current_port = port_name
                
                if len(result_tmp)!= 0 and len(idx_tmp) != 0 and "COMMON." not in data[2]:
                    # print("result temp:",result_tmp)
                    # print("idx temp:",idx_tmp)
                    if "PASS" not in result_tmp and "FAIL" in result_tmp:
                        for idx,rt in enumerate(result_tmp):
                            if rt == "FAIL":
                                fail_comment_idx.append(idx_tmp[idx])
                    result_tmp = []
                    idx_tmp = []
                    result_tmp.append(rl)
                    idx_tmp.append(i)
                elif len(result_tmp)!= 0 and len(idx_tmp) != 0 and "COMMON." in data[2]:
                    # print("result temp:",result_tmp)
                    # print("idx temp:",idx_tmp)
                    for idx,rt in enumerate(result_tmp):
                        if rt == "FAIL":
                            fail_comment_idx.append(idx_tmp[idx])
                    result_tmp = []
                    idx_tmp = []
                    result_tmp.append(rl)
                    idx_tmp.append(i)
                else:
                    result_tmp.append(rl)
                    idx_tmp.append(i)
            elif i == len(result_list) - 1:
                result_tmp.append(rl)
                idx_tmp.append(i)
                # print("result temp:",result_tmp)
                # print("idx temp:",idx_tmp) 
                if "PASS" not in result_tmp and "FAIL" in result_tmp and "COMMON." not in data[2]:
                    for idx,rt in enumerate(result_tmp):
                        if rt == "FAIL":
                            fail_comment_idx.append(idx_tmp[idx])
                elif "FAIL" in result_tmp and "COMMON." in data[2]:
                    for idx,rt in enumerate(result_tmp):
                        if rt == "FAIL":
                            fail_comment_idx.append(idx_tmp[idx])
            else:
                result_tmp.append(rl)
                idx_tmp.append(i)
        else:
            if rl == "FAIL":
                fail_comment_idx.append(i)

    return fail_comment_idx