# import Globals
from bs4 import BeautifulSoup
from datetime import datetime
import Globals

def get_result(data,file_list):
    for file in file_list:
        print(file)
        # with open(file, 'rb') as f:
        #     html_doc = f.read()
        
        with open(file, 'rb') as f:
            lines = f.readlines()

        # soup = BeautifulSoup(html_doc, 'html.parser') 
        # h4_list = soup.find_all("h4")
        # h6_list = soup.find_all("h6")

        # print(len(h4_list),":",len(h6_list))

        h4_dict = {}
        h6_dict = {}
        for i,line in enumerate(lines):
            if "h4" in str(line):
                if str(line) not in h4_dict.keys():
                    h4_dict[str(line)] = []
                    
                h4_dict[str(line)].append(i)

                # h4_dict[i] = str(line)
            if "h6" in str(line):
                # h6_dict[i] = str(line)
                if str(line) not in h6_dict.keys():
                    h6_dict[str(line)] = []
                    
                h6_dict[str(line)].append(i)
        keyword_line = -1
        result_line = -1

        for h4 in h4_dict:
            if data[2] in h4:
                # print(data[2])
                keyword_line = h4_dict[h4]
                if len(keyword_line) == 1:
                    result_line = keyword_line[0]+1
                break
        if keyword_line != -1 and result_line != -1:
            for h6 in h6_dict:
                if result_line in h6_dict[h6]:
                    if str(data[0]) in Globals.RESULT_DATA.keys():
                        if "PASS" in h6:
                            Globals.RESULT_DATA[str(data[0])] = "PASS"
                    else:
                        if "PASS" in h6:
                            Globals.RESULT_DATA[str(data[0])] = "PASS"
                        if "FAIL" in h6:
                            Globals.RESULT_DATA[str(data[0])] = "FAIL"
    
def get_value(data,file_list,soup_list):
    if "Comment" in Globals.CURRENT_TABLE:
        # get_comment(data,file_list)
        Globals.RESULT_DATA[str(data[0])] = ""
    else:
        
        get_result(data,file_list)
    return True
