import Globals
from datetime import datetime
import datetime
import DBProcess

Month_dic_detail = {"01":"January","02":"February","03":"March","04":"April","05":"May","06":"June",
                    "07":"July","08":"Augest","09":"September","10":"October","11":"November","12":"December"}

Month_dic_simply = {"01":"Jan","02":"Feb","03":"March","04":"April","05":"May","06":"June",
                    "07":"July","08":"Aug","09":"Sep","10":"Oct","11":"Nov","12":"Dec"}

def getValue(data_list):
    for data in data_list:
        Globals.RESULT_DATA[str(data[0])] = "N/A"
        if data[1] == "[Subtitle]":
            if "PreCompliance" in Globals.REPORT_INFO[11]:
                Globals.RESULT_DATA[str(data[0])] = "Pre-Compliance Test Report"
            elif  "Compliance" in Globals.REPORT_INFO[11]:
                Globals.RESULT_DATA[str(data[0])] = "Compliance Test Report"
        elif data[1] == "[Review Date]":
            date_time_str = datetime.datetime.strptime(Globals.REPORT_INFO[13], "%Y/%m/%d")
            new_date = date_time_str + datetime.timedelta(days=2)
            review_date_tmp = str(new_date.strftime('%m %d,%Y'))
            day_year = (review_date_tmp.split(" "))[1]
            month = (review_date_tmp.split(" "))[0]
            review_date = Month_dic_detail[month] + " " + day_year
            print("new:",review_date)
            Globals.RESULT_DATA[str(data[0])] = review_date

        elif data[1] == "[Project Number]":
            Globals.RESULT_DATA[str(data[0])] = Globals.REPORT_INFO[1]

        elif data[1] == "[Customer Company]":
            Globals.RESULT_DATA[str(data[0])] = Globals.REPORT_INFO[2]
        
        elif data[1] == "[Customer Name and Mail]":
            Globals.RESULT_DATA[str(data[0])] = Globals.REPORT_INFO[3] + '\n' + Globals.REPORT_INFO[4]

        elif data[1] == "[Product Name]":
            Globals.RESULT_DATA[str(data[0])] = Globals.REPORT_INFO[5]

        elif data[1] == "[Product Description]":
            Globals.RESULT_DATA[str(data[0])] = "PD 3.1" + Globals.REPORT_INFO[6]

        elif data[1] == "[Product Type]":
            if "DRP" in data[1]:
                Globals.RESULT_DATA[str(data[0])] = "USB Type-C DRP"
            else:
                Globals.RESULT_DATA[str(data[0])] = Globals.REPORT_INFO[7]
        elif data[1] == "[TID]":
            Globals.RESULT_DATA[str(data[0])] = Globals.REPORT_INFO[8]
        elif data[1] == "[VID]":
            Globals.RESULT_DATA[str(data[0])] = Globals.REPORT_INFO[9]
        elif data[1] == "[PID]":
            Globals.RESULT_DATA[str(data[0])] = Globals.REPORT_INFO[10]
        elif data[1] == "[Test Requirement]":
            if "PreCompliance" in Globals.REPORT_INFO[11]:
                Globals.RESULT_DATA[str(data[0])] = "PD3.1 Pre-Compliance Tests"
            elif  "Compliance" in Globals.REPORT_INFO[11]:
                Globals.RESULT_DATA[str(data[0])] = "PD3.1 Compliance Tests"
        elif data[1] == "[Test Result]":
            pass
        elif data[1] == "[Receive Date]":
            Globals.RESULT_DATA[str(data[0])] = Globals.REPORT_INFO[12]
        elif data[1] == "[Test Completion date]":
            Globals.RESULT_DATA[str(data[0])] = Globals.REPORT_INFO[13]
        elif data[1] == "[Test engineer]":
            rule = "\"" + Globals.REPORT_INFO[0] + "\""
            re_list = DBProcess.get_select_result("*","member","Member_Name",rule)
            print(re_list[0][4])
            Globals.RESULT_DATA[str(data[0])] = re_list[0][4]