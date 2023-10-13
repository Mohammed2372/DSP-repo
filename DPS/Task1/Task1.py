import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np

# Globals
X_label = None
file_path = None
points = []


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
            display_error_message("An error occurred. Choose a file and try again.")

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


# Function to display an error message in the frame with red color
def display_error_message(error_msg):
    error_label.config(text=error_msg, fg="red")


# Create a tkinter window
root = tk.Tk()
root.title("Point Reader")

# Create an empty frame
bottom_frame = tk.Frame(root)
bottom_frame.pack(side="bottom", pady=20)

# Create an error label to display error messages
error_label = tk.Label(bottom_frame, text="", fg="red", pady=50)
error_label.pack()


# Create a button to open files, read and store the points
def read_and_store_points():
    file_path = open_file_dialog()
    global signal_type, is_periodic, points
    signal_type, is_periodic, points = read_points_and_metadata_from_file(file_path)


# Create two buttons for displaying the data either discretely or continuously
def display_discrete():
    if points:
        plot_discrete(points)
    else:
        display_error_message("You should choose a file first.")


def display_continuous():
    if points:
        plot_continuous(points)
    else:
        display_error_message("You should choose a file first.")


# Button to read and store the points
read_button = tk.Button(bottom_frame, text="Choose File", command=read_and_store_points)
read_button.pack()

# Buttons for displaying data in separate windows
discrete_button = tk.Button(bottom_frame, text="Display Discrete Graph", command=display_discrete)
discrete_button.pack()

continuous_button = tk.Button(bottom_frame, text="Display Continuous Graph", command=display_continuous)
continuous_button.pack()

# Start the tkinter main loop
root.mainloop()
