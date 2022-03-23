# 
# This is working version of script 
# 
# 1. get TCP/IP Data
# 2. get USB Data
# 3. check this data
# 4. write data in db
#

import time
import serial
import socket
import sys
import os
from pymongo import MongoClient
from termcolor import colored





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




def read_tcp_data():
    '''
        connect and listening ip:prot and receive tcp data
    '''

    host = "192.168.1.100" 
    port = 6070
    
    print()
    print("> Listening to TCP connection...")
    
    recieved_data = ''

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
       
        data = s.recv(1024)
        recieved_data = data.decode('utf-8')
        
        print("--------------------------------------")
        print("Get TCP data: ", end="")
        print(colored(recieved_data, 'green'))
        print("--------------------------------------")
        print()
        print("> Listening to SERIAL connection...")
        
        return recieved_data
    

def read_serial_data(ser):
    
    serial_data = ''
    
    while(True):
        if(ser == None):
            ser = serial_connect()
            print("> Reconnected serial port...")
        else:
            serial_data = ser.readline() # DECODE BYTE STRING TO STRING
            serial_data = serial_data.decode('UTF-8')

            # IF GET SOME DATA, WAIT TCP DATA
            if serial_data != '':
                print("--------------------------------------")
                print("> Serial Data: ", end='')
                print(colored(serial_data, 'red'))
                print("--------------------------------------")
                break
                
    return serial_data
                
    


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


   


def main():
    '''
        listening to tcp and serial port
    '''

    # CREATE SERIAL CONNECTION
    ser = serial_connect()
    tcp_data = None
    serial_data = None

    while(True):
<<<<<<< HEAD
        
        # READ TCP DATA
        tcp_data = read_tcp_data()
        
        if tcp_data != '':
            # READ SERAIL DATA
            serial_data = read_serial_data(ser)
            
        # CHECK DATA IN DB
        if tcp_data != '' and serial_data != '':
            print()
            print("--------------------------------------")
            print(colored("...CHECKING DATA IN MONGO DB...", 'magenta'))
            print("--------------------------------------")
            
=======
        # try:
            if(ser == None):
                ser = serial_connect()
                print("> Reconnected serial port...")

            else:


                serial_data = ser.readline() # DECODE BYTE STRING TO STRING
                serial_data = serial_data.decode('UTF-8')

                
               
                # IF GET SOME DATA, WAIT TCP DATA
                if serial_data != '':
                    print("--------------------------------------")
                    print(f"> Serial Data: {serial_data}")
                    print("--------------------------------------")
                    # print("> Please wait 2 second...")
                    # time.sleep(2)
                    
                    tcp_data = tcp_data_listener()

                    # CHECK FUNCTION
                    # check_data_in_db(serial_data, tcp_data)

        # except:
        #     if(not(ser == None)):
        #         ser.close()
        #         ser = None
        #         print("> Disconnecting serial port...")
                
                

        #         send_email()
>>>>>>> 819331c9b38602395cdcd332e15f8e7abd085cea

                   



if __name__ == "__main__":
    print("=======================================")
    print("> Script start")
    print("=======================================")

    main()

