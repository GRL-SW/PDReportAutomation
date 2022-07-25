import sys
# sys.path.append("..")
import Globals
import DBProcess
import MySQLdb
import Commonlib
import lib.word_lib as GRLWord
from datetime import datetime

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


def save_table_content(word,template_id):
    tables = word.ww.tables
    for i,table in enumerate(tables):
        text_list=[]
        print(i)
        max_col=0
        if i == 14:
            for r in range(0, len(table.rows)):
                for c in range(0, len(table.rows[r].cells)):
                    print(r,",",c,":",table.cell(r,c).text)
                # if r == 0:
                #     # sql="INSERT INTO `tables` (`Table_ID`,`Globals.CURRENT_TABLE`,`Template_ID`) VALUES ("+str(10000+i)+",\""+table.cell(0,0).text+"\",1)"
                #     sql="INSERT INTO `tables` (`Table_Name`,`Table_word_id`,`Template_ID`) VALUES (\""+table.cell(0,0).text+"\","+str(i) + "," + str(template_id) +")"
                #     DBProcess.excute_SQL(sql)

                #     sql="SELECT * FROM `tables` ORDER BY `Table_ID` DESC LIMIT 0 , 1"
                    
                #     id = ((DBProcess.excute_SQL(sql))[0])[0]

                # if len(table.rows[r].cells) > max_col:
                #     max_col = len(table.rows[r].cells)

                
                # if r < 10:
                #     for c in range(0, len(table.rows[r].cells)):
                #         if c < 10:
                #         # print(table.cell(r,c).text)
                #             if table.cell(r,c).text != "":
                #                 text_list.append(table.cell(r,c).text)

        # text = ','.join(text_list)
        # sql="INSERT INTO `content` (`Content_Text`, `Content_Row`, `Content_Col`, `Table_ID`) VALUES (\"" + text + "\"," + str(len(table.rows)) + "," + str(max_col) + "," + str(id) + ")"
        # DBProcess.excute_SQL(sql)
        # text_list.clear()
        print("=======================================================")

def del_old_data(template_ID):
    select_table_sql="SELECT `Table_ID` FROM `Tables` WHERE `Template_ID`=" + str(template_ID)
    table_id_list = DBProcess.excute_SQL(select_table_sql)
    for i in range(0,len(table_id_list)):
        delete_sql = "DELETE FROM `Content` WHERE `Table_ID` = " + str(table_id_list[i][0])
        DBProcess.excute_SQL(delete_sql)
    delete_tables="DELETE FROM `Tables` WHERE `Template_ID`="  + str(template_ID)
    DBProcess.excute_SQL(delete_tables)
    return

def add_tab(template_id):
    item_list = DBProcess.getTable(Globals.TYPELIST)
    for item in item_list:
        print(item)
        table_keys = item[4].split(",")
        tab_idx = Commonlib.findTable(table_keys,template_id)
        print(tab_idx)
        table_id = []
        # tab_str = ",".join(tab_idx)
        for idx in tab_idx:
            sql = "SELECT `Table_ID` FROM `tables` WHERE `Table_word_id` = " + str(idx) + " and `Template_ID` = " + str(template_id)
            re_list = DBProcess.excute_SQL(sql)
            table_id.append(str(re_list[0][0]))

        cols = DBProcess.getFields(item[0])

        for tab in range(0,len(tab_idx)):
          if tab == 0:
               begin_idx = update_pos(item, cols, tab_idx, tab, 0)
          else:
               begin_idx = update_pos(item, cols, tab_idx, tab, begin_idx)

        tab_str = ",".join(table_id)    
        sql = "UPDATE `testitems` SET `Table_ID` = \"" + tab_str + "\" WHERE `Item_ID` = " + str(item[0])
        DBProcess.excute_SQL(sql)



if __name__ == '__main__':
    Globals.initialize(sys.argv)
    
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    template_id = Commonlib.get_template_id(Globals.TEMPLATE_TYPE)
    print(template_id)
    DBProcess.connectDB()
    # del_old_data(template_id)
    DBProcess.close_all()

    word = GRLWord.Get_word(Globals.TEMPLATE_WORD_NAME)
    DBProcess.connectDB()
    save_table_content(word,template_id)
    # add_tab(template_id)
    DBProcess.close_all()

    # DBProcess.connectDB()
    # item_list = DBProcess.getTable(Globals.TYPELIST)
    # # for item in item_list:
    # #     print(item)
    # DBProcess.close_all()
    
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))