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
    # # log_file = Globals.PROJECT_NAME + "_" + Globals.START_TIME 
    # # # print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # print(param_list)
    # # for param in param_list:
    # #     # print(param)
    Gen_Report()
    
    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # # # ============ Testing Code ============
    for idx in Globals.RESULT_DATA:
        print(idx,":",Globals.RESULT_DATA[idx])
    # # print("56239:",Globals.RESULT_DATA["56239"])
    # # for idx in Globals.ALL_FOLDER:
    # #     # print(idx,":",Globals.ALL_FOLDER[idx])



    print(start_time,":",end_time)

    sys.stdout = original_stdout

