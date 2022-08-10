from docx.shared import RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import Globals
import DBProcess
import lib.word_lib as GRLWord
# import PAGE_BREAK
import Commonlib
from datetime import datetime

def setStyle(word, style):
    word.typeface=style[2]
    word.type=style[3]
    word.FONT=style[4]

    r = int((style[5].split(",")[0]))
    g = int((style[5].split(",")[1]))
    b = int((style[5].split(",")[2]))
    word.FONT_COLOR = RGBColor(r,g,b)
    
    word.width=style[6]
    word.high=style[7]
    
    if style[8] == "Center":
        word.alignment=WD_ALIGN_PARAGRAPH.CENTER
    elif style[8] == "Left":
        word.alignment=WD_ALIGN_PARAGRAPH.LEFT
    elif style[8] == "Right":
        word.alignment=WD_ALIGN_PARAGRAPH.RIGHT

    return word

# def deTables(word):
#     del_table = []
#     del_table_idx_db = []
#     tables = word.ww.tables

#     # # print(Globals.DELETE_TABLES)

#     for item in Globals.DELETE_TABLES:
#         table_idx = item[8].split(",")
#         for idx in table_idx:
#             del_table_idx_db.append(idx)
#     del_table_idx_db = list(set(del_table_idx_db))

#     # # print(del_table_idx_db)

#     for table in del_table_idx_db:
#         sql = "SELECT `Table_word_id` FROM `tables` WHERE `Table_ID` = " + str(table)
#         # # print(sql)
#         return_list = DBProcess.excute_SQL(sql)
#         del_table.append(return_list[0][0])

#     for idx in range(len(tables)-1,0,-1):
#         if idx in del_table and idx not in Globals.SELECT_TABLES:
#             word.deletable(idx)

#     word = PAGE_BREAK.delete_blank_page_USB_Report_only(word)

#     return word

# def delete_rows(word):
#     deleted_rows = {} 
#     current_table_idx = 0
#     for idx in Globals.DELETE_IDX:
#         sql = "SELECT `File_ID`,`File_Pos`,`Style_ID` FROM `files` WHERE `File_ID`=" + str(idx)
#         sql_result = DBProcess.excute_SQL(sql)
#         if len(sql_result) == 1:
#             pos = sql_result[0][1].split(",")
#             # # print(int(idx),",",pos)
#             table_idx = pos[0]
#             if current_table_idx != table_idx:
#                 current_table_idx = table_idx
#                 deleted_rows[str(current_table_idx)] = []

#             row = pos[1]
#             deleted_rows[str(current_table_idx)].append(int(row))
            

#     for idx in deleted_rows:
#         unique_set = set(deleted_rows[idx])
#         unique_list = list(unique_set)
#         unique_list.sort(reverse = True)
#         # # print(idx,":",unique_list)
#         for row in unique_list:
#             word.delerow(int(idx),int(row))
    
#     return word
       

def updateWord(word):
    for idx in Globals.RESULT_DATA:
        sql = "SELECT `File_ID`,`File_Pos`,`Style_ID`, `File_Name`, `Item_ID` FROM `files` WHERE `File_ID`=" + str(idx)
        # # print(sql)
        sql_result = DBProcess.excute_SQL(sql)
        # # print("sql result:",sql_result)

        if len(sql_result) == 1:
            
            pos = sql_result[0][1].split(",")
            # # print(int(idx),",",pos)
            table_idx = pos[0]
            row = pos[1]
            col = pos[2]

            sql = "SELECT `Item_Name` FROM `testitems` WHERE `Item_ID`=" + str(sql_result[0][4])
            item_name = (DBProcess.excute_SQL(sql))[0][0]
            result = Globals.RESULT_DATA[idx]

            # # print(int(table_idx),",", int(row),",", int(col),":",result)

            # # print(int(table_idx),",", item_name)

            style_sql=""
            if result == "N/A" and "Cover" not in item_name:
                style_sql="SELECT * FROM `style` WHERE `Style_ID`= 50"
            elif result == "PASS":
                style_sql = "SELECT * FROM `style` WHERE `Style_ID`=48"
            elif result == "FAIL":
                style_sql = "SELECT * FROM `style` WHERE `Style_ID`= 49"
            else:
                style_sql = "SELECT * FROM `style` WHERE `Style_ID`="+str(sql_result[0][2])
            
            style = DBProcess.excute_SQL(style_sql)
            word = setStyle(word,style[0])

            if "Cover" in item_name:
                if result == "PASS" or result == "FAIL" or result == "N/A":
                        word.alignment=WD_ALIGN_PARAGRAPH.LEFT
                        word.FONT=12
            
            # if table need to insert image not value 
                # image type support :png PNG jpg JPG
            result_lower = str(result).lower()
            if "png" in result_lower or "jpg" in result_lower: 
                # write png
                word.InsertPNGtoWord(int(table_idx), int(row), int(col),[result])   
            else:
                # # print("not image")
                # N/A PASS,N/A FAIL
                if "USB Power Delivery Compliance Test Merged" in item_name:
                    if "Comment" in item_name:
                        # print("Comment")
                        # print(int(table_idx),",", int(row),",", int(col),":",result)
                        # print(idx,":",word.Get_CellValue(int(table_idx), int(row), int(col)))
                        
                        if result == "N/A":
                                continue
                        elif word.Get_CellValue(int(table_idx), int(row), int(col)) == "":
                             word.WritevValuetoTable(int(table_idx), int(row), int(col), str(result))
                        elif word.Get_CellValue(int(table_idx), int(row), int(col)) == "N/A":
                            continue
                        elif word.Get_CellValue(int(table_idx), int(row), int(col)) != "" and str(result)!= "":
                            value = word.Get_CellValue(int(table_idx), int(row), int(col)) + "\n" + str(result)
                            word.WritevValuetoTable(int(table_idx), int(row), int(col), str(value))
                    else:
                        # # print(idx,":",word.Get_CellValue(int(table_idx), int(row), int(col)),"V.S",str(result))
                        if word.Get_CellValue(int(table_idx), int(row), int(col)) == str(result):
                            continue
                        elif word.Get_CellValue(int(table_idx), int(row), int(col)) == "N/A" and str(result)=="PASS":
                            # # print("Writing PASS")
                            word.WritevValuetoTable(int(table_idx), int(row), int(col), str(result))
                            # # print(word.Get_CellValue(int(table_idx), int(row), int(col)))
                        elif word.Get_CellValue(int(table_idx), int(row), int(col)) == "N/A" and str(result)=="FAIL":
                            # # print("Origin NA Writing FAIL")
                            word.WritevValuetoTable(int(table_idx), int(row), int(col), str(result))
                            # # print(word.Get_CellValue(int(table_idx), int(row), int(col)))
                        elif word.Get_CellValue(int(table_idx), int(row), int(col)) == "PASS" and str(result)=="N/A":
                            continue
                        elif word.Get_CellValue(int(table_idx), int(row), int(col)) == "PASS" and str(result)=="FAIL":
                            # # print("Origin PASS Writing FAIL")
                            word.WritevValuetoTable(int(table_idx), int(row), int(col), str(result))
                            # # print(word.Get_CellValue(int(table_idx), int(row), int(col)))
                        elif word.Get_CellValue(int(table_idx), int(row), int(col)) == "FAIL" and str(result)=="PASS":
                            continue
                        elif word.Get_CellValue(int(table_idx), int(row), int(col)) == "FAIL" and str(result)=="N/A":
                            continue
                        else:
                            # # print("Writing Value")
                            word.WritevValuetoTable(int(table_idx), int(row), int(col), str(result))
                            # # print(word.Get_CellValue(int(table_idx), int(row), int(col)))

                        # # print("========================================================================================")
                
                elif "Comment" in item_name:
                    # # print("Comment")
                    if word.Get_CellValue(int(table_idx), int(row), int(col)) == "":
                        if result == "N/A":
                            # # print("no update")
                            continue
                        else:
                            word.WritevValuetoTable(int(table_idx), int(row), int(col), str(result))
                    else:
                        if result == "N/A":
                            # # print("no update")
                            continue
                        else:
                            word.WritevValuetoTable(int(table_idx), int(row), int(col), str(result))
                
                else:
                    word.WritevValuetoTable(int(table_idx), int(row), int(col), str(result))



    # # print("Delete row:",datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # word = delete_rows(word)
    # # print("Delete Tables:",datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # word = deTables(word)
    
    # print("Save file:",datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    word.SaveAs(Globals.REPORT_NAME)
    return
