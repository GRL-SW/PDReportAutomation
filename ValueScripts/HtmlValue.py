# File Name : HtmlValue.py
# Brief:
    # get value for raw data type of HTML
# Author: Sammi Guo
# Date:2021.06.15

import Globals
from bs4 import BeautifulSoup
import ItemScripts.EllisysFunctions as EllisysFunctions
import ItemScripts.LecroyFunctions as LecroyFunctions
import ItemScripts.C2Functions as C2Functions
import ItemScripts.MQPFunctions as MQPFunctions
import ItemScripts.Inrush as Inrush

def get_html_value(data):
    
    if "Ellisys Explorer" in Globals.CURRENT_TABLE:
        EllisysFunctions.get_value(data,Globals.DATA_FILE,Globals.SOUP_LIST)
    elif "Lecroy" in Globals.CURRENT_TABLE:
        LecroyFunctions.get_value(data,Globals.DATA_FILE)
    elif "C2" in Globals.CURRENT_TABLE:
        C2Functions.get_value(data,Globals.SOUP_LIST)
    elif "MQP" in Globals.CURRENT_TABLE:
        MQPFunctions.get_value(data,Globals.DATA_FILE,Globals.SOUP_LIST)
    elif "Inrush" in Globals.CURRENT_TABLE:
        Inrush.get_value(data,Globals.DATA_FILE)

    return