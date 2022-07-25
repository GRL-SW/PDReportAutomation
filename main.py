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
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(param_list)
    
    original_stdout = sys.stdout
    # log_file = Globals.PROJECT_NAME + "_" + Globals.START_TIME
    log_file = Globals.PROJECT_NAME + "_" + datetime.now().strftime('%Y%m%d_%H%M%S')
    sys.stdout = Commonlib.PrintLog(log_file) 
    Gen_Report()
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # # ============ Testing Code ============
    # for idx in Globals.RESULT_DATA:
    #     print(idx,":",Globals.RESULT_DATA[idx])

    # for idx in Globals.ALL_FOLDER:
    #     print(idx,":",Globals.ALL_FOLDER[idx])

    sys.stdout = original_stdout
        