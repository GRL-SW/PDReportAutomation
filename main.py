# File Name :main.py
# Brief:
    # Entry of Thunderbolt Automation code
    # Parameters:
        # Import data path
        # Output data path
        # DUT information
        # Report information
        # 0: Single Data 1:Multiple data: attach a csv file
        # Start Time : used in find log file
# Author: Sammi Guo
# Date:2021.12.17

import sys
import Commonlib
import Globals
import GetResult
import DBProcess as DBProcess
import UpdateFile as UpdateFile
import lib.word_lib as GRL_Word
from datetime import datetime
from bs4 import BeautifulSoup

def Gen_Report():
    Commonlib.save_all_folder()
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    Globals.OUTPUT_FILE = GRL_Word.Get_word(Globals.TEMPLATE_WORD_NAME)

    GetResult.save_pos_value(Globals.OUTPUT_FILE)

    print("Updating word...")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    DBProcess.connectDB() 
    UpdateFile.updateWord(Globals.OUTPUT_FILE)
    DBProcess.close_all()


if __name__ == '__main__':
    param_list = sys.argv
    Globals.initialize(param_list)
    
    original_stdout = sys.stdout
    # log_file = Globals.PROJECT_NAME + "_" + Globals.START_TIME 
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(param_list,":",len(param_list))
    # for param in param_list:
    #     print(param)
    Gen_Report()
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # # ============ Testing Code ============
    for idx in Globals.RESULT_DATA:
        print(idx,":",Globals.RESULT_DATA[idx])

    # for idx in Globals.ALL_FOLDER:
    #     print(idx,":",Globals.ALL_FOLDER[idx])

    # DBProcess.connectDB()
    # data_list = DBProcess.getFields(861)

    # start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # file = r'\\192.168.2.104\Public\Software\07_PDReportAutomation\pd compliance new\2 port DRP\USB Power Delivery Compliance Test (Merged)\PA\MQP\Report_0C56_C1_2022-03-03-10-26-11_CTS_CUST.html'

    # with open(file, 'rb') as f:
    #     html_doc = f.read()
    
    # with open(file, 'rb') as f:
    #     lines = f.readlines()
    # soup = BeautifulSoup(html_doc, 'html.parser') 

    # h4list = soup.find_all("h4")

    # # for h4 in h4list:
    # #     print(h4.text)
    # classify_words = {}

    # for line in lines:
    #     for h4 in h4list:
    #         if h4 in line:
    #             classify_words[h4] = line


    # for data in data_list:
    #     print(data[0])
    #     # for line in lines:
    #     for h4 in h4list:
    #         if data[2] in h4.text:
    #             print("in:",h4)
    #             break
        
    # end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # print(start_time,":",end_time)
    # DBProcess.close_all()