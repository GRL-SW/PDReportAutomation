import Globals
from bs4 import BeautifulSoup
import Commonlib

def adjust_value(data,value):
    value_list = value.split(" ")
    if len(value_list) == 2:
        # print(value_list[1].encode('utf-8'))
        # print(value_list[0],":",value_list[1],"/",data[6])
        if value_list[1].strip() == data[6]:
            return format(float(value_list[0]), '.2f')
        elif "μ" in data[6] and "u" in value_list[1]:
            if "ppm" in data[6]:
                adj_value = Commonlib.adjustValueUnit(str(value_list[0]).strip(), value_list[1].strip(),data[6].strip())
                return adj_value
            else:
                return format(float(value_list[0]), '.2f')
        else:
            # print("transfering...")
            adj_value = Commonlib.adjustValueUnit(str(value_list[0]).strip(), value_list[1].strip(),data[6].strip())
            return adj_value
            # print("adjvalue:",adj_value)
    else:
        if "Hits" in data[6]:
            # print("Hits in data")
            print(value_list[0])
            return format(float(value_list[0]), '.0f')
        else:
            return value


def get_value(data,file):
    print(file[0])
    next_data =None
    keys = data[2].split(",")

    if str(file[0]) == "None":
        return
    else:
        with open(file[0], 'r', encoding='utf-8') as f:
            html_doc = f.read()
        
        soup = BeautifulSoup(html_doc, 'html.parser')
        lines = soup.find_all('ul')[0].find_all('li')

        text_list = []

        for li in lines:
            li_text = (li.text).split('\n')
            for text in li_text:
                if text not in text_list:
                    text_list.append(text)

        for text in text_list:
            if len(keys) == 2:
                # find the value of inrush current
                if keys[1] in text:
                    value = ((text.split(keys[1]))[1]).strip()
                    value = adjust_value(data,value)
                    print("length 2:",value)
                    Globals.RESULT_DATA[str(data[0])] = value
            # find the value of result
            elif len(keys) == 3:
                if keys[2] in text:
                    value = ((text.split(keys[2]))[1]).strip()
                    value = value.upper()
                    print("length 3:",value)
                    if "PASS" in value:
                        Globals.RESULT_DATA[str(data[0])] = "PASS"
                    else:
                        Globals.RESULT_DATA[str(data[0])] = "FAIL"
        return next_data