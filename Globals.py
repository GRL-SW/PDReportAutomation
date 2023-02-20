# File Name : Globals.py
# Brief:
    # initialize: initialize all global values using by main.py
# Author: Sammi Guo
# Date:2021.05.17

import os
import sys
import json
from datetime import datetime
import Commonlib

# initialize:
    # TABLES: all tables of usb test in database
    # TEMPLATE_WORD_NAME: default word file
    # TYPELIST:user input from website
        # TYPELIST[0]: Port Number
        # TYPELIST[1]: Equipment for Type-C Functional Test 

def initialize(param):
    
    if param[len(param) - 1] != "START_TIME":
        start_time = param[len(param) - 1]
    else:
        start_time = datetime.now().strftime('_%Y%m%d_%H%M%S')
    # # print("report_info:",report_info)

    global ALL_FOLDER
    global INPUT_PATH
    global FINAL_PATH

    global REPORT_NAME
    global PROJECT_NAME
    global TEMPLATE_WORD_NAME
    global LOG_FILE

    global TYPELIST
    global REPORT_INFO
    global TEMPLATE_TYPE
    global PORT_NUM
    global START_TIME

    global RESULT_DATA
    global DATA_FILE
    global SELECT_TABLES
    
    global ALL_KEYWORDS
    global PATH_KEY
    global SOUP_LIST
    
    global CURRENT_TABLE
    global CURRENT_TYPE
    global SUMMARY_LIST
    global DETAIL_LIST

    global TABLES
    global FIELDS
    global OUTPUT_FILE

    ALL_FOLDER = {}
    RESULT_DATA = {}
    INPUT_PATH = param[1]
    FINAL_PATH = param[2]
    PROJECT_NAME = param[3]
    TEMPLATE_TYPE = param[4]
    PORT_NUM = param[5]
    TYPELIST = param[6].split("%")
    REPORT_INFO = param[7].split(",")
    TEMPLATE_WORD_NAME = "\\\\192.168.2.104\\Public\\Report-Template-SW (勿刪)\\PowerDelivery\\" + TEMPLATE_TYPE
    # # print(TEMPLATE_WORD_NAME)
    
    DATA_FILE = []
    SELECT_TABLES = []
    ALL_KEYWORDS = []
    PATH_KEY = ""
    CURRENT_TYPE = ""
    CURRENT_TABLE = ""
    SOUP_LIST = []
    SUMMARY_LIST = []
    DETAIL_LIST = []

    if len(param) == 9:
        START_TIME = param[8]
        file_name = TEMPLATE_TYPE.replace("DUT model name",REPORT_INFO[5]).replace("yyyy_mm_dd",datetime.strptime(REPORT_INFO[13], "%Y/%m/%d").strftime('%Y_%m_%d'))
        # print(file_name)
        REPORT_NAME = FINAL_PATH + "\\report\\PD\\" + file_name
        LOG_FILE = PROJECT_NAME + "_" + START_TIME
    else:
        START_TIME = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = TEMPLATE_TYPE.replace("DUT model name",REPORT_INFO[5]).replace("yyyy_mm_dd",datetime.strptime(REPORT_INFO[13], "%Y/%m/%d").strftime('%Y_%m_%d'))
        # print(file_name)
        REPORT_NAME = FINAL_PATH + "\\report\\PD\\" + datetime.now().strftime('%Y%m%d_%H%M%S') + "_"+ file_name
        LOG_FILE = PROJECT_NAME + "_" + datetime.now().strftime('%Y%m%d_%H%M%S')

    sys.stdout = Commonlib.PrintLog(LOG_FILE)




    