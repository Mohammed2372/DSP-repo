import pandas as pd
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
import cmath
import math
from typing import List, Any

### lists for convolving


def read_data(div_x, div_y):
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as file:
            signal_type = int(file.readline().strip())
            is_periodic = int(file.readline().strip())
            n1 = int(file.readline().strip())

            for _ in range(n1):
                line = file.readline().strip()
                if line:
                    parts = line.split()
                    div_x.append(float(parts[0]))
                    div_y.append(float(parts[1]))


# advancing signal


def advance():
    x = []
    y = []
    fold_count = 0
    new_window = tk.Toplevel(root)
    new_window.geometry("200x300")
    fold = tk.Frame(new_window)
    # reading the file
    uploadButton = tk.Button(
        fold, text="upload signal", command=lambda: read_data(x, y))
    uploadButton.pack(pady=10)
    label1 = tk.Label(fold, text="advance by:")
    label1.pack(pady=10)
    advandBy = tk.IntVar(fold)
    # advance the signal by :
    advance = tk.Entry(fold, textvariable=advandBy)
    advance.pack(pady=10)

    def advance_signal():
        advancedOutPut = x.copy()
        for i in range(advandBy.get()):
            # removing the last n element from the list
            advancedOutPut.pop()

        for i in range(advandBy.get()):
            # adding element to the begining of the list
            first = advancedOutPut[0]
            advancedOutPut = [first - 1] + advancedOutPut
        return advancedOutPut

    def advance_plot(x, y):
        newX = advance_signal()
        plt.subplot(2, 1, 1)
        plt.plot(x, y, label='orginal')
        plt.legend()
        plt.subplot(2, 1, 2)

        plt.plot(newX, y, label='advanced by ' + str(advandBy.get()))
        plt.legend()
        plt.tight_layout()
        plt.show()

    def advance_folded(x, y):
        newX = advance_signal()
        nonlocal fold_count  # Use nonlocal to modify the outer fold_count variable
        fold_count += 1  # Increment the counter each time the function is called

        if fold_count % 2 == 1:  # Check if the counter is odd
            folded = newX[::-1]
        else:
            folded = newX
        plt.subplot(2, 1, 1)
        plt.plot(x, y, label='orginal')
        plt.legend()
        plt.subplot(2, 1, 2)
        plt.plot(folded, y, label='advanced_folded ')
        plt.legend()
        plt.tight_layout()
        plt.show()

    advancedButton = tk.Button(fold, text="advanced",
                               command=lambda: advance_plot(x, y))
    advancedButton.pack(pady=10)
    advancedFoldedButton = tk.Button(fold, text="advanced folded",
                                     command=lambda: advance_folded(x, y))
    advancedFoldedButton.pack(pady=10)
    fold.pack()


def delay():
    x = []
    y = []
    fold_count = 0
    new_window = tk.Toplevel(root)
    new_window.geometry("200x300")
    fold = tk.Frame(new_window)
    # reading the file
    uploadButton = tk.Button(
        fold, text="upload signal", command=lambda: read_data(x, y))
    uploadButton.pack(pady=10)
    label1 = tk.Label(fold, text="delay by:")
    label1.pack(pady=10)
    advandBy = tk.IntVar(fold)
    # advance the signal by :
    advance = tk.Entry(fold, textvariable=advandBy)
    advance.pack(pady=10)

    def delayed_signal():
        # Use list slicing to remove the first advandBy elements
        advancedOutput = x[advandBy.get():]

        for _ in range(advandBy.get()):
            last = advancedOutput[-1]
            # Use append to add elements to the end
            advancedOutput.append(last + 1)

        return advancedOutput

    def delay_plot(x, y):
        newX = delayed_signal()
        plt.subplot(2, 1, 1)
        plt.plot(x, y, label='orginal')
        plt.legend()
        plt.subplot(2, 1, 2)

        plt.plot(newX, y, label='delayed by ' + str(advandBy.get()))
        plt.legend()
        plt.tight_layout()
        plt.show()

    def delay_folded(x, y):
        newX = delayed_signal()
        nonlocal fold_count  # Use nonlocal to modify the outer fold_count variable
        fold_count += 1  # Increment the counter each time the function is called

        if fold_count % 2 == 1:  # Check if the counter is odd
            folded = newX[::-1]
        else:
            folded = newX
        plt.subplot(2, 1, 1)
        plt.plot(x, y, label='orginal')
        plt.legend()
        plt.subplot(2, 1, 2)
        plt.plot(folded, y, label='advanced_folded ')
        plt.legend()
        plt.tight_layout()
        plt.show()

    advancedButton = tk.Button(fold, text="delayed",
                               command=lambda: delay_plot(x, y))
    advancedButton.pack(pady=10)
    advancedFoldedButton = tk.Button(fold, text="delayed folded",
                                     command=lambda: delay_folded(x, y))
    advancedFoldedButton.pack(pady=10)
    fold.pack()


def fold():
    x = []
    y = []
    fold_count = 0
    new_window = tk.Toplevel(root)
    new_window.geometry("200x300")
    fold = tk.Frame(new_window)
    # reading the file
    uploadButton = tk.Button(
        fold, text="upload signal", command=lambda: read_data(x, y))
    uploadButton.pack(pady=10)

    def delay_plot(x, y):
        nonlocal fold_count  # Use nonlocal to modify the outer fold_count variable
        fold_count += 1  # Increment the counter each time the function is called

        if fold_count % 2 == 1:  # Check if the counter is odd
            x = x[::-1]
        plt.plot(x, y, label='orginal')
        plt.legend()
        plt.show()

    advancedButton = tk.Button(fold, text="folded",
                               command=lambda: delay_plot(x, y))
    advancedButton.pack(pady=10)
    fold.pack()


def DerivativeSignal():
    InputSignal = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0,
                   19.0, 20.0, 21.0, 22.0,
                   23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0, 31.0, 32.0, 33.0, 34.0, 35.0, 36.0, 37.0, 38.0, 39.0,
                   40.0, 41.0, 42.0,
                   43.0, 44.0, 45.0, 46.0, 47.0, 48.0, 49.0, 50.0, 51.0, 52.0, 53.0, 54.0, 55.0, 56.0, 57.0, 58.0, 59.0,
                   60.0, 61.0, 62.0,
                   63.0, 64.0, 65.0, 66.0, 67.0, 68.0, 69.0, 70.0, 71.0, 72.0, 73.0, 74.0, 75.0, 76.0, 77.0, 78.0, 79.0,
                   80.0, 81.0, 82.0,
                   83.0, 84.0, 85.0, 86.0, 87.0, 88.0, 89.0, 90.0, 91.0, 92.0, 93.0, 94.0, 95.0, 96.0, 97.0, 98.0, 99.0,
                   100.0]

    expectedOutput_first = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                            1, 1, 1, 1, 1, 1]
    expectedOutput_second = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0]

    result_array1 = [InputSignal[0]]  # The first element remains unchanged

    for i in range(1, len(InputSignal) - 1):
        result_array1.append(InputSignal[i] - InputSignal[i - 1])

    result_array2 = []

    for i in range(len(InputSignal) - 1):
        if i == 0:
            result_array2.append(InputSignal[i + 1] - 2 * InputSignal[i])
        elif i == len(InputSignal) - 1:
            result_array2.append(InputSignal[i - 1] - 2 * InputSignal[i])
        else:
            result_array2.append(
                InputSignal[i + 1] - 2 * InputSignal[i] + InputSignal[i - 1])

    FirstDrev = result_array1
    SecondDrev = result_array2

    """
    Testing your Code
    """
    if (len(FirstDrev) != len(expectedOutput_first)) or (len(SecondDrev) != len(expectedOutput_second)):
        print("mismatch in length")
        return
    first = second = True
    for i in range(len(expectedOutput_first)):
        if abs(FirstDrev[i] - expectedOutput_first[i]) < 0.01:
            continue
        else:
            first = False
            print("1st derivative wrong")
            return
    for i in range(len(expectedOutput_second)):
        if abs(SecondDrev[i] - expectedOutput_second[i]) < 0.01:
            continue
        else:
            second = False
            print("2nd derivative wrong")
            return
    if first and second:
        print("Derivative Test case passed successfully")
    else:
        print("Derivative Test case failed")
    return


def read_and_store_points(signal_number):
    file_path = open_file_dialog()
    signal_type, is_periodic, points = read_points_and_metadata_from_file(
        file_path)

    if signal_number == 1:
        global pointsconv1
        pointsconv1 = points
    elif signal_number == 2:
        global pointsconv2
        pointsconv2 = points


def read_points_and_metadata_from_file(file_path):
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
                        # Store as [x, y] sub-arrays in the 2D array
                        points.append([x, y])
                        size -= 1

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            display_error_message(
                "An error occurred. Choose a file and try again.", 3)

    return SignalType, IsPeriodic, points


def open_file_dialog():
    file_path = filedialog.askopenfilename()
    return file_path


def open_convolve_frame():
    convolve_frame = tk.Toplevel(root)
    convolve_frame.title("Convolution Options")
    convolve_frame.geometry("400x200")

    choose_file_button1 = tk.Button(convolve_frame, text="Choose First Signal",
                                    command=lambda: read_and_store_points(1))
    choose_file_button1.pack()

    choose_file_button2 = tk.Button(convolve_frame, text="Choose Second Signal",
                                    command=lambda: read_and_store_points(2))
    choose_file_button2.pack()

    execute_button = tk.Button(convolve_frame, text="Execute Convolution", command=perform_convolution)
    execute_button.pack()


def perform_convolution():
    if not pointsconv1 or not pointsconv2:
        display_error_message("Please choose both signals first.", 3)
        return

    try:
        # Extract the y values from the stored points
        signal1 = np.array([point[1] for point in pointsconv1])
        signal2 = np.array([point[1] for point in pointsconv2])

        # Perform custom convolution
        result = convolve_custom(signal1, signal2)

        # Do something with the result, like display it or use it further
        print("Convolution Result:", result)

        # Call the ConvTest function to perform the test
        ConvTest(np.arange(len(result)) - 2, result)

        # show_message("Operation", "Convolution completed")

    except Exception as e:
        display_error_message(f"An error occurred: {str(e)}", 3)


def convolve_custom(signal1, signal2):
    len1, len2 = len(signal1), len(signal2)
    result_len = len1 + len2 - 1
    result = np.zeros(result_len)

    # Perform convolution
    for i in range(result_len):
        for j in range(len1):
            if i - j >= 0 and i - j < len2:
                result[i] += signal1[j] * signal2[i - j]

    return result


def ConvTest(Your_indices, Your_samples):
    expected_indices = [-2, -1, 0, 1, 2, 3, 4, 5, 6]
    expected_samples = [1, 1, -1, 0, 0, 3, 3, 2, 1]

    if len(expected_samples) != len(Your_samples) or len(expected_indices) != len(Your_indices):
        print("Conv Test case failed, your signal has a different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if Your_indices[i] != expected_indices[i]:
            print("Conv Test case failed, your signal has different indices from the expected one")
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Conv Test case failed, your signal has different values from the expected one")
            return
    print("Conv Test case passed successfully")


amb = []
theta = []
tolerance = 10 ^ -6


# Example usage:
# Assuming 'out' is your input list for IDFT
# IDFT(out)


def remove_dc():
    Xn = []  # Ensure Xn is correctly defined with the input signal
    dft = []
    x = []
    idft = []
    new_window = tk.Toplevel(root)
    new_window.geometry("200x300")
    fold = tk.Frame(new_window)

    # Reading the file
    uploadButton = tk.Button(fold, text="Upload Signal",
                             command=lambda: read_data(x, Xn))
    uploadButton.pack(pady=10)
    dftButton = tk.Button(fold, text="dft", command=lambda: DFT(Xn, dft))
    dftButton.pack(pady=10)

    def DFT(dftList, out):
        for i in range(len(dftList)):
            k = i
            sum = 0
            for y in range(len(dftList)):
                sum += dftList[y] * \
                       cmath.exp((-1j * 2 * math.radians(180) * k * y) / len(dftList))
                if abs(sum.imag) < tolerance:
                    sum = complex(sum.real, 0)
                R = sum.real
                I = sum.imag
                R = round(sum.real, 2)
                I = round(sum.imag, 2)
                if i == 0:
                    sum = complex(0, 0)
                else:
                    sum = complex(R, I)
            out.append(sum)

            Idft = []

        for i in range(len(out)):
            k = i
            sum_val = 0

            for y in range(len(out)):
                sum_val += out[y] * \
                           cmath.exp((1j * 2 * math.pi * k * y) / len(out))

            if abs(sum_val.imag) < tolerance:
                sum_val = complex(sum_val.real, 0)

            Idft.append(round(sum_val.real / len(out), 6))
        print(Idft)

    fold.pack()


def show_message( title, message):
    messagebox.showinfo(title, message)


def display_error_message( message, duration):
    messagebox.showerror("Error", message)
    master.after(duration * 1000, lambda: close_error_message())


def close_error_message():
    master.destroy()
def perform_operation( operation):
    show_message("Operation", f"Performing {operation} operation")

root = tk.Tk()
root.geometry("200x500")
root.title("DSP")
taskOneLabel = tk.Label(root, text="Task# 6", fg="blue")
taskOneLabel.pack()
button1 = tk.Button(root, text="advance",
                    command=advance)
button1.pack(pady=10)
button2 = tk.Button(root, text="delay",
                    command=delay)
button2.pack(pady=10)
button3 = tk.Button(root, text="fold",
                    command=fold)
button3.pack(pady=10)
button4 = tk.Button(root, text="sharpining",
                    command=lambda: DerivativeSignal())
button4.pack(pady=10)
button5 = tk.Button(root, text="remove dc",
                    command=remove_dc)
button5.pack(pady=10)
button6 = tk.Button(root, text="convolve",
                    command=open_convolve_frame)
button6.pack(pady=10)
root.mainloop()
