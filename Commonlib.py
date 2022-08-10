# File Name :Commonlib.py
# Brief:
    # Some common function in this script
    # Current Functions:
        # is_float
        # round_up
        # adjuctValueLength
        # adjustValueUnit
        # check_file
        # getTargetFile
        # getPath
        # getTargetTag
        # findTable
        # get_reg_result_list
        # get_reg_result_string
        # save_all_folder
        # add_tag
        # Class-PringLog

# Author: Sammi Guo
# Date:2021.11.23

import os
import sys
import re
import Globals
import DBProcess
import Globals

def is_float(string):
    try:
        if string=='NaN':
            return False
        else:
            float(string)
            return True
    except ValueError:
        return False

def round_up(n, m):
    n = str(n)
    if len(n) - n.index(".") - 1 == m + 1:
        n += "1"
    n = float(n)
    return round(n, m)

def adjustValueLength(string, specLength = 5):
    return_str = ""
    pointIdx = string.find(".")
    if is_float(string) == True:
        num = float(string)
        if pointIdx != -1:
            round_idx = specLength - pointIdx - 1
            return_str = str(round_up(num,round_idx))
        else:
            return str(num)
          
    return return_str

def adjustValueUnit(string, origin_unit, convert_unit, length=2):
    num = 0.0
    re_str = ""
    origin_unit = origin_unit.lower()
    convert_unit = convert_unit.lower()

    # # print(origin_unit," v.s ",convert_unit)
    # # print("µs".encode('utf-8'))
    # # print(origin_unit.encode('utf-8'))
    # # print(origin_unit == "ns")
    # # print(convert_unit == "μs")
    # # print(is_float(string) == True)

    # k x m µ n p f

    if is_float(string) == True:
        if origin_unit == "mv" and convert_unit == "v":
            # print("mV to V")
            num = round(float(string)/1000, length)
        elif origin_unit == "v" and convert_unit == "mv":
            # print("V to mV")
            num = round(float(string)*1000, length)
        elif origin_unit == "µv" and convert_unit == "mv":
            # print("µV to mV")
            num = round(float(string)/1000, length)
        elif origin_unit == "ms" and convert_unit == "µs":
            # print("ms to μs")
            num = round(float(string)*1000, length)
        elif origin_unit == "ns" and convert_unit == "μs":
            # print("ns to μs")
            num = round(float(string)/1000, length)
        elif origin_unit == "µs" and convert_unit == "ms":
            # print("µs to ms")
            num = round(float(string)/1000, length)
        elif origin_unit == "µs" and convert_unit == "ns":
            # print("µs to ns")
            num = round(float(string)*1000, length)
        elif origin_unit == "ps" and convert_unit == "fs":
            # print("ps to fs")
            num = round(float(string)*1000, length)
        elif origin_unit == "ns" and convert_unit == "µs":
            # print("ns to µs")
            num = round(float(string)/1000, length)
        elif "kppm" in origin_unit and "ppm" in convert_unit:
            # print("kppm to ppm")
            num = round(float(string)*1000, length)
        elif origin_unit == "?s" and convert_unit == "ns":
            # print("?s to ns")
            num = float(string)*1000
        elif origin_unit == "繕s" and convert_unit == "ns":
            # print("繕s to ns")
            num = float(string)*1000
        else:
            return format(float(string), '.2f')
    else:
        return 

    return str(num)     
    # return re_str

def check_file(file,file_key):
    keys = file_key.split(",")
    pass_cnt = len(keys)
    key_in_file = 0
    for key in keys:
        key = key.strip()
        if key in file:
            key_in_file = key_in_file + 1
    if key_in_file == pass_cnt:
        return True
    else:
        return False

def getTargetFile(path, file_key, filetype):
    files = os.listdir(path)
    keys = file_key.split(",")
    pass_cnt = len(keys)
    return_list = []
    for file in files:
        # # print(file)
        key_in_file = 0
        for key in keys:
            # # print(key)
            key = key.strip()
            if key in file:
                # # print("in1")
                key_in_file = key_in_file + 1
            elif key.upper() in file:
                # # print("in2")
                if key == "png" or key == "xlsx":
                    # # print("in2")
                    key_in_file = key_in_file + 1
                elif "Sideband" in Globals.CURRENT_TABLE: 
                    # # print("in3")               
                    key_in_file = key_in_file + 1
            elif "Sideband" in Globals.CURRENT_TABLE:
                # # print("Upper case:",key.upper(),",",file.upper())
                if key.upper() in file.upper():     
                    # # print("in3")               
                    key_in_file = key_in_file + 1
        # # print(key_in_file)
        if key_in_file == pass_cnt:
            if filetype == "IMAGE":
                if file.endswith("jpg") or file.endswith("JPG") or file.endswith("png") or file.endswith("PNG"):
                    return_file = r''+path+"\\"+file
                    return_list.append(return_file)
            else:
                return_file = r''+path+"\\"+file
                return_list.append(return_file)
    
    return return_list
            

def getPath(input_path,string, allFolder):
    path_key = string.split("/")
    key_len = len(path_key)
    return_Path=[]
    input_path = input_path + "\\"
    for folder in allFolder:
        folder_list = (folder.split(input_path)[1]).split("\\")
        # # print(folder_list)
        if allFolder[folder] == key_len:
            cnt_tmp = 0
            for i,key in enumerate(path_key):
                if key in folder_list[i]:
                    # # print(key,":",folder)
                    cnt_tmp = cnt_tmp + 1
                elif key in str(folder_list[i]).upper():
                # elif key.upper() in str(folder_list[i]).upper():
                    # # print(key,":",folder)
                    cnt_tmp = cnt_tmp + 1

            if cnt_tmp == key_len:
                # # print(folder)
                return_Path.append(folder)
    return return_Path

def getTargetTag(soup,key):
    test = soup.find_all(key)
    span_list = []
    re_list = []
    for t in test:
        t_str = str(t.text).strip()
        span_list.append(t_str)

    for span in span_list:
        if span != "":
            re_list.append(span)

    return re_list

def findTable(values,template_id):
    result_table = []

    select_tables = "SELECT * FROM `tables` where `Template_ID` = " + str(template_id)
    Table_list=DBProcess.excute_SQL(select_tables)
    for table in Table_list:
        # # print(table[0])
        find_text = "SELECT * FROM `content` WHERE `Table_ID` = " + str(table[0])
        text_list=DBProcess.excute_SQL(find_text)
        is_find = True
        for text in text_list:
            # # print("text:",text)
            for v in values:
                # # print("v:",v)
                # # print(v in text_list)
                if text[1].find(v.strip()) == -1 or table[2] in result_table:
                    is_find=False
        if is_find == True:
            result_table.append(table[2])

    return result_table

def get_reg_result_list(rule,input_list):
    return_list = {}
    for input in input_list:
        regex = re.compile(rule)
        match = regex.search(input)
        if str(match) == "None":
            return_list[input] = False
        else:
            return_list[input] = True

    return return_list

def get_reg_result_string(rule,string):
    regex = re.compile(rule)
    match = regex.search(string)
    if str(match) == "None":
        return False
    else:
        return True

class PrintLog(object):
    def __init__(self,file):
        self.console = sys.stdout
        # print(file)
        file_name = r'' + Globals.FINAL_PATH + "\\log\\PD\\log_" + file + ".txt"
        self.log_file = open(file_name, "w+", encoding='utf-8')

    def write(self, msg):
        self.console.write(msg)
        self.log_file.write(msg)

    def flush(self):
        pass   

def save_all_folder():
    all_Folder =  os.walk(Globals.INPUT_PATH)
    # result_folder = Globals.INPUT_PATH+ "\\03"
    # info_folder = Globals.INPUT_PATH+"\\01"
    for ele in all_Folder:
        path_heirarchy = len(((ele[0].split(Globals.INPUT_PATH)[1].split("\\"))))-1
        if Globals.INPUT_PATH in ele[0] and path_heirarchy >= 1:
            Globals.ALL_FOLDER[ele[0]] = path_heirarchy
            # # print(ele[0])
        # elif info_folder in ele[0]:
        #     Globals.ALL_FOLDER[ele[0]] = -1

def add_tag(dataList,tag):
    for data in dataList:
        if tag not in data[2]:
            string = tag + "," + data[2]
            sql = "UPDATE `files` SET `File_Keyword` = \"" + str(string) + "\" WHERE `File_ID` = " + str(data[0])
            DBProcess.excute_SQL(sql)
        else:
            print(data[0],":","no add")
    return

def get_template_id(template_type):
    if "Power Delivery Pre-Compliance Test" in template_type and "1port" in template_type:
        return 5
    elif "Power Delivery Pre-Compliance Test" in template_type and "2port" in template_type:
        return 6


