# File Name : Globals.py
# Brief:
    # initialize: initialize all global values using by main.py
# Author: Sammi Guo
# Date:2021.05.17

import os
import sys
import json
from datetime import datetime

# initialize:
    # TABLES: all tables of usb test in database
    # TEMPLATE_WORD_NAME: default word file
    # TYPELIST:user input from website
        # TYPELIST[0]: Port Number
        # TYPELIST[1]: Equipment for Type-C Functional Test 

def initialize(param):
    
    if param[len(param) - 1] != "START_TIME":
        start_time = param[len(param) - 1]
    else:
        start_time = datetime.now().strftime('_%Y%m%d_%H%M%S')
    # print("report_info:",report_info)

    global ALL_FOLDER
    global INPUT_PATH
    global OUTPUT_FILE 
    global FINAL_PATH
    global REPORT_NAME
    global PROJECT_NAME
    global TYPELIST
    global TEMPLATE_TYPE
    global PORT_NUM
    global TEMPLATE_WORD_NAME
    global TABLES
    global CURRENT_TABLE
    global CURRENT_TYPE
    global FIELDS
    global RESULT_DATA
    global DATA_FILE
    global SELECT_TABLES
    global REPORT_NAME
    global ALL_KEYWORDS
    global MERGED_UPDC
    global PATH_KEY
    global SOUP_LIST

    ALL_FOLDER = {}
    RESULT_DATA = {}
    INPUT_PATH = param[1]
    FINAL_PATH = param[2]
    PROJECT_NAME = param[3]
    TEMPLATE_TYPE = param[4]
    PORT_NUM = param[5]
    TYPELIST = param[6].split("%")
    TEMPLATE_WORD_NAME = "\\\\192.168.2.104\\Public\\Software\\07_PDReportAutomation\\pd compliance new\\blank template\\" + TEMPLATE_TYPE
    DATA_FILE = []
    SELECT_TABLES = []
    ALL_KEYWORDS = []
    PATH_KEY = ""
    SOUP_LIST = []

    MERGED_UPDC = {
        "TEST.PD.PHY.ALL.1 Transmit Bit Rate and the Drift":"",
        "TEST.PD.PHY.ALL.2 Transmitter Eye Diagram":"",
        "TEST.PD.PHY.ALL.3 Collision Avoidance":"",
        "TEST.PD.PHY.ALL.4 Bus Idle Detection":"",
        "TEST.PD.PHY.ALL.5 Receiver Interference Rejection":"",
        "TEST.PD.PHY.ALL.6 Invalid SOP*":"",
        "TEST.PD.PHY.ALL.7 Valid SOP*":"",
        "TEST.PD.PHY.ALL.8 Incorrect CRC":"",
        "TEST.PD.PHY.ALL.9 Receiver Input Impedance":"",
        "TEST.PD.PROT.ALL.1 Corrupted GoodCRC":"",
        "TEST.PD.PROT.ALL.2 Soft Reset and Hard Reset":"",
        "TEST.PD.PROT.ALL.3 Soft Reset response":"",
        "TEST.PD.PROT.ALL.4 Reset Signals and MessageID":"",
        "TEST.PD.PROT.ALL.5 Unrecognized Message":"",
        "TEST.PD.PROT.ALL3.1 Get_Status Response":"",
        "TEST.PD.PROT.ALL3.2 Get_Manufacturer_Info Response":"",
        "TEST.PD.PROT.ALL3.3 Invalid Manufacturer Info Target":"",
        "TEST.PD.PROT.ALL3.4 Invalid Manufacturer Info Ref":"",
        "TEST.PD.PROT.ALL3.5 Chunked Extended Message Response":"",
        "TEST.PD.PROT.ALL3.6 ChunkSenderResponseTimer Timeout":"",
        "TEST.PD.PROT.ALL3.7 Security Messages Supported":"",
        "TEST.PD.PROT.PORT3.1 Get Battery Status Response":"",
        "TEST.PD.PROT.PORT3.2 Invalid Battery Status":"",
        "TEST.PD.PROT.PORT3.3 Get Battery Cap Response":"",
        "TEST.PD.PROT.PORT3.4 Invalid Battery Capabilities Reference":"",
        "TEST.PD.PROT.PORT3.5 Get Country Codes Response":"",
        "TEST.PD.PROT.PORT3.6 Get Country Info Response":"",
        "TEST.PD.PROT.PORT3.7 Unchunked Extended Message Supported":"",
        "TEST.PD.PROT.SRC.1 Get_Source_Cap Response":"",
        "TEST.PD.PROT.SRC.2 Get_Source_Cap No Request":"",
        "TEST.PD.PROT.SRC.3 Sender Response Timer Deadline":"",
        "TEST.PD.PROT.SRC.4 Reject Request":"",
        "TEST.PD.PROT.SRC.5 Reject Request Invalid Object Position":"",
        "TEST.PD.PROT.SRC.6 Atomic Message Sequence – Request":"",
        "TEST.PD.PROT.SRC.7 DR_Swap":"",
        "TEST.PD.PROT.SRC.8 VCONN_Swap Response":"",
        "TEST.PD.PROT.SRC.9 PR_Swap Response":"",
        "TEST.PD.PROT.SRC.10 PR_Swap – PSSourceOnTimer Timeout":"",
        "TEST.PD.PROT.SRC.11 Unexpected Message Received in Ready State":"",
        "TEST.PD.PROT.SRC.12 Get_Sink_Cap Response":"",
        "TEST.PD.PROT.SRC.13 PR Swap GoodCRC not sent in Response to PS_RDY":"",
        "TEST.PD.PROT.SRC3.1 SourceCapabilityTimer Timeout":"",
        "TEST.PD.PROT.SRC3.2 SenderResponseTimer Timeout":"",
        "TEST.PD.PROT.SRC3.3 Get_Source_Cap_Extended Response":"",
        "TEST.PD.PROT.SRC3.4 Alert Response Source Input Change":"",
        "TEST.PD.PROT.SRC3.5 Alert Response Battery Status Change":"",
        "TEST.PD.PROT.SRC3.6 Soft_Reset Sent when SinkTxOK":"",
        "TEST.PD.PROT.SRC3.7 Get_PPS_Status Response":"",
        "TEST.PD.PROT.SRC3.8 SourcePPSCommTimer Deadline":"",
        "TEST.PD.PROT.SRC3.9 SourcePPSCommTimer Timeout":"",
        "TEST.PD.PROT.SRC3.10 SourcePPSCommTimer Stopped":"",
        "TEST.PD.PROT.SRC3.11 GoodCRC Specification Revision Compatibility":"",
        "TEST.PD.PROT.SRC3.12 FR Swap Without Signaling":"",
        "TEST.PD.PROT.SRC3.13 Cable Type Detection":"",
        "TEST.PD.PROT.SNK.1 Get_Sink_Cap Response":"",
        "TEST.PD.PROT.SNK.2 Get_Source_Cap Response":"",
        "TEST.PD.PROT.SNK.3 SinkWaitCapTimer Deadline":"",
        "TEST.PD.PROT.SNK.4 SinkWaitCapTimer Timeout":"",
        "TEST.PD.PROT.SNK.5 SenderResponseTimer Deadline":"",
        "TEST.PD.PROT.SNK.6 SenderResponseTimer Timeout":"",
        "TEST.PD.PROT.SNK.7 PSTransitionTimer Timeout":"",
        "TEST.PD.PROT.SNK.8 Atomic Message Sequence – Accept":"",
        "TEST.PD.PROT.SNK.9 Atomic Message Sequence – PS_RDY":"",
        "TEST.PD.PROT.SNK.10 DR_Swap Request":"",
        "TEST.PD.PROT.SNK.11 VCONN_Swap Request":"",
        "TEST.PD.PROT.SNK.12 PR_Swap – PSSourceOffTimer Timeout":"",
        "TEST.PD.PROT.SNK.13 PR_Swap – Request SenderResponseTimer Timeout":"",
        "TEST.PD.PROT.SNK.14 Valid Use of GoodCRC on Power up":"",
        "TEST.PD.PROT.SNK3.1 Get_Source_Cap_Extended":"",
        "TEST.PD.PROT.SNK3.2 Alert Response Source Input Change":"",
        "TEST.PD.PROT.SNK3.3 Alert Response Battery Status Change":"",
        "TEST.PD.PROT.SNK3.4 Soft_Reset Sent Regardless of Rp Value":"",
        "TEST.PD.PROT.SNK3.5 Sink PPS Normal Operation":"",
        "TEST.PD.PROT.SNK3.6 Revision Number Test":"",
        "TEST.PD.PROT.SNK.3.7 GoodCRC Specification Revision Compatibility":"",
        "TEST.PD.VDM.SRC.1 Discovery Process and Enter Mode":"",
        "TEST.PD.VDM.SRC.2 Invalid Fields – Discover Identity":"",
        "TEST.PD.VDM.SNK.1 Discovery Process and Enter Mode":"",
        "TEST.PD.VDM.SNK.2 Exit Mode without Entering":"",
        "TEST.PD.VDM.SNK.3 Interruption by PD Message":"",
        "TEST.PD.VDM.SNK.4 Interruption by VDM Message":"",
        "TEST.PD.VDM.SNK.5 DR Swap in Modal Operation":"",
        "TEST.PD.VDM.SNK.6 Structured VDM Revision Number Test":"",
        "TEST.PD.VDM.SNK.7 Unrecognized VID in Unstructured VDM":"",
        "TEST.PD.VDM.CBL.1 Discovery Process and Enter Mode":"",
        "TEST.PD.VDM.CBL3.1 Revision Number Test":"",
        "TEST.PD.PS.SRC.1 Multiple Request Messages":"",
        "TEST.PD.PS.SRC.2 PDO Transition":"",
        "TEST.PD.PS.SRC.3 Initial Source PDO Transition":"",
        "TEST.PD.PS.SNK.1 PDO Transition":"",
        "TEST.PD.PS.SNK.2 Initial Sink PDO Transition":"",
        "TEST.PD.PS.SNK.3 Multiple Request Load Test Post PRSwap":"",
        "COMMON.CHECK.PD.1 Check Preamble":"",
        "COMMON.CHECK.PD.2 Check Message Header":"",
        "COMMON.CHECK.PD.3 Check GoodCRC":"",
        "COMMON.CHECK.PD.4 Check Atomic Message Sequence":"",
        "COMMON.CHECK.PD.5 Check Unexpected Messages and Signals":"",
        "COMMON.CHECK.PD.6 Check Control Message":"",
        "COMMON.CHECK.PD.7 Check Source Capabilities Message":"",
        "COMMON.CHECK.PD.8 Check Request Message":"",
        "COMMON.CHECK.PD.9 Check Structured VDM Message":"",
        "COMMON.CHECK.PD.10 Check Extended Message Header":"",
        "COMMON.CHECK.PD.11 Check Source Capabilities Extended Message":"",
        "COMMON.CHECK.PD.12 Check Sink Capabilities Message":"",
        "COMMON.CHECK.PD.13 Check Correct Use of Rp":"",
        "COMMON.CHECK.PD3.1 Check EPR_Request Message":"",
        "COMMON.CHECK.PD3.2 Check EPR_Mode Message":"",
        "COMMON.CHECK.PD3.3 Check EPR_Source_Capabilities Message":"",
        "COMMON.CHECK.PD3.4 Check EPR_Sink_Capabilities Message":"",
        "COMMON.PROC.PD.1 Tester Sends GoodCRC":"",
        "COMMON.PROC.PD.2 UUT Sent Get_Source_Cap":"",
        "COMMON.PROC.PD.3 UUT Sent Get_Sink_Cap":"",
        "COMMON.PROC.PD.4 UUT Sent Ping":"",
        "COMMON.PROC.PD.5 UUT Sent PR_Swap":"",
        "COMMON.PROC.PD.6 UUT Sent VCONN_Swap":"",
        "COMMON.PROC.PD.7 UUT Sent Discover Identity Request":"",
        "COMMON.PROC.PD.8 UUT Sent Discover SVIDs Request":"",
        "COMMON.PROC.PD.9 UUT Sent Attention":"",
        "COMMON.PROC.PD.10 UUT Sent Request":"",
        "COMMON.PROC.PD.11 UUT Sent Source Capabilities":"",
        "COMMON.PROC.PD.12 UUT Sent DR_Swap":"",
        "COMMON.PROC.PD.17 Tester Sent Vconn_swap message":"",
        "COMMON.PROC.PD3.1 Sink Start an AMS":"",
        "COMMON.PROC.PD3.2 UUT Sent EPR_Source_Cap message":"",
        "COMMON.PROC.PD3.3 UUT Sent EPR_Get_Source_Cap":"",
        "COMMON.PROC.PD3.4 UUT Sent EPR_Request":"",
        "COMMON.PROC.PD3.5 Tester Sent EPR_Mode (Enter)":"",
        "COMMON.PROC.PD3.6 UUT Sent EPR_Mode (Enter)":""
    }
    REPORT_NAME = datetime.now().strftime('%Y%m%d_%H%M%S') + "_"+ TEMPLATE_TYPE




    