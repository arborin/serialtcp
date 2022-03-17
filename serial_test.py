import time
import serial



def serial_connect():
    '''
        serial port configuration
        this configuration will be move in config file
    '''

    ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate = 9600, # 115200
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )

    return ser


# SERIAL CONNECTION
ser = serial_connect()

# SOCKET CONNECTION
# con = socket_connect()

print("> Listening SERIAL connection...")

while(True):
    
    serial_data = ser.readline() # DECODE BYTE STRING TO STRING
    serial_data = serial_data.decode('UTF-8')

    # IF GET SOME DATA, WAIT TCP DATA
    if serial_data != '':
        print("--------------------------------------")
        print(f"> Serial Data: {serial_data}")
        print("--------------------------------------")
        print("> Please wait 0.2 second...")
        time.sleep(.2)