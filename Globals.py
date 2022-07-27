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
    # print("report_info:",report_info)

    global ALL_FOLDER
    global INPUT_PATH
    global FINAL_PATH
    global REPORT_NAME
    global PROJECT_NAME
    global TYPELIST
    global TEMPLATE_TYPE
    global PORT_NUM
    global TEMPLATE_WORD_NAME
    global RESULT_DATA
    global DATA_FILE
    global SELECT_TABLES
    global REPORT_NAME
    global ALL_KEYWORDS
    global PATH_KEY
    global SOUP_LIST
    global START_TIME
    global LOG_FILE

    global TABLES
    global CURRENT_TABLE
    global CURRENT_TYPE
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
    TEMPLATE_WORD_NAME = "\\\\192.168.2.104\\Public\\Software\\07_PDReportAutomation\\pd compliance new\\blank template\\" + TEMPLATE_TYPE
    print(TEMPLATE_WORD_NAME)
    DATA_FILE = []
    SELECT_TABLES = []
    ALL_KEYWORDS = []
    PATH_KEY = ""
    SOUP_LIST = []

    if len(param) == 9:
        START_TIME = param[8]
        REPORT_NAME = FINAL_PATH + "\\report\\PD\\" + START_TIME + "_"+ TEMPLATE_TYPE
        LOG_FILE = PROJECT_NAME + "_" + START_TIME
    else:
        START_TIME = datetime.now().strftime('%Y%m%d_%H%M%S')
        REPORT_NAME = FINAL_PATH + "\\report\\PD\\" + datetime.now().strftime('%Y%m%d_%H%M%S') + "_"+ TEMPLATE_TYPE
        LOG_FILE = PROJECT_NAME + "_" + datetime.now().strftime('%Y%m%d_%H%M%S')

    sys.stdout = Commonlib.PrintLog(LOG_FILE)




    