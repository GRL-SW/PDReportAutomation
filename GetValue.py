import Globals
import Commonlib as Commonlib
import ValueScripts.HtmlValue as HtmlValue
import ValueScripts.PetrptValue as PetrptValue
from bs4 import BeautifulSoup

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

                print(path_key)

                input_path = Commonlib.getPath(Globals.INPUT_PATH,path_key,Globals.ALL_FOLDER)
                print(input_path)
                for ip in input_path:
                    files = Commonlib.getTargetFile(ip,key_words[len(key_words)-1],Globals.CURRENT_TYPE)
                    print(files)
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
                
            # for file in file_list:
            #     print("file:",file)
            #     print("Global:",Globals.DATA_FILE)

            if Globals.DATA_FILE != file_list:
                # print("Reload data")
                reload = True
                Globals.DATA_FILE = file_list 
                Globals.SOUP_LIST.clear()
            else:
                reload = False

            # # ======= [Getting Value] =======
            if len(file_list) != 0:
                # print("in")
                if Globals.CURRENT_TYPE == "HTML":
                    if reload == True:
                        for file in file_list:
                            with open(file, 'rb') as f:
                                html_doc = f.read()
                            soup = BeautifulSoup(html_doc, 'html.parser')    
                            Globals.SOUP_LIST.append(soup)
                    HtmlValue.get_html_value(data)
           
                elif Globals.CURRENT_TYPE == "PETRPT":
                    PetrptValue.get_value(data,file_list)

            print("=====================================================================")

