import cmath
import tkinter as tk
import math
from tkinter import filedialog

amb = []
theta = []
tolerance = 1e-6  # Updated tolerance value


def read_data(signal):
    filename = filedialog.askopenfilename()
    if filename:
        with open(filename, 'r') as file:
            data = file.readlines()
            signal.clear()
            line_count = 0
            for line in data:
                if line_count < 3:  # Skip the first 3 lines
                    line_count += 1
                    continue
                parts = line.strip().split(' ')
                signal.append(float(parts[0]))


def perform_operation(signal1, signal2, operation):
    global out_file
    out1 = []
    out2 = []
    DFT(signal1, out1, correlation=(operation == 'correlation'))
    DFT(signal2, out2, correlation=(operation == 'correlation'))
    x3 = []

    if operation == 'correlation':
        out_file = "fastCorrelation.txt"
    elif operation == 'convolution':
        out_file = "fastConvolution.txt"

    for i in range(len(out1)):
        x3.append(out1[i] * out2[i])

    IDFT(x3, out_file)


def DFT(dftList, out, correlation=False):
    for i in range(len(dftList)):
        k = i
        sum_value = 0
        for y in range(len(dftList)):
            sum_value += dftList[y] * cmath.exp((-1j if correlation else 1j) * 2 * math.pi * k * y / len(dftList))
            if abs(sum_value.imag) < tolerance:
                sum_value = complex(sum_value.real, 0)
        if correlation:
            sum_value = complex(sum_value.real, sum_value.imag * -1)
        out.append(sum_value)
        print(f'DFT[{i}] = {sum_value}')

    for i in out:
        polar = cmath.polar(i)
        amb.append(polar[0])
        theta.append((polar[1]))
    with open("DFToutput.txt", "w") as myFile:
        for i in range(len(amb)):
            myFile.write(str(amb[i]) + ' , ' + str(theta[i]) + '\n')


def IDFT(x1, outfile):
    # Perform IDFT
    result = []
    length = len(x1)
    for i in range(length):
        k = i
        sum_value = 0
        for y in range(length):
            sum_value += x1[y] * cmath.exp((1j * 2 * math.pi * k * y) / length)
        result.append(round(sum_value.real, 2) / length)
        print(f'IDFT[{i}] = {sum_value}')

    with open(outfile, "w") as myFile:
        for i in range(len(result)):
            myFile.write(str(i) + ' ' + str(result[i]) + "\n")


def create_gui():
    root = tk.Tk()
    root.title("Signal Processing GUI")

    signal1 = []
    signal2 = []

    def upload_signal1():
        read_data(signal1)

    def upload_signal2():
        read_data(signal2)

    def fast_correlation():
        perform_operation(signal1.copy(), signal2.copy(), 'correlation')

    def fast_convolution():
        perform_operation(signal1.copy(), signal2.copy(), 'convolution')

    button_frame = tk.Frame(root)
    button_frame.pack(padx=20, pady=10)

    upload_button1 = tk.Button(button_frame, text="Upload Signal 1", command=upload_signal1)
    upload_button1.grid(row=0, column=0, padx=5, pady=5)

    upload_button2 = tk.Button(button_frame, text="Upload Signal 2", command=upload_signal2)
    upload_button2.grid(row=0, column=1, padx=5, pady=5)

    correlation_button = tk.Button(button_frame, text="Fast Correlation", command=fast_correlation)
    correlation_button.grid(row=1, column=0, padx=5, pady=5)

    convolution_button = tk.Button(button_frame, text="Fast Convolution", command=fast_convolution)
    convolution_button.grid(row=1, column=1, padx=5, pady=5)

    root.mainloop()


# Run the GUI
create_gui()
