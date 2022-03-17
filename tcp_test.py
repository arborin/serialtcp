import time
import socket


def tcp_data_listener():
    host = "192.168.1.100" 
    port = 6070
    
    print()
    print("> Listening to TCP connection...")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
                
        data = s.recv(1024)
        recieved_data = data.decode('utf-8')
        s.close()
        print("--------------------------------------")
        print(f"> Get TCP data: {recieved_data}")
        print("--------------------------------------")


while True:
    tcp_data_listener()
    time.sleep(2)
