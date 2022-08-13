# File Name :GetValue.py
# Brief:
    # Functions about using Database
# Author: Sammi Guo
# Date:2021.07.12

import MySQLdb
import Globals
import Commonlib

def connectDB():
    conn=MySQLdb.connect(host="192.168.100.24",user="grlreport", passwd="grlreport", db="grl_sw", charset="utf8")
    cursor=conn.cursor()
    Globals.DATABASE_CONN=conn
    Globals.DATABASE_CURSOR=cursor
    # print("Connect End")

def excute_SQL(sql):
    Globals.DATABASE_CURSOR.execute(sql)
    returnList = list(Globals.DATABASE_CURSOR.fetchall())
    return returnList

def close_all():
    Globals.DATABASE_CURSOR.close()
    Globals.DATABASE_CONN.commit()
    Globals.DATABASE_CONN.close()

def getTable(TypeList):
    # port_cnt = int(TypeList[5])
    # sql="SELECT * FROM `testitems` WHERE `Type_ID` = 8";
    # sql="SELECT * FROM `testitems` WHERE `Type_ID` = 8  AND `Item_ID` in (857)"
    sql="SELECT * FROM `testitems` WHERE `Type_ID` = 8  and `Item_ID` BETWEEN 856 AND 859"
    relist = excute_SQL(sql)
    # print(relist)
    tables=[]
    del_tables = []
    get_table=True 
    
    for table in relist:
        get_table=True
        noteList = table[6].split('/')
        
        # print(table)
        if noteList[0] != Globals.PORT_NUM and noteList[0] != '':
            # print("not get:port number different")
            get_table=False
        
        if noteList[1] not in Globals.TEMPLATE_TYPE:
            # print("not get:not pd compliance")
            get_table=False
        
        for i in range(1,len(TypeList)):
            if noteList[i+2].strip() not in TypeList[i].strip() and noteList[i+2].strip()!='' and TypeList[i].strip() != '':
                # print("not get")
                # print(TypeList[i],":",noteList[i+2])
                get_table=False

        # # print(get_table)

        # if port_cnt != 4:
        #     for i,port in enumerate(port_name):
        #         if i >= port_cnt and port in table[1]:
        #             get_table=False
            
        if get_table is True:
            tables.append(table)
        # else:
        #     del_tables.append(table)

    # # print(del_tables)

        # tables.append(table)
    
    return tables
    # return tables,del_tables

def get_all_testItems():
    sql="SELECT * FROM `testitems` WHERE `Type_ID` = 8"
    relist = excute_SQL(sql)
    tables=[]
    for table in relist:
        tables.append(table)

    return tables
    
def getFields(table_idx):
    sql="SELECT * FROM `files` WHERE `Item_ID` = " + str(table_idx)
    relist = excute_SQL(sql)
    return relist

def get_select_result(select_col, table ,rule_col, target):
    sql = "SELECT " + select_col + "FROM " + table + " WHERE " + rule_col + "=" + target
    # print(sql)
    relist = excute_SQL(sql)
    
    return relist

 
