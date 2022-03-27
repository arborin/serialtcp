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
import smtplib
from pymongo import MongoClient
from termcolor import colored
from datetime import datetime
from email.mime.text import MIMEText



class SerialConnector:
    
    serial = ''
    
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.ser = self.connect()
        
        
    def connect(self):
        '''
            serial port configuration
        '''
        try:
            self.ser = serial.Serial(
                port = self.port,
                baudrate = self.baudrate,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
            )
        except:
            self.ser = None

        return self.ser
    
      
    def read_serial_data(self):
        ''' 
            reads and print data from serial port
        '''
    
        serial_data = 'error'
            
        while(True):
            
            try:
                if(self.ser == None):
                    self.ser = self.connect()
                    time.sleep(1.0)
                    # CHECK IT AGAIN
                    if(self.ser == None):
                        print(colored(f" Read Failed: {self.port} ", 'grey', 'on_red'))
                        break
        
                if self.ser:
                    serial_data = self.ser.readline() # DECODE BYTE STRING TO STRING
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
                            
                        print(colored(f" {message} ", 'grey', bg_color))
                        
                        break
                        
            except Exception as e:
                if(not(self.ser == None)):
                    self.ser.close()
                    self.ser = None
                    print(colored(f" Read Failed: {self.port} ", 'grey', 'on_red'))
                    # print(e)
                break
                                    
        return serial_data


class TcpConnector:
    
    def __init__(self, host, port):
        
        self.host = host
        self.port = port
        
        
    def tcp_test(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        try:
            s.connect((self.host, self.port))
            recieved_data = 'ok'
        except:
            recieved_data = 'error'
        
        return recieved_data
            
            
    def read_tcp_data(self):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:               
                s.connect((self.host, self.port))   
                data = s.recv(1024)
                recieved_data = data.decode('utf-8')
                
                # CALCULATE DATA LENGTH
                data_length = len(recieved_data.split('#'))
                
                bg_color = 'on_green'
                message = recieved_data
                
                if data_length != 7: 
                    bg_color = 'on_blue'
                    message = "NO READ"
                    recieved_data = 'error'
                    
            
                print(colored(f" {message} ", 'grey', bg_color) , end='')
                print(' ++ ', end='')
                sys.stdout.flush()

            except:
                recieved_data = 'error'
        
        return recieved_data
        

class Db:
    
    def __init__(self, mongo_conn, database, collection):
        self.mongo_conn = mongo_conn
        self.database = database
        self.collection = collection
        self.coll = self.connect()

    def connect(self):
        '''
            mongodb configuration
            this configuration will be move in config file
        '''
       
        result = ''
        
        try:
            client = MongoClient(self.mongo_conn)
            db = client[self.database]
            result = db[self.collection]
            
            db.command("serverStatus")       
        except:
            result = 'error'
        
        return result
        
    def update_data_in_db(self, serial_data, tcp_data):

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

        search_result = self.coll.find_one(search_dict)

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
            
            values['Date'] = update_vals[0]
            values['Time'] = update_vals[1]
            # CREATE STRING COMMENT FROM LIST
            values['Comment'] = " ".join(update_vals[9:])
            
            # update existing value list
            # values.update(search_result['Measurement_Values'])
            # print(values)
            self.coll.update_one(search_dict, { "$set": { "Measurement_Values":  values }})



class Email:
    
    def __init__(self, smtp_server, smtp_port, smtp_user, smtp_pass):
        
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_pass = smtp_pass
        
    def set_mail_data(self, sender, receiver, subject, message):
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.message = message
    
    
    def send_email(self):
        # DONT MAKE IDENTATION 
        msg = MIMEText(self.message)
        msg['Subject'] = self.subject
        msg['From'] = self.sender
        msg['To'] = self.receiver
        
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.login(self.smtp_user, self.smtp_pass)
            server.sendmail(self.sender, self.receiver, msg.as_string())
            
    
    def test_email(self):
        result = 'ok'
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.login(self.smtp_user, self.smtp_pass)
        except:
            result = 'error'
        
        return result

              
    
  



def print_color_codes():

    print(colored("---------------------------------------", 'green'))
    print(colored("Color-codes:", attrs=['bold']))
    print(colored(" Green  ", "grey", "on_green") + ": Data OK")
    print(colored(" Red    ", "grey", "on_red") + ": Screwing error")
    print(colored(" Blue   ", "grey", "on_blue") + ": TCP/IP error")
    print(colored(" Yellow ", "grey", "on_yellow") + ": MongoDB error")
    print(colored("---------------------------------------", 'green'))
    
    

def check_connections(ser, tcp_con, db, email):
    
    # 1. CHECK SERIAL CONNECTION AND PRINT STATUS
    serial_status = "OK"
    serial_bg = "on_green" 
    
    if ser == None:
        serial_status = "NOK"
        serial_bg = "on_red"
        
    print("> USB connection:\t" + colored(f" {serial_status} ", 'grey', serial_bg))
    
    # 2. CHECK TCP CONNECTION AND PRINT STATUS
    tcp_data = tcp_con.tcp_test()
    tcp_status = "OK"
    tcp_bg = "on_green" 
    
    if tcp_data == 'error':
        tcp_status = "NOK"
        tcp_bg = "on_red" 
    
    print("> TCP/IP connection:\t" + colored(f" {tcp_status} ", 'grey', tcp_bg))
    
    # 3. DATABSE CONNECTION
    db_status = "OK"
    db_bg = "on_green" 
    
    # IF DATABASE CHECK IS OFF
    if db is not None:
        db_result = db.connect()
        
        if db_result == 'error':
            db_status = "NOK"
            db_bg = "on_red" 
        
        print("> DB connection:\t" + colored(f" {db_status} ", 'grey', db_bg))
        
    
    # 4. EMAIL CONNECTION
    email_status = "OK"
    email_bg = "on_green"
    
    if email is not None:
        email_result = email.test_email()
        
        if email_result == 'error':
            email_status = "NOK"
            email_bg = "on_red" 
        
        print("> Email Login:\t\t" + colored(f" {email_status} ", 'grey', email_bg))
        
    
    result = 'ok'
        
    if serial_status == 'NOK' or tcp_status == 'NOK' or db_status == 'NOK' or email_status == 'NOK':
        result = 'error'
    
    return result
        


def main(ser, tcp_con, db, email):
    '''
        listening to tcp and serial port
    '''

    # CREATE SERIAL CONNECTION
    # ser = serial_connect()
    tcp_data = None
    serial_data = None
    
    print_color_codes()
    
    # COUNTING ERRORS 
    error_data = {'count': 0, 'time': ''}
    
    
    print("Listening to TCP & USB data stream....")

    while(True):
        
        try:
            # READ TCP DATA
            tcp_data = tcp_con.read_tcp_data()

            if tcp_data != '':
                # READ SERAIL DATA
                serial_data = ser.read_serial_data()
                
            # CHECK DATA IN DB
            if serial_data != '' and serial_data != 'error' and tcp_data != 'error':
                
                if db:
                    # UPDATE DATA IN DB
                    db.update_data_in_db(serial_data, tcp_data)
                    
                    # THIS MESSAGE MUST DEPEND ON DB UPDATE OR NOT
                    print(colored(' DB OK ', 'grey', 'on_green'))
            
            # GET ERROR MESSAGE
            else:
                error_data['count'] += 1
                
                # IF FIRST ERROR SAVE TIME
                if error_data['count'] == 1:
                    error_data['time'] = datetime.now()
                
                # CHECK TIMEDELTA
                time_delta_min = int((datetime.now() - error_data['time']).total_seconds() / 60)
                
                # IF IN 5 MUNUTE OCCURED 3 ERROR
                if time_delta_min <= 5 and error_data['count'] >= 3:
                    if email:
                        try:
                            email.send_email()
                            error_data['count'] = 0
                            print(colored(' Email Sent ', 'grey', 'on_green'))
                        except:
                            print(colored(' Email not send ', 'grey', 'on_red'))
                    
                    
            
        except KeyboardInterrupt:
            print()
            print(colored("---------------------------------------", 'red'))
            print("> Script end")
            print(colored("---------------------------------------", 'red'))
            sys.exit()
                   



if __name__ == "__main__":
    print(colored("=======================================", 'green'))
    print("> Script start")
    print(colored("=======================================", 'green'))
    
    # CONFIGURATION
    # ====================================
    
    # TCP CONNECTION
    host = '192.168.1.100'
    tcp_port = 6070
    
    # SERIAL CONNECTION
    serial_port='/dev/ttyUSB0'
    baudrate=9600
    
    # DB CONNECTION
    mongo_conn = 'mongodb://192.168.1.50:27017/'
    database = "learning"
    collection = "upwork"
    
    # EMAIL CONFIG
    smtp_server = "smtp.mailtrap.io"
    smtp_port = 2525
    smtp_user = "f69396842d193f"
    smtp_pass = "c831385ef5eec6"
    #
    sender = "nika.kobaidze@gmail.com"
    receiver = "revievermail@gmail.com"
    subject = "Alert"
    message = "Can not read data"
    
    # True - write data in database
    # False - don't data in database
    write_db = False
    
    # True - send email
    # False - don't send email
    send_email = True
    
    # END CONFIGURATION
    #=====================================
    
    # SERIAL
    serial_con = SerialConnector(serial_port, baudrate);
    
    # TCP
    tcp_con = TcpConnector(host, tcp_port)
    
    # MONG DB
    db = None
    if write_db:
        db = Db(mongo_conn, database, collection)
    
    email = None
    if send_email:
        email = Email(smtp_server, smtp_port, smtp_user, smtp_pass)
        email.set_mail_data(sender, receiver, subject, message)
    
    
    # CONNECTION RESULT
    result = check_connections(serial_con, tcp_con, db, email)
    
    # IF ALL CONNECTIONS ARE OK
    if result == 'ok':
                
        # RUN MAIN LOOP
        main(serial_con, tcp_con, db, email)
    else:
        print(colored("---------------------------------------", 'red'))
        print(colored('> Connection check failed...', 'red'))
        print(colored("---------------------------------------", 'red'))
        

