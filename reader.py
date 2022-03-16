# 
# This is working version of script 
# 
# 1. you will get first USB Data
# 2. then you will get TCP/IP Data
# 3. cache usb data
# 4. wait for tcp data
# (time between it is maybe 1-3 seconds)
#

import time
import serial
import socket
import sys
import os
from pymongo import MongoClient





def serial_connect():
    '''
        serial port configuration
        this configuration will be move in config file
    '''

    ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )

    return ser




def db_connect():
    '''
        mongodb configuration
        this configuration will be move in config file
    '''
    mongo_conn = 'mongodb://192.168.1.50:27017/'
    database = "learning"
    collection = "upwork"

    client = MongoClient(mongo_conn)
    db = client[database]
    collection = db[collection]

    print(f"> Database connection {db}")
    
    return collection



def send_email():
    '''
        email sending
    '''
    print("> SNED EMAIL ALERT")




def tcp_data_listener():
    '''
        connect and listening ip:prot and receive tcp data
    '''

    host = "192.168.1.100" 
    port = 6070
    
    print()
    print("> Listening to TCP connection...")
    

    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # s.connect((host, port))

    # data = s.recv(1024)
    # recieved_data = data.decode('utf-8')
    # s.close()

    recieved_data = ''

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        data = s.recv(1024)
        recieved_data = data.decode('utf-8')
        
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        print("--------------------------------------")
        print(f"> Get TCP data: {recieved_data}")
        print("--------------------------------------")
        print()
        print("> Listening to SERIAL connection...")

        return recieved_data
    



def check_data_in_db(serial_data, tcp_data):

    coll = db_connect()  # mongo db collection

    tcp_list = tcp_data.split("#")
    print(tcp_list)

    
    search_dict = {
            "PartNo": tcp_list[0], 
            "PartIndex": tcp_list[1], 
            "SupplierID": int(tcp_list[2]), 
            "ManfDay": tcp_list[3],
            "SerialNo": tcp_list[4],
            "Cavity": tcp_list[5]
    }

    print(search_dict)

    search_result = coll.find_one(search_dict)

    print("==============================================")
    print(f"> SERIAL DATA: {serial_data}")
    print(f"> TCP DATA:    {tcp_data}")
    print("==============================================")
    print(f"> Database search result: {search_result}")
    print("==============================================")
    if search_result:
        update_vals = serial_data.split(" ")
        print(f"> update data {update_vals}")        
        # example of update_vals = ['09.03.2022', '10:22:58', 'PG:', '11', 'TQ:', '3.81', 'Nm', 'AN:', '1215', 'Grad', 'IO'] 
        
        # get keys and values will be next elements in list
        values = {"PG": '', "TQ": '', "AN": ''}

        for key in values.keys():
            try:
                index = update_vals.index(key+":") # GET key index
                values[key] = update_vals[index+1] # index+1 will be value of this key
            except:
                print("key not found")
        
        # update existing value list
        values.update(search_result['Measurement_Values'])
        print(values)
        coll.update_one(search_dict, { "$set": { "Measurement_Values":  values }})


   


def read_serial_data():
    '''
        listening to serial port
        main function loop
    '''

    # SERIAL CONNECTION
    ser = serial_connect()

    # SOCKET CONNECTION
    # con = socket_connect()

    print("> Listening SERIAL connection...")

    while(True):
        # try:
            if(ser == None):
                ser = serial_connect()
                print("> Reconnected serial port...")

            else:
                serial_data = ser.readline().decode("utf-8") # DECODE BYTE STRING TO STRING
               
                # IF GET SOME DATA, WAIT TCP DATA
                if serial_data != '':
                    print("--------------------------------------")
                    print(f"> Serial Data: {serial_data}")
                    print("--------------------------------------")

                    tcp_data = tcp_data_listener()

                    # CHECK FUNCTION
                    # check_data_in_db(serial_data, tcp_data)

        # except:
        #     if(not(ser == None)):
        #         ser.close()
        #         ser = None
        #         print("> Disconnecting serial port...")
                
                

        #         send_email()

        #     print("> No serial connection")
        #     time.sleep(2)



if __name__ == "__main__":
    print("=======================================")
    print("> Script start")
    print("=======================================")
    # FREE UP PORT IF IT IS ALREADY IN USE

    read_serial_data()

