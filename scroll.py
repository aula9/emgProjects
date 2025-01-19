import pyautogui
import time
import numpy as np
import serial
import struct

# Setup Serial Connection
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=921600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0
)

def process_emg(emg_value):
    threshold = 2 
    if emg_value > threshold:
        return "scroll_up"
    else:
        return "scroll_down"

def scroll_up():
    pyautogui.scroll(100)
    print("Scrolled Up")

def scroll_down():
    pyautogui.scroll(-100)
    print("Scrolled Down")

def moving_average(values, window_size):
    return np.convolve(values, np.ones(window_size)/window_size, mode='valid')

ser.flushInput()
emg_values = []

while True:
    x = ser.read(4)
    if x and len(x) == 4:
        sensor_value = list(struct.unpack('f', x))
        emg_values.append(sensor_value[0])

        if len(emg_values) > 10:  # Use a moving window size of 10
            averaged_value = moving_average(emg_values, 10)[-1]
            print(f"Averaged EMG Value: {averaged_value}")

            action = process_emg(averaged_value)
            if action == "scroll_up":
                scroll_up()
            elif action == "scroll_down":
                scroll_down()
            
            emg_values.pop(0)  # Remove the oldest value to maintain window size
    
    time.sleep(0.1)
