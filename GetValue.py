import Globals
import Commonlib as Commonlib
import lib.Excel_lib as GRL_Excel
import ValueScripts.HtmlValue as HtmlValue
from bs4 import BeautifulSoup
# import ValueScripts.TxtValue as TxtValue
# import ValueScripts.CSVValue as CSVValue
# import ValueScripts.ExcelValue as ExcelValue
# import ValueScripts.SpecialValue as SpecialValue

def value_main(data_list,path):
    current_sheet = ""

    for data in data_list:
        # if data[0] == 55628:
            print(data[0],":",data[1])
            # reload = False
            file_list = []
            # sheet=""

            # # ======= [Get Files] ======= 
            if "/" in data[1]:
                key_words = data[1].split("/")
                p = path[0]
                path_key = Globals.PATH_KEY
                for kw_idx in range(0,len(key_words)-1):
                    path_key = path_key + "/" + key_words[kw_idx]

                # print(path_key)

                input_path = Commonlib.getPath(Globals.INPUT_PATH,path_key,Globals.ALL_FOLDER)
                # print(input_path)
                for ip in input_path:
                    files = Commonlib.getTargetFile(ip,key_words[len(key_words)-1],Globals.CURRENT_TYPE)
                    for f in files:
                        file_list.append(f)
                # print(file_list)
            elif len(path) > 1:
                for p in path:
                    files = Commonlib.getTargetFile(p,data[1],Globals.CURRENT_TYPE)
                    if len(files) != 0:
                        for f in files:
                            file_list.append(f)
            else:
                file_list = Commonlib.getTargetFile(path[0],data[1],Globals.CURRENT_TYPE)
            # if "[" not in data[1] and "]" not in data[1]:
            #     if "/" in data[1] and Globals.CURRENT_TYPE != "XLSX":
            #         keys = data[1].split("/")
            #         for p in path:
            #             if keys[0] in p:
            #                 files = Commonlib.getTargetFile(p,keys[1],Globals.CURRENT_TYPE)
            #                 if len(files) != 0:
            #                     for f in files:
            #                         file_list.append(f)
            #     elif len(path) == 1 and Globals.CURRENT_TYPE == "XLSX":
            #         file_key = (data[1].split("/"))[0]
            #         sheet = (data[1].split("/"))[1]
            #         files = Commonlib.getTargetFile(path[0],file_key,Globals.CURRENT_TYPE)
            #         if len(files) == 1:
            #             for f in files:
            #                 file_list.append(f)
            #     elif ";" in data[1] and len(path) == 1:
            #         keylist = data[1].split(";")
            #         for key in keylist:
            #             files =  Commonlib.getTargetFile(path[0],key,Globals.CURRENT_TYPE)
            #             if len(files) != 0:
            #                 for f in files:
            #                     file_list.append(f)
                
            for file in file_list:
                print("file:",file)
                # print("Global:",Globals.DATA_FILE)

            #     # ======= [SETTING　DATAFILE] =======
            #         # Setting Globals.DATA_FILE to avoiding reload file_list (reduce excuting time) 

            #     if Globals.CURRENT_TYPE == "XLSX":
            #         if current_sheet != sheet or Globals.DATA_FILE != file_list:
            #             # print("Reload excel")
            #             if len(file_list) > 0:
            #                 Globals.DATA_FILE = file_list
            #                 Globals.EXCEL_FILE = GRL_Excel.GetExcel(r''+file_list[0], sheet)
            #                 current_sheet = sheet
            if Globals.DATA_FILE != file_list:
                # print("Reload data")
                reload = True
                Globals.DATA_FILE = file_list 
                Globals.SOUP_LIST.clear()
            else:
                reload = False

            # # ======= [Initialize all fields] =======

            # if "[Scope of Testing Content]" == data[1]:
            #     continue
            # else:
            #     Globals.RESULT_DATA[str(data[0])] = "N/A"


            # # ======= [Getting Value] =======
            if len(file_list) != 0:
                # print("in")
                if Globals.CURRENT_TYPE == "HTML":
                    soup_list = []
                    if reload == True:
                        for file in file_list:
                            with open(file, 'r', encoding='utf-8') as f:
                                html_doc = f.read()
                            soup = BeautifulSoup(html_doc, 'html.parser')    
                            Globals.SOUP_LIST.append(soup)
                    HtmlValue.get_html_value(data)
           
            #     elif Globals.CURRENT_TYPE == "TXT":
            #         TxtValue.get_value(data,file_list)
            #     elif Globals.CURRENT_TYPE == "CSV":
            #         CSVValue.getValue(data,file_list)
            #     elif Globals.CURRENT_TYPE == "XLSX":
            #         ExcelValue.get_value_excel(data,Globals.EXCEL_FILE)
            #     elif Globals.CURRENT_TYPE == "IMAGE":
            #         # print(file)
            #         if len(file_list) == 1:
            #             Globals.RESULT_DATA[str(data[0])] = file_list[0]
            # else:
            #     if "[" in data[1] and "]" in data[1]:
            #         SpecialValue.get_value(data)
            #     elif "Thunderbolt DUT Appearance Cover" in Globals.CURRENT_TABLE:
            #         Globals.RESULT_DATA[str(data[0])] = ""
            #     elif "Sideband" in Globals.CURRENT_TABLE:
            #         # print("in")
            #         Globals.RESULT_DATA[str(data[0])] = ""
            #     else:
            #         continue

            print("=====================================================================")

