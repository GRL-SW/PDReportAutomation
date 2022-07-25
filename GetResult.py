# File Name :GetResult.py
# Brief:
    # getResult: get the word value and position
    # getPos: get where the value filled
    # update_pos: update position to database
# Author: Sammi Guo
# Date:2021.05.27

from datetime import datetime
import Globals
import DBProcess as DBProcess
import Commonlib as Commonlib
import GetValue
# import ValueScripts.Cover_Page as Cover_Page
import os

def update_pos(table, cols, tab_idx, tab, begin_idx=0):
     cur_row = int((table[5].split(","))[0])
     cur_cell = int((table[5].split(","))[1])
     for i,col in enumerate(cols):
          # print(col[0],":",begin_idx,"/",i,":",str(tab_idx[tab]) , "," , str (cur_row) , "," , str(cur_cell))
          if i >= begin_idx:
               pos = str(tab_idx[tab]) + "," + str (cur_row) + "," + str(cur_cell)
               sql = "UPDATE `files` SET `File_Pos` = \"" + pos + "\" WHERE `File_ID` = " + str(col[0])
               DBProcess.excute_SQL(sql)
               step_row = int((col[5].split(","))[0])
               step_cell = int((col[5].split(","))[1])
               if step_row == 0 and step_cell == 0:
                    begin_idx = i+1
                    return begin_idx
               else:
                    cur_row = cur_row + step_row
                    cur_cell = cur_cell + step_cell


def getPos(table, cols):
     table_keys = table[4].split(",")
     template_id = Commonlib.get_template_id(Globals.TEMPLATE_TYPE)
     tab_idx = Commonlib.findTable(table_keys,template_id)
     print("table:",tab_idx)
     begin_idx = 0
     for idx in tab_idx:
          if idx not in Globals.SELECT_TABLES:
               Globals.SELECT_TABLES.append(idx)
     for tab in range(0,len(tab_idx)):
          if tab == 0:
               begin_idx = update_pos(table, cols, tab_idx, tab, 0)
          else:
               begin_idx = update_pos(table, cols, tab_idx, tab, begin_idx)

def adjustPath(table,path):
     adjust_path = []
    #  for p in path:
          
     return adjust_path

def get_file_list(path,table):
     file_list=[]
     if len(path) != 0:
          for p in path:
               files = os.listdir(p)
               for f in files:
                    file_list.append(os.path.join(p,f)) 

     if len(file_list) != 0:
          # print(file_list)
          adjust_path = adjustPath(table,file_list)
          print("get_file_list_adjust path:",adjust_path)
          if len(adjust_path) != 0:
               path = adjust_path
          else:
               return []
          # print("path:",path)
          return path
     else:
          return file_list

def save_pos_value(word):
     DBProcess.connectDB()
     Globals.TABLES = DBProcess.getTable(Globals.TYPELIST)
     DBProcess.close_all()
     
     for table in Globals.TABLES:
          DBProcess.connectDB()
          if table[0] > -1:
            #    try:
                    Globals.CURRENT_TABLE = table[1]
                    Globals.PATH_KEY = table[2]
                    print(table)
                    Globals.FIELDS = DBProcess.getFields(table[0])
                    getPos(table,Globals.FIELDS)

                    path = Commonlib.getPath(Globals.INPUT_PATH,table[2], Globals.ALL_FOLDER)
                    print(path)

                    Globals.CURRENT_TYPE = table[3]

                    print("Get Value Start:",datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                    for data in Globals.FIELDS:
                         if "Comment" in Globals.CURRENT_TABLE:
                              item = data[2].split(",")
                              Globals.ALL_KEYWORDS.append(item[0])
                         Globals.RESULT_DATA[str(data[0])] = "N/A"

                    if len(path) != 0:
                         GetValue.value_main(Globals.FIELDS,path)


                    print("Get Value End:",datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    print("------------------------------------------------------------------------------")
          DBProcess.close_all()
            #    except Exception as e:
            #         print("#############")
            #         print(e)
            #         print("#############")
            #         pass 