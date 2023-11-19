import tkinter as tk
from tkinter import ttk
import numpy as np
import math
import matplotlib.pyplot as plt
from tkinter import filedialog
from functools import partial

from DPS.Task2 import add_signals
from DPS.Task3 import task3
from DPS.task5 import tst
from DPS.task5.DCT_DC import Task5


def taskk5(value):
    user_var = value
    global Y, DCT, N
    Y = [50.3844170297569,
         49.5528258147577,
         47.5503262094184,
         44.4508497187474,
         40.3553390593274,
         50]

    DCT = []
    N = len(Y)
    for x in range(N):
        k = 0
        for y in range(N):
            k += Y[y] * math.cos((math.pi / (4 * N)) * (2 * y - 1) * (2 * x - 1))
        k *= math.sqrt(2 / N)
        DCT.append(round(k, 5))

    with open("DCToutput.txt", "w") as myFile:
        for i in range(int(user_var)):
            myFile.write(str(i) + '  ' + str(DCT[i]) + '\n')

    print(DCT)

    before = [10.4628, 7.324, 7.8834, 11.3679, 12.962, 10.4628, 7.324,
              7.8834, 11.3679, 12.962, 11.3679, 12.962, 10.4628, 7.324, 7.8834, 12.962]

    sum = 0

    for j in before:
        sum += j

    before_mean = sum / len(before)

    for j in range(len(before)):
        before[j] = round((before[j] - before_mean), 3)

    after = before

    with open("DC_output.txt", "w") as myFile:
        for i in range(len(after)):
            myFile.write(str(i) + '  ' + str(after[i]) + '\n')

    print(after)

    tst.SignalSamplesAreEqual("DCT_output.txt", DCT)
    tst.SignalSamplesAreEqual("DC_component_output.txt", after)

def calculate_dct(user_var):
    task5(user_var)

# Globals
X_label = None
file_path = None
timelist = np.arange(0, 10, .1)
points = []
digital = True
points1, points2 = [], []


### Functions
def switch_to_frame(frame_to_show, frame_to_hide):
    frame_to_hide.pack_forget()
    frame_to_show.pack()


def draw_wave():
    re_enter_label.config(text="")
    wave_type = value_entry.get()
    Amplitude = float(Amplitude_entry.get())
    AnalogFrequency = float(AnalogFrequency_entry.get())
    SamplingFrequency = int(SamplingFrequency_entry.get())
    PhaseShift = float(PhaseShift_entry.get())

    global timelist, digital
    timelist = np.arange(0, 10, 0.01)

    if SamplingFrequency != 0:

        timelist = np.linspace(0, 10, (SamplingFrequency * 10))
        digital = False

        if wave_type == "sin":
            ylist = Amplitude * np.sin(2 * np.pi * (AnalogFrequency / SamplingFrequency) * timelist + PhaseShift)
        elif wave_type == "cos":
            ylist = Amplitude * np.cos(2 * np.pi * (AnalogFrequency / SamplingFrequency) * timelist + PhaseShift)
        else:
            display_error_message("Enter right data", 2)  # 2 for re-enter message
            ylist = None

    else:
        if wave_type == "sin":
            ylist = Amplitude * np.sin(2 * np.pi * AnalogFrequency * timelist + PhaseShift)
        elif wave_type == "cos":
            ylist = Amplitude * np.cos(2 * np.pi * AnalogFrequency * timelist + PhaseShift)
        else:
            display_error_message("Enter right data", 2)  # 2 for re-enter message
            ylist = None

    return ylist


def plot_wave():
    ylist = draw_wave()
    if ylist is not None:
        plt.figure(num=0, dpi=120, figsize=(10, 4))
        if digital:
            # plt.subplot(2,1,1)
            plt.plot(timelist, ylist)
            plt.title("wave")
            plt.xlabel("Time(s)")
            plt.ylabel("AMP")
            plt.axhline(color="g")
            plt.grid(True)

        else:
            # plt.subplot(2, 1, 2)
            plt.stem(timelist, ylist)
            plt.title("wave")
            plt.xlabel("Time(s)")
            plt.ylabel("AMP")
            plt.axhline(color="g")
            plt.grid(True)

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
            display_error_message("An error occurred. Choose a file and try again.", 3)

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


# open file, read and store the points
def read_and_store_points():
    file_path = open_file_dialog()
    global signal_type, is_periodic, points
    signal_type, is_periodic, points = read_points_and_metadata_from_file(file_path)


def read_and_store_points1():
    file_path = open_file_dialog()
    global signal1, isperiodic1, points1
    signal1, isperiodic1, points1 = read_points_and_metadata_from_file(file_path)


def read_and_store_points2():
    file_path = open_file_dialog()
    global signal2, isperiodic2, points2
    signal2, isperiodic2, points2 = read_points_and_metadata_from_file(file_path)


# Displaying the data discrete
def display_discrete():
    if points:
        plot_discrete(points)
    else:
        display_error_message("You should choose a file first.", 1)  # 1 for display error message


# Displaying the data continues
def display_continuous(choice):
    cl = add_signals.Add_Signals()
    pointss = []  # Initialize an empty list
    if choice == "+":
        pointss.clear()  # set pointss to null before using it
        if points1 and points2:  # Check if both signals are loaded
            pointss = cl.adding(points1, points2)
            print("Added Points:", pointss)
    elif choice == "-":
        pointss.clear()
        if points1 and points2:
            points11 = points1
            points22 = points2
            pointss = cl.subtracting(points11, points22)
            print("Subtracted Points:", pointss)
    elif choice == "*":
        points11 = points1
        cl.multiplication_constant = float(multiconst_entry.get())  # getting the consatnt value from user
        if points11:
            pointss.clear()
            pointss = cl.multiplication(
                points11)  # make entry to take multiplicatoin constant from user and define it in class

            print("multiplicatoin points:", pointss)

    elif choice == "shift":
        points11 = points1
        cl.shift_constant = float(shift_entry.get())  # getting the consatnt value from user
        if points11:
            pointss.clear()
            pointss = cl.shift(points11)  # make entry to take multiplicatoin constant from user and define it in class

            print("multiplicatoin points:", pointss)

    elif choice == "norm":
        points11 = points1
        cl.norm_mode = norm_var.get()  # getting the consatnt value from user
        if points11:
            pointss.clear()
            pointss = cl.norm(points11)  # make entry to take multiplicatoin constant from user and define it in class

            print("multiplicatoin points:", pointss)

    elif choice == "acc":
        points11 = points1
        if points11:
            pointss.clear()
            pointss = cl.acc(points11)  # make entry to take multiplicatoin constant from user and define it in class

    elif choice == "2":
        points11 = points1
        pointss.clear()
        if points1:
            pointss = cl.squaring(points11)
            print("squaring Points:", pointss)
    elif choice == 0:
        pointss.clear()
        if points:  # Check if a single signal is loaded
            pointss = points

    if pointss:  # Check if the list is not empty
        plot_continuous(pointss)
    else:
        display_error_message("No data to plot.", 1)


def option_selected(*args):
    label.config(text=f"Selected: {value}")
    user_choice.set(selected_option.get())


# Function to update the label when an option is selected
def entry_option_selected(*args):
    global label
    value = user_choice.get()
    label.config(text=f"Selected (Entry): {value}")


def calculate_bits():
    selected_value = selected_option.get()
    task3.quantization.calculate_bits(points1, selected_value)


#############################################################################
# creating the app
app = tk.Tk()
app.title("DPS")

### Frames
frame0 = ttk.Frame(app, padding="50")
frame0.pack()

frame = ttk.Frame(app, padding="40")
frame.pack()
frame.pack_forget()

frame2 = ttk.Frame(app, padding="20")
frame2.pack()
frame2.pack_forget()

frame3 = ttk.Frame(app, padding="50")
frame3.pack(side="bottom", pady=20)
frame3.pack_forget()

frame4 = ttk.Frame(app, padding="50")
frame4.pack()
frame4.pack_forget()

frame5 = ttk.Frame(app, padding="50")  # task3
frame5.pack()
frame5.pack_forget()

frame6 = ttk.Frame(app, padding="50")  # task5
frame6.pack()
frame6.pack_forget()

## labels
error_label = tk.Label(frame3, text="", fg="red", pady=50)
error_label.pack()

re_enter_label = tk.Label(frame2, text="", fg="red", pady=10)
re_enter_label.pack()

choose_label = ttk.Label(frame, text="Choose your weapon", padding="20")
choose_label.pack()

entry_label = ttk.Label(frame2, text="Enter your data", padding="20")
entry_label.pack()

wave_label = ttk.Label(frame2, text="Enter sin/cos:", padding="20")
wave_label.pack()
value_entry = ttk.Entry(frame2, width=20)
value_entry.pack()

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

### buttons
# Button to read and store the points
read_button = tk.Button(frame3, text="Choose File", command=lambda: read_and_store_points())
read_button.pack(pady=10)

# Buttons for displaying data in separate windows
discrete_button = tk.Button(frame3, text="Display Discrete Graph", command=display_discrete)
discrete_button.pack(pady=10)

continuous_button = tk.Button(frame3, text="Display Continuous Graph", command=lambda: display_continuous(0))
continuous_button.pack(pady=10)

draw_button = tk.Button(frame, text="Draw your signal", command=lambda: switch_to_frame(frame2, frame))
draw_button.pack(pady=10)

points_button = tk.Button(frame, text="read points", command=lambda: switch_to_frame(frame3, frame))
points_button.pack(pady=10)

plot_button = tk.Button(frame2, text="Plot it", command=plot_wave, padx=20)
plot_button.pack(pady=10)

task1_button = ttk.Button(frame0, text="Task1", command=lambda: switch_to_frame(frame, frame0))
task1_button.pack()

task2_button = ttk.Button(frame0, text="Task2", command=lambda: switch_to_frame(frame4, frame0))
task2_button.pack()

task3_button = ttk.Button(frame0, text="Task3", command=lambda: switch_to_frame(frame5, frame0))
task3_button.pack()

frame2_back_button = tk.Button(frame2, text="back", command=lambda: switch_to_frame(frame, frame2))
frame2_back_button.pack(pady=10)

frame3_back_button = tk.Button(frame3, text="back", command=lambda: switch_to_frame(frame, frame3))
frame3_back_button.pack(pady=10)

frame4_file1_button = tk.Button(frame4, text="choose first file", command=lambda: read_and_store_points1())
frame4_file1_button.pack(pady=10)

frame4_file2_button = tk.Button(frame4, text="choose second file", command=lambda: read_and_store_points2())
frame4_file2_button.pack(pady=10)

# task3
value_label = ttk.Label(frame5, text="bits/levels")
value_label.pack(pady=10)

options = ["bits", "levels"]
selected_option = tk.StringVar(app)
selected_option.set(options[0])

radioOption = tk.StringVar()
# Create the OptionMenu
option_menu = tk.OptionMenu(frame5, selected_option, *options, command=entry_option_selected)
option_menu.pack(pady=5)

entry_var = tk.IntVar(frame5)
entry = ttk.Entry(frame5, textvariable=entry_var)
entry.pack(pady=10)

frame5_file_button = tk.Button(frame5, text="choose signal file", command=lambda: read_and_store_points1())
frame5_file_button.pack(pady=10)

user_choice = tk.StringVar()
user_choice.trace_add("write", entry_option_selected)

calculattask5 = tk.Button(frame5, text="Calculate", command=calculate_bits)
calculattask5.pack(pady=10)


#################################################################################
## task5


task5_button = ttk.Button(frame0, text="Task5", command=lambda: switch_to_frame(frame6, frame0))
task5_button.pack()

value_label55 = ttk.Label(frame6, text="enter number of dct:", padding="20")
value_label55.pack()
value_entry55 = ttk.Entry(frame6, width=20)
value_entry55.pack()
global value55
value55 = value_entry55.get()
calculattask5 = ttk.Button(frame6, text="Calculate", command=lambda: taskk5(value55))
calculattask5.pack(pady=10)
# print(DCT_DC.Task5.DCT)
##################################################################################
add_signals_button = tk.Button(frame4, text="add signals", command=lambda: display_continuous("+"))
add_signals_button.pack(pady=10)

subtract_signals_button = tk.Button(frame4, text="subtract signals", command=lambda: display_continuous("-"))
subtract_signals_button.pack(pady=10)

### label entry for multi value

multiconst_label = ttk.Label(frame4, text="Enter constant value:", padding="20")
multiconst_label.pack()
multiconst_entry = ttk.Entry(frame4, width=20)
multiconst_entry.pack()

multi_signals_button = tk.Button(frame4, text="multiplicate signal with constant",
                                 command=lambda: display_continuous("*"))
multi_signals_button.pack(pady=10)

shift_label = ttk.Label(frame4, text="Enter constant value:", padding="20")
shift_label.pack()
shift_entry = ttk.Entry(frame4, width=20)
shift_entry.pack()

shift_signals_button = tk.Button(frame4, text="shift signal", command=lambda: display_continuous("shift"))
shift_signals_button.pack(pady=10)

type = ["-1 to 1", "0 to 1"]
norm_var = tk.StringVar(frame4)
norm_var.set("Select an option")
menu = tk.OptionMenu(frame4, norm_var, *type)
menu.pack(pady=10)

norm_signals_button = tk.Button(frame4, text="norm signal", command=lambda: display_continuous("norm"))
norm_signals_button.pack(pady=10)

squaring_signals_button = tk.Button(frame4, text="squaring first signal", command=lambda: display_continuous("2"))
squaring_signals_button.pack(pady=10)

acc_signals_button = tk.Button(frame4, text="Accumulation signal", command=lambda: display_continuous("acc"))
acc_signals_button.pack(pady=10)

app.mainloop()
