import serial
import struct
import time
import pyautogui
def scroll_up():
    pyautogui.scroll(100) 
    print("Scrolled Up")
def scroll_down():
    pyautogui.scroll(-100)   
    print("Scrolled Down")
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=921600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0)  # Setup Serial Connection
ser.flushInput()
while True:
    x = ser.read(4)
    sensor_value = []
    if x and len(x) == 4:
        sensor_value = list(struct.unpack('f', x))
        print(f"Sensor Value: {sensor_value[0]}")
    if sensor_value and sensor_value[0] > 2: 
        scroll_up()
        time.sleep(1)
    elif sensor_value:
        scroll_down()
        time.sleep(1)
