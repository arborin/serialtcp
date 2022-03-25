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
    try:
        ser = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate = 9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
    except:
        ser = None

    return ser




def db_connect():
    '''
        mongodb configuration
        this configuration will be move in config file
    '''
    mongo_conn = 'mongodb://192.168.1.50:27017/'
    database = "learning"
    collection = "upwork"
    
    result = ''
    
    try:
        client = MongoClient(mongo_conn)
        db = client[database]
        result = db[collection]
        
        db.command("serverStatus")
            
    except:
        result = 'error'
    
    return result



def read_tcp_data(connection_test = 0):
    '''
        connect and listening ip:prot and receive tcp data
    '''

    host = '192.168.1.100'
    port = 6070
    recieved_data = ''
    
    # THIS IS FOR TESTING CONNECTION 
    if connection_test == 1:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        try:
            s.connect((host, port))
            recieved_data = 'ok'
        except:
            recieved_data = 'error'
    
    else:
    
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:                
                s.connect((host, port))   
                data = s.recv(1024)
                recieved_data = data.decode('utf-8')
                
                data_length = len(recieved_data.split('#'))
                
                bg_color = 'on_green'
                message = recieved_data
                
                if data_length != 7: 
                    bg_color = 'on_blue'
                    message = "NO READ"
                    recieved_data = 'error'
                    
                
                print(colored(message, 'grey', bg_color) , end='')
                print(' ++ ', end='')
                sys.stdout.flush()

            except:
                recieved_data = 'error'
        
    return recieved_data
    

def read_serial_data(ser):
    
    serial_data = ''
        
    while(True):
        
        try:
            if(ser == None):
                ser = serial_connect()
                time.sleep(1.0)
            else:
                serial_data = ser.readline() # DECODE BYTE STRING TO STRING
                serial_data = serial_data.decode('UTF-8')

                # IF GET SOME DATA, WAIT TCP DATA
                if serial_data != '':
                    
                    bg_color = 'on_green'
                    message = serial_data
                    
                    if 'ABBRUCH' in serial_data:
                        bg_color = 'on_red'
                    
                    if len(serial_data.split(" ")) < 9:
                        bg_color = 'on_red'
                        message = "NO READ"
                        serial_data = 'error' # it is return value for checking
                        
                        
                    print(colored(message, 'grey', bg_color))
                    
                    break
                    
        except Exception as e:
            if(not(ser == None)):
                ser.close()
                ser = None
                print("> Disconnecting serial port...")
                print(e)
            break
                                
    return serial_data
                
    
def send_email():
    '''
        email sending
    '''
    print("> SNED EMAIL ALERT")
    
    

def update_data_in_db(serial_data, tcp_data):

    coll = db_connect()  # mongo db collection

    tcp_list = tcp_data.split("#")
    # EXAMPLE
    # ['', 'N01HHAR2502301', 'Ca', '131945', 'T04222', 'S0002130', 'N01']
    
    search_dict = {
            "PartNo": tcp_list[1], 
            "PartIndex": tcp_list[2], 
            "SupplierID": int(tcp_list[3]), 
            "ManfDay": tcp_list[4],
            "SerialNo": tcp_list[5],
            "Cavity": tcp_list[6]
    }

    search_result = coll.find_one(search_dict)

    if search_result:
        update_vals = serial_data.split(" ")
         
        # example of update_vals = ['09.03.2022', '10:22:58', 'PG:', '11', 'TQ:', '3.81', 'Nm', 'AN:', '1215', 'Grad', 'IO'] 
        
        # get keys and values will be next elements in list
        values = {"PG": '', "TQ": '', "AN": ''}

        for key in values.keys():
            try:
                index = update_vals.index(key+":") # get key index
                values[key] = update_vals[index+1] # index+1 will be value of this key
            except:
                pass
        
        values['date'] = update_vals[0]
        values['time'] = update_vals[1]
        # CREATE STRING COMMENT FROM LIST
        values['comment'] = " ".join(update_vals[9:])
        
        # update existing value list
        # values.update(search_result['Measurement_Values'])
        # print(values)
        coll.update_one(search_dict, { "$set": { "Measurement_Values":  values }})


def print_color_codes():

    print("---------------------------------------")
    print(colored("Color-codes:", attrs=['bold']))
    print(colored(" Green  ", "grey", "on_green") + ": Data OK")
    print(colored(" Red    ", "grey", "on_red") + ": Screwing error")
    print(colored(" Blue   ", "grey", "on_blue") + ": TCP/IP error")
    print(colored(" Yellow ", "grey", "on_yellow") + ": MongoDB error")
    print("---------------------------------------")
    
    

def check_connections():
    
    # 1. CHECK SERIAL CONNECTION AND PRINT STATUS
    ser = serial_connect()
    serial_status = " OK "
    serial_bg = "on_green" 
    
    if ser == None:
        serial_status = " NOK "
        serial_bg = "on_red"
        
    print("> USB connection:\t" + colored(serial_status, 'grey', serial_bg))
    
    # 2. CHECK TCP CONNECTION AND PRINT STATUS
    tcp_data = read_tcp_data(connection_test=1)
    tcp_status = " OK "
    tcp_bg = "on_green" 
    
    if tcp_data == 'error':
        tcp_status = " NOK "
        tcp_bg = "on_red" 
    
    print("> TCP/IP connection:\t" + colored(tcp_status, 'grey', tcp_bg))
    
    # 3. DATABSE CONNECTION
    db_result = db_connect()
    db_status = " OK "
    db_bg = "on_green" 
    
    if db_result == 'error':
        db_status = " NOK "
        db_bg = "on_red" 
    
    print("> DB connection:\t" + colored(db_status, 'grey', db_bg))
    
    result = 'ok'
    
    if serial_status == ' NOK ' or tcp_status == ' NOK ' or db_status == ' NOK ':
        result = 'error'
    
    return result
        


def main():
    '''
        listening to tcp and serial port
    '''

    # CREATE SERIAL CONNECTION
    ser = serial_connect()
    tcp_data = None
    serial_data = None
    
    print("Listening to TCP & USB data stream....")

    while(True):
        
        try:
            # READ TCP DATA
            try:
                tcp_data = read_tcp_data()
            except:
                print("Serial connection failed")
            
            if tcp_data != '':
                # READ SERAIL DATA
                serial_data = read_serial_data(ser)
                
            # CHECK DATA IN DB
            if serial_data != '' and serial_data != 'error' and tcp_data != 'error':
                update_data_in_db(serial_data, tcp_data)
                # THIS MESSAGE MUST DEPEND ON DB UPDATE OR NOT
                print(colored("DB OK", 'grey', 'on_green'))
            
        except KeyboardInterrupt:
            print()
            print("=======================================")
            print("> Script end")
            print("=======================================")
            sys.exit()
                   



if __name__ == "__main__":
    print("=======================================")
    print("> Script start")
    print("=======================================")
    
    result = check_connections()
        
    if result == 'ok':
        print_color_codes()
        
        main()
    else:
        print(colored('\nConnection check failed...\n', 'red'))
        

