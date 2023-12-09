import tkinter as tk
from tkinter import ttk
import numpy as np
import math
import matplotlib.pyplot as plt
from tkinter import filedialog
from functools import partial

data_file1 = []
data_file2 = []
test = []
classA = []
classB = []


def Compare_Signals(file_name, Your_indices, Your_samples):
    expected_indices = []
    expected_samples = []
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L = line.strip()
            if len(L.split(' ')) == 2:
                L = line.split(' ')
                V1 = int(L[0])
                V2 = float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
    print("Current Output Test file is: ")
    print(file_name)
    print("\n")
    if (len(expected_samples) != len(Your_samples)) and (len(expected_indices) != len(Your_indices)):
        # print("Shift_Fold_Signal Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if Your_indices[i] != expected_indices[i]:
            # print("Shift_Fold_Signal Test case failed, your signal have different indicies from the expected one")
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Correlation Test case failed, your signal have different values from the expected one")
            return
    print("Correlation Test case passed successfully")


def read_data_exact_path(classT, classtype):
    signals = []
    if classtype:
        for i in range(5):
            with open("down" + str(i + 1) + ".txt", 'r') as file:
                n1 = 251
                for _ in range(n1):
                    line = file.readline().strip()
                    if line:
                        parts = line.split()

                        signals.append(float(parts[0]))
                classT.append(signals)
                signals = []
    else:
        for i in range(5):
            with open("up" + str(i + 1) + ".txt", 'r') as file:
                n1 = 251
                for _ in range(n1):
                    line = file.readline().strip()
                    if line:
                        parts = line.split()

                        signals.append(float(parts[0]))
                classT.append(signals)
                signals = []


def read_data(signals, x):
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

                    signals.append(float(parts[x]))


def calc_correlation(signal1, signal2, normalized):
    sqr_signal1_sum = 0
    sqr_signal2_sum = 0

    correlation = []
    indecies = []
    r = 0

    for i in range(len(signal1)):
        sqr_signal1_sum += signal1[i] ** 2
        sqr_signal2_sum += signal2[i] ** 2
    for j in range(len(signal1)):
        for n in range(len(signal1)):
            r += (1 / len(signal1)) * (signal1[n] * signal2[(n + j) % len(signal1)])

        if normalized:
            result = r / ((1 / len(signal1)) * (math.sqrt(sqr_signal1_sum * sqr_signal2_sum)))
            correlation.append(round(result, 8))
        else:
            correlation.append(round(r, 8))
        indecies.append(j)
        r = 0
    if normalized:
        Compare_Signals("CorrOutput.txt", indecies, correlation)
    return correlation


def calc_time_delay(signal1, signal2, Ts):
    delay = 0
    correlation = []
    correlation = calc_correlation(signal1, signal2, False)
    lag = correlation.index(max(correlation))
    delay = lag * Ts
    print("Delay amout : ", delay)


def determine_signal_class():
    avg_A = []
    avg_B = []
    sum_A = 0
    sum_B = 0
    for i in range(len(classA[0])):
        # Calc the avrage
        for j in range(len(classA)):
            sum_A += (classA[j][i] / len(classA))
            sum_B += (classB[j][i] / len(classB))

        # Append in avg list
        avg_A.append(sum_A)
        avg_B.append(sum_B)
        sum_A = 0
        sum_B = 0
    # Calc correlation
    correlation_with_A = calc_correlation(test, avg_A, True)
    correlation_with_B = calc_correlation(test, avg_B, True)
    countA = 0
    coutnB = 0

    for i in range(len(test)):
        if correlation_with_A[i] > countA:
            countA = correlation_with_A[i]
        if correlation_with_B[i] > coutnB:
            coutnB = correlation_with_B[i]

    # print(countA, "____---____", coutnB)

    if countA > coutnB:
        print("This signal belongs to class A")
    else:
        print("This signal belongs to class B")


read_data_exact_path(classA, True)
read_data_exact_path(classB, False)

# GUI setup
app = tk.Tk()
app.title("File Upload and Functions")

frame0 = ttk.Frame(app, padding="50")
frame0.pack()

# Buttons for file uploads
upload_button_1 = tk.Button(frame0, text="Upload File 1", command=lambda: read_data(data_file1, 1))
upload_button_1.pack(pady=10)

upload_button_2 = tk.Button(frame0, text="Upload File 2", command=lambda: read_data(data_file2, 1))
upload_button_2.pack(pady=10)

upload_button_3 = tk.Button(frame0, text="Upload File 3", command=lambda: read_data(test, 0))
upload_button_3.pack(pady=10)

# Buttons for functions
function_button_1 = tk.Button(frame0, text="Function 1", command=lambda: calc_correlation(data_file1, data_file2, True))
function_button_1.pack(pady=10)

function_button_2 = tk.Button(frame0, text="Function 2",
                              command=lambda: calc_time_delay(data_file1, data_file2, 1 / 100))
function_button_2.pack(pady=10)

function_button_3 = tk.Button(frame0, text="Function 3", command=determine_signal_class)
function_button_3.pack(pady=10)

app.mainloop()
