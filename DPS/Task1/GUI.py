import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog

# Globals
X_label = None
file_path = None
points = []


### Functions
def switch_to_frame(frame_to_show, frame_to_hide):
    frame_to_hide.pack_forget()
    frame_to_show.pack()


def draw_wave():
    re_enter_label.config(text="")
    wave_type = wave_entry.get()
    Amplitude = float(Amplitude_entry.get())
    AnalogFrequency = float(AnalogFrequency_entry.get())
    SamplingFrequency = float(SamplingFrequency_entry.get())
    PhaseShift = float(PhaseShift_entry.get())

    global timelist
    timelist = np.arange(0, 10, .1)

    if wave_type == "sin":
        ylist = Amplitude * np.sin(2 * np.pi * (AnalogFrequency / SamplingFrequency) * timelist + PhaseShift)
    elif wave_type == "cos":
        ylist = Amplitude * np.cos(2 * np.pi * (AnalogFrequency / SamplingFrequency) * timelist + PhaseShift)
    else:
        display_error_message("Enter right data", 2)  # 2 for re-enter message
        ylist = None

    return ylist


def plot_wave():
    ylist = draw_wave()
    if ylist is not None:
        plt.figure(num=0, dpi=120, figsize=(10, 4))
        plt.plot(timelist, ylist)
        plt.title("sin wave")
        plt.xlabel("Time(s)")
        plt.ylabel("AMP")
        plt.show()


# Function to open a file dialog and return the selected file path
def open_file_dialog():
    file_path = filedialog.askopenfilename()
    return file_path


# To read points from the file
def read_points_and_metadata_from_file(file_path):
    global X_label, points
    points = []
    SignalType, IsPeriodic, size = None, None, None

    if file_path:
        try:
            with open(file_path, 'r') as file:
                # Read the first three lines to get SignalType, IsPeriodic, and Size
                SignalType = int(file.readline().strip())
                IsPeriodic = int(file.readline().strip())
                size = int(file.readline().strip())

                for line in file:
                    if size > 0:
                        x, y = map(float, line.strip().split())
                        points.append([x, y])  # Store as [x, y] sub-arrays in the 2D array
                        size -= 1

                # Set the X_label based on SignalType
                if SignalType == 0:
                    X_label = "Time"
                elif SignalType == 1:
                    X_label = "Frequency"
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            display_error_message("An error occurred. Choose a file and try again.",3)

    return SignalType, IsPeriodic, points


# Function to represent points as a discrete graph in a new window
def plot_discrete(points):
    if points:
        x_values, y_values = zip(*points)
        plt.scatter(x_values, y_values, marker='o', label='Discrete Data')
        plt.xlabel(X_label)
        plt.ylabel("Y values")
        plt.title("Signal Representation (Discrete)")
        plt.grid(True)
        plt.legend()
        plt.show()


# Function to represent points as a continuous graph in a new window
def plot_continuous(points):
    if points:
        x_values, y_values = zip(*points)

        # Increase the number of data points for a smoother curve
        interpolated_x = []
        interpolated_y = []
        for i in range(len(x_values) - 1):
            x1, x2 = x_values[i], x_values[i + 1]
            y1, y2 = y_values[i], y_values[i + 1]
            interpolated_x.extend(list(np.linspace(x1, x2, num=100))[:-1])  # 100 data points per interval
            interpolated_y.extend(list(np.linspace(y1, y2, num=100))[:-1])

        plt.plot(interpolated_x, interpolated_y, label='Continuous Data')
        plt.xlabel(X_label)
        plt.ylabel("Y values")
        plt.title("Signal Representation (Continuous)")
        plt.grid(True)
        plt.legend()
        plt.show()


# Function to display an error message in the frame
def display_error_message(error_msg, choice):
    if choice == 1:
        error_label.config(text=error_msg)
    elif choice == 2 or choice == 3:
        re_enter_label.config(text=error_msg)


# Create a button to open files, read and store the points
def read_and_store_points():
    file_path = open_file_dialog()
    global signal_type, is_periodic, points
    signal_type, is_periodic, points = read_points_and_metadata_from_file(file_path)


# Displaying the data discrete
def display_discrete():
    if points:
        plot_discrete(points)
    else:
        display_error_message("You should choose a file first.", 1)  # 1 for display error message


# Displaying the data continues
def display_continuous():
    if points:
        plot_continuous(points)
    else:
        display_error_message("You should choose a file first.",1)  # 1 for display error message


# creating the app
app = tk.Tk()
app.title("DPS")

### Frames
frame = ttk.Frame(app, padding="20")
frame.pack()

frame2 = ttk.Frame(app, padding="20")
frame2.pack()
frame2.pack_forget()

frame3 = tk.Frame(app)
frame3.pack(side="bottom", pady=20)
frame3.pack_forget()

## labels
error_label = tk.Label(frame3, text="", fg="red", pady=50)
error_label.pack()

choose_label = ttk.Label(frame, text="Choose your weapon", padding="20")
choose_label.pack()

entry_label = ttk.Label(frame2, text="Enter your data", padding="20")
entry_label.pack()

wave_label = ttk.Label(frame2, text="Enter sin/cos:", padding="20")
wave_label.pack()
wave_entry = ttk.Entry(frame2, width=20)
wave_entry.pack()

Amplitude_label = ttk.Label(frame2, text="Enter Amplitude:", padding="20")
Amplitude_label.pack()
Amplitude_entry = ttk.Entry(frame2, width=20)
Amplitude_entry.pack()

AnalogFrequency_label = ttk.Label(frame2, text="Enter Analog Frequency:", padding="20")
AnalogFrequency_label.pack()
AnalogFrequency_entry = ttk.Entry(frame2, width=20)
AnalogFrequency_entry.pack()

SamplingFrequency_label = ttk.Label(frame2, text="Enter Sampling Frequency:", padding="20")
SamplingFrequency_label.pack()
SamplingFrequency_entry = ttk.Entry(frame2, width=20)
SamplingFrequency_entry.pack()

PhaseShift_label = ttk.Label(frame2, text="Enter PhaseShift:", padding="20")
PhaseShift_label.pack()
PhaseShift_entry = ttk.Entry(frame2, width=20)
PhaseShift_entry.pack()

re_enter_label = tk.Label(frame2, text="", fg="red", pady=10)
re_enter_label.pack()

### buttons
# Button to read and store the points
read_button = tk.Button(frame3, text="Choose File", command=read_and_store_points)
read_button.pack()

# Buttons for displaying data in separate windows
discrete_button = tk.Button(frame3, text="Display Discrete Graph", command=display_discrete)
discrete_button.pack()

continuous_button = tk.Button(frame3, text="Display Continuous Graph", command=display_continuous)
continuous_button.pack()

draw_button = tk.Button(frame, text="Draw your signal", command=lambda: switch_to_frame(frame2, frame))
draw_button.pack()

draw_button = tk.Button(frame, text="Read signal", command=lambda: switch_to_frame(frame3, frame))
draw_button.pack()

plot_button = tk.Button(frame2, text="Plot it", command=plot_wave)
plot_button.pack(pady=20)

app.mainloop()
