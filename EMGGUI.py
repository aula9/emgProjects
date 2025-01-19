import tkinter as tk
from tkinter import filedialog
import pygame
import serial
import struct
import random
import time

pygame.mixer.init()  # Initialize Pygame Mixer
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=921600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0)  # Setup Serial Connection

# Initialize variables
volume_state = 'increase'  # State can be 'increase', 'hold', or 'decrease'
hold_time = 2  # Time to hold the volume in seconds
hold_start_time = None  # Start time for holding the volume

# Function to update volume based on sensor value
def update_volume(value, previous_value):
    global volume_state, hold_start_time

    if previous_value is None:
        volume = 0.2  # Set initial volume to a mid-level
    elif volume_state == 'increase':
        volume = min(pygame.mixer.music.get_volume() + 0.4, 1.0)  # Increase volume significantly
        if volume == 1.0:
            volume_state = 'hold'
            hold_start_time = time.time()
    elif volume_state == 'hold':
        volume = pygame.mixer.music.get_volume()
        if time.time() - hold_start_time >= hold_time:
            volume_state = 'decrease'
    elif volume_state == 'decrease':
        volume = max(pygame.mixer.music.get_volume() - 0.1, 0.0)  # Decrease volume gradually
        if volume == 0.0:
            volume_state = 'increase'  # Reset to increase state when volume is at minimum

    pygame.mixer.music.set_volume(volume)
    print(f"Current Volume: {volume}, State: {volume_state}")  # Print current volume and state
    return value

# Function to choose and play music
def play_music():
    file_path = filedialog.askopenfilename()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

root = tk.Tk()  # Create the main window
root.title('Volume Visualizer')

# Create a Canvas for drawing
canvas = tk.Canvas(root, width=400, height=300)
canvas.pack()

# Function to create a random color
def random_color():
    return '#{:02x}{:02x}{:02x}'.format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Create multiple rectangles for a visual effect
rectangles = []
for i in range(10):
    rectangles.append(canvas.create_rectangle(50 + i*30, 150, 70 + i*30, 250, fill=random_color()))

# Button to choose and play music
play_button = tk.Button(root, text='Play Music', command=play_music)
play_button.pack()

# Function to update the rectangles based on volume
def update_rectangles(volume):
    for i, rect in enumerate(rectangles):
        new_height = 250 - (volume * 200) - random.randint(0, 50)  # Add randomness to height
        canvas.coords(rect, 50 + i*30, new_height, 70 + i*30, 250)
        canvas.itemconfig(rect, fill=random_color())
        #print(f"Rectangle {i} Height: {new_height}")  # Print rectangle height
    # Change background color based on volume
    canvas.config(bg=random_color())

# Function to close the window
def close_window():
    ser.close()
    root.destroy()

# Button to exit the application
exit_button = tk.Button(root, text='Exit', command=close_window)
exit_button.pack()

# Main loop to read sensor data and update volume
previous_value = None
ser.flushInput()
sensor_value = []
while True:
    x = ser.read(4)
    if x and len(x) == 4:
        sensor_value = list(struct.unpack('f', x))
        print(f"Sensor Value: {sensor_value[0]}")  # Print sensor value
        previous_value = update_volume(sensor_value[0], previous_value)
        update_rectangles(pygame.mixer.music.get_volume())
    root.update_idletasks()
    root.update()

