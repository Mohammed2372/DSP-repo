import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
import math
import cmath
import compare9 as comp

time = np.linspace(0, 10, 100)


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


def read_data_new(div_x):
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as file:
            for line in file:
                number = float(line.strip())
                div_x.append(number)


global listA
listA = []
global listB
listB = []


def read_data2(classT, type):

    signals = []
    if type == "A":
        for i in range(6):
            with open("signals\Practical task 2\Practical task 2\A\ASeg"+str(i+1)+".txt", 'r') as file:
                for line in file:
                    line = file.readline().strip()
                    if line:
                        parts = line.split()

                        signals.append(float(parts[0]))
                classT.append(signals)
    else:
        for i in range(6):
            with open("signals\Practical task 2\Practical task 2\B\BSeg"+str(i+1)+".txt", 'r') as file:
                for line in file:
                    line = file.readline().strip()
                    if line:
                        parts = line.split()

                        signals.append(float(parts[0]))
                classT.append(signals)


def open_frame1_window(frame):
    x = []
    y = []

    def plot_dis():
        plt.stem(x, y)
        plt.axhline(y=0, color='r')
        plt.show()

    def plot_con():
        plt.plot(x, y, label="Continous signal")
        plt.axhline(y=0, color='r')
        plt.show()

    def combined_plot():
        plt.stem(x, y)
        plt.plot(x, y, label="Continous signal")
        plt.axhline(y=0, color='r')
        plt.legend()
        plt.show()
    new_window = tk.Toplevel(frame)
    new_window.geometry("400x300")
    frame1 = tk.Frame(new_window)
    label1 = tk.Label(frame1, text="upload your data")
    upload_button = tk.Button(
        frame1, text="Upload File", command=lambda: read_data(x, y))
    con_button = tk.Button(
        frame1, text="continous graph", command=lambda: plot_con())
    dis_button = tk.Button(frame1, text="Discrete graph",
                           command=lambda: plot_dis())
    comb_button = tk.Button(
        frame1, text="Combined graph", command=lambda: combined_plot())
    label1.pack(pady=10)
    upload_button.pack(pady=10)
    con_button.pack(pady=10)
    dis_button.pack(pady=10)
    comb_button.pack(pady=10)
    frame1.pack()


def open_frame2_window(frame):
    new_window = tk.Toplevel(frame)
    new_window.geometry("400x520")
    frame2 = tk.Frame(new_window)
    label2 = tk.Label(frame2, text="write your data")
    type = ["sin", "cos"]
    type_var = tk.StringVar(frame2)
    type_var.set("Select an option")
    amb_var = tk.IntVar(frame2)
    f_var = tk.IntVar(frame2)
    fs_var = tk.IntVar(frame2)
    ph_var = tk.IntVar(frame2)
    menu = tk.OptionMenu(frame2, type_var, *type)
    amb_label = tk.Label(frame2, text="amblitute")
    amb_entry = tk.Entry(frame2, textvariable=amb_var)
    f_label = tk.Label(frame2, text="AF")
    f_entry = tk.Entry(frame2, textvariable=f_var)
    fs_label = tk.Label(frame2, text="SF")
    fs_entry = tk.Entry(frame2, textvariable=fs_var)
    ph_label = tk.Label(frame2, text="PhaseShift")
    ph_entry = tk.Entry(frame2, textvariable=ph_var)
    label2.pack(pady=10)
    menu.pack(pady=10)
    amb_label.pack(pady=10)
    amb_entry.pack(pady=10)
    f_label.pack(pady=10)
    f_entry.pack(pady=10)
    fs_label.pack(pady=10)
    fs_entry.pack(pady=10)
    ph_label.pack(pady=10)
    ph_entry.pack(pady=10)

    def plot_sin_cos():
        global time
        F_error = False
        if fs_var.get() == 0:

            F = f_var.get()
            time = np.linspace(0, 10, 500)
        else:
            F = f_var.get() / fs_var.get()
            time = np.linspace(0, 10, (fs_var.get()*10))

            if F > 0.5:
                F_error = True
                error_label.config(text="Error: F > 0.5")
            else:
                F_error = False
                error_label.config(text="")

        if (F_error == False):
            if type_var.get() == "sin":
                signal = amb_var.get() * np.sin(2 * np.pi * F * time + ph_var.get())
            elif type_var.get() == "cos":
                signal = amb_var.get() * np.cos(2 * np.pi * F * time + ph_var.get())
            if (fs_var.get() == 0):
                plt.plot(time, signal, label=type_var.get(), color="red")
            else:
                plt.stem(time, signal, label=type_var.get(),)
            plt.axhline(y=0, color='r')
            plt.legend()
            plt.show()

    error_label = tk.Label(frame2, text="", fg="red")
    wave_button = tk.Button(frame2, text="Plot", command=plot_sin_cos)
    wave_button.pack(pady=10)
    error_label.pack(pady=10)
    frame2.pack()

# task one GUI


def taskOneFrame():
    new_window = tk.Toplevel(root)
    new_window.geometry("200x200")
    frame1 = tk.Frame(new_window)
    button1 = tk.Button(frame1, text="upload your data",
                        command=lambda: open_frame1_window(frame1))
    button1.pack(pady=20)
    button2 = tk.Button(frame1, text="write your own data",
                        command=lambda: open_frame2_window(frame1))
    button2.pack(pady=20)
    frame1.pack()

# task two functions


def multiply_frame_window(frame):
    x = []
    y = []
    new_window = tk.Toplevel(frame)
    new_window.geometry("200x150")
    multiplyFrame = tk.Frame(new_window)
    uploadButton = tk.Button(
        multiplyFrame, text="upload signal", command=lambda: read_data(x, y))
    uploadButton.pack(pady=10)
    label_val = tk.Label(multiplyFrame, text="multiblication value")
    label_val.pack()
    mult_value = tk.IntVar(multiplyFrame)
    val_entry = tk.Entry(multiplyFrame, textvariable=mult_value)
    val_entry.pack(pady=10)

    def multiply_plot(x, y):
        plt.subplot(2, 1, 1)
        plt.plot(x, y, label='orginal')
        plt.legend()
        plt.subplot(2, 1, 2)
        for i in range(len(y)):
            y[i] *= mult_value.get()
        plt.plot(x, y, label='multiplied by ' + str(mult_value.get()))
        plt.legend()
        plt.tight_layout()
        plt.show()

    plotButton = tk.Button(multiplyFrame, text="plot",
                           command=lambda: multiply_plot(x, y))
    plotButton.pack(pady=10)
    multiplyFrame.pack()


def addition_frame_window(frame):
    x1 = []
    y1 = []
    x2 = []
    y2 = []

    def addition_plot():
        global Y
        plt.subplot(2, 1, 1)
        plt.plot(x1, y1, label="signal 1")
        plt.legend()
        plt.subplot(2, 1, 2)
        plt.plot(x1, Y, label="after addition")
        plt.legend()
        plt.show()

    def first_file_upload():
        global Y
        read_data(x1, y1)
        Y = y1

    def mult_add():
        global Y
        read_data(x2, y2)
        Y = [a + b for a, b in zip(Y, y2)]

    new_window = tk.Toplevel(frame)
    new_window.geometry("200x150")
    additionFrame = tk.Frame(new_window)
    uploadButton1 = tk.Button(
        additionFrame, text="firts signal", command=lambda: first_file_upload())
    uploadButton1.pack(pady=10)
    uploadButton2 = tk.Button(
        additionFrame, text="signal to add", command=lambda: mult_add())
    uploadButton2.pack(pady=10)

    plotButton = tk.Button(additionFrame, text="plot", command=addition_plot)
    plotButton.pack(pady=10)
    additionFrame.pack()


def sub_frame_window(frame):
    x1 = []
    y1 = []
    x2 = []
    y2 = []

    def sub_plot():
        global Y
        plt.subplot(2, 1, 1)
        plt.plot(x1, y1, label="signal 1")
        plt.legend()
        plt.subplot(2, 1, 2)
        plt.plot(x1, Y, label="after addition")
        plt.legend()
        plt.show()

    def first_file_upload():
        global Y
        read_data(x1, y1)
        Y = y1

    def mult_add():
        global Y
        read_data(x2, y2)
        Y = [a - b for a, b in zip(Y, y2)]

    new_window = tk.Toplevel(frame)
    new_window.geometry("200x150")
    subFrame = tk.Frame(new_window)
    uploadButton1 = tk.Button(
        subFrame, text="first signal", command=lambda: first_file_upload())
    uploadButton1.pack(pady=10)
    uploadButton2 = tk.Button(
        subFrame, text="signal to substract from", command=lambda: mult_add())
    uploadButton2.pack(pady=10)

    plotButton = tk.Button(subFrame, text="plot", command=sub_plot)
    plotButton.pack(pady=10)
    subFrame.pack()


def sq_frame_window(frame):
    x = []
    y = []

    def sq_plot():
        Y = [a ** 2 for a in y]
        plt.subplot(2, 1, 1)
        plt.plot(x, y, label="original")
        plt.legend()
        plt.subplot(2, 1, 2)
        plt.plot(x, Y, label="squared")
        plt.legend()
        plt.show()
    new_window = tk.Toplevel(frame)
    new_window.geometry("200x150")
    sqFrame = tk.Frame(new_window)
    uploadButton = tk.Button(
        sqFrame, text="upload signal", command=lambda: read_data(x, y))
    uploadButton.pack(pady=10)
    plotButton = tk.Button(sqFrame, text="plot", command=sq_plot)
    plotButton.pack(pady=10)
    sqFrame.pack()


def shifting_frame_window(frame):
    x = []
    y = []
    new_window = tk.Toplevel(frame)
    new_window.geometry("200x150")
    shiftingFrame = tk.Frame(new_window)
    uploadButton = tk.Button(
        shiftingFrame, text="upload signal", command=lambda: read_data(x, y))
    uploadButton.pack(pady=10)
    label_val = tk.Label(shiftingFrame, text="shifting amount")
    label_val.pack()
    shifting_value = tk.IntVar(shiftingFrame)
    val_entry = tk.Entry(shiftingFrame, textvariable=shifting_value)
    val_entry.pack(pady=10)

    def shifting_plot(x, y):
        plt.subplot(2, 1, 1)
        plt.plot(x, y, label='orginal')
        plt.legend()
        plt.subplot(2, 1, 2)
        for i in range(len(x)):
            x[i] -= shifting_value.get()
        plt.plot(x, y, label='shifting by ' + str(shifting_value.get()))
        plt.legend()
        plt.tight_layout()
        plt.show()

    plotButton = tk.Button(shiftingFrame, text="plot",
                           command=lambda: shifting_plot(x, y))
    plotButton.pack(pady=10)
    shiftingFrame.pack()


def normalization_frame_window(frame):
    x = []
    y = []
    new_window = tk.Toplevel(frame)
    new_window.geometry("200x150")
    normalizationFrame = tk.Frame(new_window)
    uploadButton = tk.Button(
        normalizationFrame, text="upload signal", command=lambda: read_data(x, y))
    uploadButton.pack(pady=10)
    label_val = tk.Label(normalizationFrame, text="normalization range")
    label_val.pack()
    type = ["-1 to 1", "0 to 1"]
    type_var = tk.StringVar(normalizationFrame)
    type_var.set("Select an option")
    menu = tk.OptionMenu(normalizationFrame, type_var, *type)
    menu.pack(pady=10)

    def normalization_plot(x, y):
        plt.subplot(2, 1, 1)
        plt.plot(x, y, label='orginal')
        plt.legend()
        plt.subplot(2, 1, 2)
        if type_var.get() == "-1 to 1":
            min_value = min(y)
            max_value = max(y)
            normalized_data = [
                (2 * (x - min_value) / (max_value - min_value)) - 1 for x in y]
            y = normalized_data
        elif type_var.get() == "0 to 1":
            min_value = min(y)
            max_value = max(y)
            normalized_data = [
                (x - min_value) / (max_value - min_value) for x in y]
            y = normalized_data
        plt.plot(x, y, label='normalization range ' + type_var.get())
        plt.legend()
        plt.tight_layout()
        plt.show()

    plotButton = tk.Button(normalizationFrame, text="plot",
                           command=lambda: normalization_plot(x, y))
    plotButton.pack(pady=10)
    normalizationFrame.pack()


def accumulation_frame_window(frame):
    x = []
    y = []
    new_window = tk.Toplevel(frame)
    new_window.geometry("200x150")
    accumulationFrame = tk.Frame(new_window)
    uploadButton = tk.Button(
        accumulationFrame, text="upload signal", command=lambda: read_data(x, y))
    uploadButton.pack(pady=10)

    def accumulation_plot(x, y):
        plt.subplot(2, 1, 1)
        plt.plot(x, y, label='orginal')
        plt.legend()
        plt.subplot(2, 1, 2)
        for i in range(1, len(y)):
            y[i] += y[i-1]
        plt.plot(x, y, label='accumulation_plot')
        plt.legend()
        plt.tight_layout()
        plt.show()

    plotButton = tk.Button(accumulationFrame, text="plot",
                           command=lambda: accumulation_plot(x, y))
    plotButton.pack(pady=10)
    accumulationFrame.pack()


# task two GUI
def taskTwoFrame():
    new_window = tk.Toplevel(root)
    new_window.geometry("200x400")
    frame2 = tk.Frame(new_window)
    multiplyButton = tk.Button(
        frame2, text="multiply signals", command=lambda: multiply_frame_window(frame2))
    multiplyButton.pack(pady=10)
    additionButton = tk.Button(
        frame2, text="add signals", command=lambda: addition_frame_window(frame2))
    additionButton.pack(pady=10)
    subButton = tk.Button(
        frame2, text="subtract signals", command=lambda: sub_frame_window(frame2))
    subButton.pack(pady=10)
    sqButton = tk.Button(
        frame2, text="square signal", command=lambda: sq_frame_window(frame2))
    sqButton.pack(pady=10)
    shiftButton = tk.Button(
        frame2, text="Shifting signal", command=lambda: shifting_frame_window(frame2))
    shiftButton.pack(pady=10)
    normalizationButton = tk.Button(
        frame2, text="Normalization signal", command=lambda: normalization_frame_window(frame2))
    normalizationButton.pack(pady=10)
    accumulationButton = tk.Button(
        frame2, text="Accumulation signal", command=lambda: accumulation_frame_window(frame2))
    accumulationButton.pack(pady=10)
    frame2.pack()

# task three function (no new frame needed)


def task3_frame_window():
    global x, y, ranges, index, quan, incoded, error
    x = []
    y = []
    ranges = []
    index = []
    quan = []
    incoded = []
    error = []
    new_window = tk.Toplevel(root)
    new_window.geometry("200x300")
    task3Frame = tk.Frame(new_window)
    label_val = tk.Label(task3Frame, text="bits/levels")
    label_val.pack(pady=10)
    radioOption = tk.StringVar()
    option_menu = tk.Entry(task3Frame, textvariable=radioOption)
    option_menu.pack(pady=10)
    entry_var = tk.IntVar(task3Frame)
    entry = tk.Entry(task3Frame, textvariable=entry_var)
    entry.pack(pady=10)
    uploadButton = tk.Button(
        task3Frame, text="upload signal", command=lambda: read_data(x, y))
    uploadButton.pack(pady=10)

    def calculate_bits():
        if radioOption.get() == "bits":
            max_value = max(y)
            min_value = min(y)
            n = entry_var.get()
            levels = pow(2, n)
            lamda = (max_value - min_value) / levels
            for i in range(levels):
                midPoint = (min_value + (min_value + lamda)) / 2
                Range = [round(min_value, 3), round((min_value + lamda), 3),
                         round(midPoint, 3), i + 1]
                ranges.append(Range)
                min_value += lamda
            for i in y:
                for j in ranges:
                    if i >= j[0]:
                        if i <= j[1]:
                            quan.append(j[2])
                            index.append(j[3])
                            break
            for i in range(len(y)):
                error.append(round(quan[i] - y[i], 3))
            for i in index:
                binary_representation = format(i - 1, f'0{n}b')
                incoded.append(binary_representation)
            print(incoded)
            print(quan)
        else:
            max_value = max(y)
            min_value = min(y)
            levels = entry_var.get()
            lamda = (max_value - min_value) / levels
            for i in range(levels):
                midPoint = (min_value + (min_value + lamda)) / 2
                Range = [round(min_value, 3), round((min_value + lamda), 3),
                         round(midPoint, 3), i + 1]
                ranges.append(Range)
                min_value += lamda
            for i in y:
                for j in ranges:
                    if i >= j[0]:
                        if i <= j[1]:
                            quan.append(j[2])
                            index.append(j[3])
            for i in range(len(y)):
                error.append(round(quan[i] - y[i], 3))
            for i in index:
                num_digits = math.ceil(math.log(levels, 2))
                binary_representation = format(
                    i - 1, f'0{num_digits}b')
                incoded.append(binary_representation)
            print(index)
            print(incoded)
            print(quan)
            print(error)
    calculateButton = tk.Button(
        task3Frame, text="Calculate", command=calculate_bits)
    calculateButton.pack(pady=10)
    task3Frame.pack()

# task 4 functions


amb = []
theta = []
# DFT

tolerance = 1e-10


def DFT(dftList, out):
    for i in range(len(dftList)):
        k = i
        sum = 0
        for y in range(len(dftList)):
            sum += dftList[y] * \
                cmath.exp((-1j * 2*math.radians(180)*k*y)/len(dftList))
            if abs(sum.imag) < tolerance:
                sum = complex(sum.real, 0)
            R = sum.real
            I = sum.imag
            R = round(sum.real, 2)
            I = round(sum.imag, 2)
            sum = complex(R, I)
        out.append(sum)
    for i in out:
        polar = cmath.polar(i)
        amb.append(polar[0])
        theta.append((polar[1]))
    with open("DFTotput.txt", "w") as myFile:
        for i in range(len(amb)):
            myFile.write(str(amb[i])+' , '+str(theta[i])+'\n')


out = []
omega = 0


def DFT_Window(frame):
    Xn = []
    x = []
    new_window = tk.Toplevel(frame)
    new_window.geometry("200x600")
    DFTFrame = tk.Frame(new_window)
    label = tk.Label(DFTFrame, text="DFT Window")
    label.pack()
    uploadButton = tk.Button(
        DFTFrame, text="upload signal", command=lambda: read_data(x, Xn))
    DFTBtn = tk.Button(DFTFrame, text="Calc", command=lambda: DFT(Xn, out))
    entryVar = tk.IntVar(DFTFrame)
    labelFs = tk.Label(DFTFrame, text="Enter Fs")
    uploadButton.pack(pady=10)
    DFTBtn.pack(pady=10)
    entry = tk.Entry(DFTFrame, textvariable=entryVar)
    labelFs.pack(pady=10)
    entry.pack(pady=10)
    mlabel = tk.Label(DFTFrame, text="modify phase or amp")
    mlabel.pack(pady=10)
    type = ["theta", "amb"]
    type_var = tk.StringVar(DFTFrame)
    menu = tk.OptionMenu(DFTFrame, type_var, *type)
    menu.pack(pady=10)
    ilabel = tk.Label(DFTFrame, text="index")
    ilabel.pack(pady=10)
    iVar = tk.IntVar(DFTFrame)
    ientry = tk.Entry(DFTFrame, textvariable=iVar)
    ientry.pack(pady=10)
    ilabel = tk.Label(DFTFrame, text="value")
    ilabel.pack(pady=10)
    vVar = tk.StringVar(DFTFrame)
    ventry = tk.Entry(DFTFrame, textvariable=vVar)
    ventry.pack(pady=10)

    def modify():
        if type_var.get() == "amb":
            amb[iVar.get()] = vVar.get()
            R = float(vVar.get()) * math.cos(theta[iVar.get()])
            I = float(vVar.get()) * math.sin(theta[iVar.get()])
            if abs(I) < tolerance:
                I = 0
            R = round(R, 2)
            I = round(I, 2)
            out[iVar.get()] = complex(R, I)
            with open("DFTotput.txt", "w") as myFile:
                for i in range(len(amb)):
                    myFile.write(str(amb[i])+' , '+str(theta[i])+'\n')
        else:
            theta[iVar.get()] = float(vVar.get())
            R = float(vVar.get()) * math.cos(theta[iVar.get()])
            I = float(vVar.get()) * math.sin(theta[iVar.get()])
            if abs(I) < tolerance:
                I = 0
            R = round(R, 2)
            I = round(I, 2)
            out[iVar.get()] = complex(R, I)
            with open("DFTotput.txt", "w") as myFile:
                for i in range(len(amb)):
                    myFile.write(str(amb[i])+' , '+str(theta[i])+'\n')
        print(out)
    mbutton = tk.Button(DFTFrame, text="modify", command=lambda: modify())
    mbutton.pack(pady=10)

    def plot():
        omega = 2*math.pi/((1/entryVar.get())*len(Xn))
        fy = []
        thta = []
        for i in range(len(Xn)):
            fy.append(str(omega*(i+1)))
        for i in theta:
            thta.append(math.degrees(i))
        plt.subplot(2, 1, 1)
        plt.stem(fy, amb)
        plt.subplot(2, 1, 2)
        plt.stem(fy, thta)
        plt.axhline(y=0, color='r')
        plt.show()

    plotBtn = tk.Button(DFTFrame, text="plot", command=lambda: plot())
    plotBtn.pack(pady=10)
    DFTFrame.pack()


def IDFT_Window(frame):
    Xn = []
    x = []
    Idft = []
    Idfts = []
    index = []
    new_window = tk.Toplevel(frame)
    new_window.geometry("200x300")
    DFTFrame = tk.Frame(new_window)
    label = tk.Label(DFTFrame, text="IDFT Window")
    label.pack()
    uploadButton = tk.Button(
        DFTFrame, text="upload signal", command=lambda: read_data(x, Xn))
    uploadButton.pack(pady=10)

    def writeFile():
        for i in range(len(Xn)):
            temp = cmath.rect(x[i], Xn[i])
            Idfts.append(complex(round(temp.real, 0), round(temp.imag, 0)))
        # print(Idfts)
        for i in range(len(Xn)):
            k = i
            sum = 0
            for y in range(len(Xn)):
                sum += Idfts[y] * \
                    cmath.exp((1j * 2*math.radians(180)*k*y)/len(Xn))
                if abs(sum.imag) < tolerance:
                    sum = complex(sum.real, 0)
                R = sum.real
                I = sum.imag
                R = round(sum.real, 0)
                I = round(sum.imag, 0)
            Idft.append(round(sum.real, 0)/len(Xn))
            sum = 0
        with open("IDFToutput.txt", "w") as myFile:
            for i in range(len(Xn)):
                index.append(i)
                myFile.write(str(i) + ' ' + str(round(Idft[i], 0))+'\n')

    def plot():
        print(Idft)
        plt.stem(index, Idft)
        plt.show()
    IDFTBtn = tk.Button(DFTFrame, text="Write", command=lambda: writeFile())
    IDFTBtn.pack(pady=10)
    DFTFrame.pack()
    plotBtn = tk.Button(DFTFrame, text="plot", command=lambda: plot())
    plotBtn.pack(pady=10)

# task four GUI


def task4_frame_window():
    new_window = tk.Toplevel(root)
    new_window.geometry("200x400")
    frame3 = tk.Frame(new_window)
    dftBtn = tk.Button(frame3, text="DFT", command=lambda: DFT_Window(frame3))
    dftBtn.pack(pady=10)
    idftBtn = tk.Button(frame3, text="IDFT",
                        command=lambda: IDFT_Window(frame3))
    idftBtn.pack(pady=10)
    frame3.pack()

# task five funcrions


def DCT(frame):
    x = []
    y = []
    DCTList = []
    new_window = tk.Toplevel(frame)
    new_window.geometry("200x300")
    DCTFrame = tk.Frame(new_window)
    uploadButton = tk.Button(
        DCTFrame, text="upload signal", command=lambda: read_data(x, y))
    uploadButton.pack(pady=10)
    for x in range(len(y)):
        k = 0
        for j in range(len(y)):
            k += y[j] * math.cos((math.pi / (4 * len(y))) *
                                 (2 * j - 1) * (2 * x - 1))
        k *= math.sqrt(2 / len(y))
        DCTList.append(k)
    print(DCTList)
    DCTFrame.pack()
# task five GUI


def task5_frame_window():
    new_window = tk.Toplevel(root)
    new_window.geometry("200x400")
    frame5 = tk.Frame(new_window)
    dftBtn = tk.Button(frame5, text="DCT", command=lambda: DCT(frame5))
    dftBtn.pack(pady=10)
    # idftBtn = tk.Button(frame4, text="Remove DC",
    #                     command=lambda: removeDC(frame4))
    # idftBtn.pack(pady=10)
    frame5.pack()


def fast_correlatoin(frame):
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    new_window = tk.Toplevel(frame)
    new_window.geometry("200x300")
    FastFrame = tk.Frame(new_window)
    uploadButton1 = tk.Button(
        FastFrame, text="upload signal", command=lambda: read_data(x1, y1))
    uploadButton2 = tk.Button(
        FastFrame, text="upload signal", command=lambda: read_data(x2, y2))

    len1 = len(y1)
    len2 = len(y2)

    # if len1 < len2:
    #     y1 += [0] * (len2 - len1)
    # elif len1 > len2:
    #     y2 += [0] * (len1 - len2)

    def calc_fast_correlation():
        nonlocal y1, y2
        out1 = []
        out2 = []
        DFT(y1, out1)
        DFT(y2, out2)
        x1 = out1
        x2 = out2
        x3 = []
        for i in x1:
            i = complex(i.real, i.imag * -1)
        for i in range(len(x1)):
            x3.append(x1[i]*x2[i])
        # IDFT
        result = []
        for i in range(len(x3)):
            k = i
            sum = 0
            for y in range(len(x3)):
                sum += x3[y] * \
                    cmath.exp((1j * 2*math.radians(180)*k*y)/len(x3))
                if abs(sum.imag) < tolerance:
                    sum = complex(sum.real, 0)
                R = sum.real
                I = sum.imag
                R = round(sum.real, 0)
                I = round(sum.imag, 0)
            result.append(round(sum.real, 0)/len(x3))
            sum = 0
        for i in range(len(result)):
            # print(result[i])
            result[i] = result[i] / len(result)
            print(result[i])
        with open("fastCorelation.txt", "w") as myFile:
            for i in range(len(result)):
                myFile.write(str(i) + ' ' +
                             str(result[i]) + "\n")

    calcBtn = tk.Button(FastFrame, text="calc",
                        command=lambda: calc_fast_correlation())
    uploadButton1.pack(pady=10)
    uploadButton2.pack(pady=10)
    calcBtn.pack(pady=10)
    FastFrame.pack()


def fast_convolution(frame):
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    new_window = tk.Toplevel(frame)
    new_window.geometry("200x300")
    FastFrame = tk.Frame(new_window)
    uploadButton1 = tk.Button(
        FastFrame, text="upload signal", command=lambda: read_data(x1, y1))
    uploadButton2 = tk.Button(
        FastFrame, text="upload signal", command=lambda: read_data(x2, y2))
    len1 = len(y1)
    len2 = len(y2)

    if len1 < len2:
        y1 += [0] * (len2 - len1)
    elif len1 > len2:
        y2 += [0] * (len1 - len2)

    def calc_fast_convolution():
        nonlocal y1, y2
        out1 = []
        out2 = []
        DFT(y1, out1)
        DFT(y2, out2)
        x1 = out1
        x2 = out2
        x3 = []
        for i in range(len(x1)):
            x3.append(x1[i]*x2[i])
        # IDFT
        result = []
        for i in range(len(x3)):
            k = i
            sum = 0
            for y in range(len(x3)):
                sum += x3[y] * \
                    cmath.exp((1j * 2*math.radians(180)*k*y)/len(x3))
                if abs(sum.imag) < tolerance:
                    sum = complex(sum.real, 0)
                R = sum.real
                I = sum.imag
                R = round(sum.real, 0)
                I = round(sum.imag, 0)
            result.append(round(sum.real, 0)/len(x3))
            sum = 0
        with open("fastConvolution.txt", "w") as myFile:
            for i in range(len(result)):
                myFile.write(str(i) + ' ' +
                             str(result[len(result) - i - 1]) + "\n")

    calcBtn = tk.Button(FastFrame, text="calc",
                        command=lambda: calc_fast_convolution())
    uploadButton1.pack(pady=10)
    uploadButton2.pack(pady=10)
    calcBtn.pack(pady=10)
    FastFrame.pack()


def task8_frame_window():
    new_window = tk.Toplevel(root)
    new_window.geometry("200x400")
    frame8 = tk.Frame(new_window)
    correlationBtn = tk.Button(
        frame8, text="fast correlation", command=lambda: fast_correlatoin(frame8))
    correlationBtn.pack(pady=10)
    convolutionBtn = tk.Button(
        frame8, text="fast convolution", command=lambda: fast_convolution(frame8))
    convolutionBtn.pack(pady=10)
    frame8.pack()


def FIR(frame):
    result = []
    x = []
    xList = []
    ecg = []
    resultFilterd = []
    new_window = tk.Toplevel(frame)
    new_window.geometry("200x800")
    FIR_Frame = tk.Frame(new_window)
    type_var = tk.StringVar(FIR_Frame)
    fs = tk.IntVar(FIR_Frame)
    stop = tk.IntVar(FIR_Frame)
    f1 = tk.IntVar(FIR_Frame)
    f2 = tk.IntVar(FIR_Frame)
    trans = tk.IntVar(FIR_Frame)
    type_var.set("Select an option")
    type = ["low-pass", "high-pass", "band-pass", "band-stop"]
    type_label = tk.Label(FIR_Frame, text="filter type")
    type_label.pack(pady=10)
    menu = tk.OptionMenu(FIR_Frame, type_var, *type)
    menu.pack(pady=10)
    fs_label = tk.Label(FIR_Frame, text="FS")
    fs_label.pack(pady=10)
    fs_entry = tk.Entry(FIR_Frame, textvariable=fs)
    fs_entry.pack(pady=10)
    stop_label = tk.Label(FIR_Frame, text="stop")
    stop_label.pack(pady=10)
    stop_entry = tk.Entry(FIR_Frame, textvariable=stop)
    stop_entry.pack(pady=10)
    f1_label = tk.Label(FIR_Frame, text="FC/F1")
    f1_label.pack(pady=10)
    f1_entry = tk.Entry(FIR_Frame, textvariable=f1)
    f1_entry.pack(pady=10)
    f2_label = tk.Label(FIR_Frame, text="F2(in case band pass or stop)")
    f2_label.pack(pady=10)
    f2_entry = tk.Entry(FIR_Frame, textvariable=f2)
    f2_entry.pack(pady=10)
    trans_label = tk.Label(FIR_Frame, text="Transition")
    trans_label.pack(pady=10)
    trans_entry = tk.Entry(FIR_Frame, textvariable=trans)
    trans_entry.pack(pady=10)
    uploadButton1 = tk.Button(
        FIR_Frame, text="upload signal", command=lambda: read_data(x, ecg))

    def plot(x, y):
        plt.plot(x, y, label="filterd ecg")
        plt.show()

    def window_calc(Wtype, n, N):
        match Wtype:
            case "Rectangular":
                return 1
            case "Hanning":
                return 0.5 + (0.5*math.cos((2*math.pi*n)/N))
            case "Hamming":
                return 0.54 + (0.46*math.cos((2*math.pi*n)/N))
            case "Blackman":
                return 0.42 + (0.5*math.cos((2*math.pi*n)/(N-1))) + (0.08*math.cos((4*math.pi*n)/(N-1)))

    def calc(Ftype, fs, stop, f1, f2, trans, result, ecg, filterd):
        Wtype = ""
        n = 0
        N = 0
        normalized_trans = trans / fs

        if (stop <= 21):
            Wtype = "Rectangular"
            N = round(0.9/normalized_trans, 0)
        elif (stop <= 44):
            Wtype = "Hanning"
            N = round(3.1/normalized_trans, 0)
        elif (stop <= 53):
            Wtype = "Hamming"
            N = round(3.3/normalized_trans, 0)
        elif (stop <= 74 or stop > 74):
            Wtype = "Blackman"
            N = round(5.5/normalized_trans, 0)

        if (N % 2 == 0):
            N = N + 1
        n = -((N-1)/2)

        match Ftype:
            case "low-pass":
                f1 = (f1 + (trans/2))/fs
            case "high-pass":
                f1 = (f1 - (trans/2))/fs
            case "band-pass":
                f1 = (f1 - (trans/2))/fs
                f2 = (f2 + (trans/2))/fs
            case "band-stop":
                f1 = (f1 + (trans/2))/fs
                f2 = (f2 - (trans/2))/fs
        for i in range(int(N)):
            res = 0
            match Ftype:
                case "low-pass":
                    if (n == 0):
                        res = (2 * f1) * window_calc(Wtype, n, N)
                    else:
                        res = (2 * f1 * ((math.sin(n*2*math.pi*f1)) /
                                         (n*2*math.pi*f1))) * window_calc(Wtype, n, N)
                case "high-pass":
                    if (n == 0):
                        res = (1-2*f1) * window_calc(Wtype, n, N)
                    else:
                        res = (-2 * f1 * (math.sin(n*2*math.pi*f1) /
                                          (n*2*math.pi*f1)))*window_calc(Wtype, n, N)
                case "band-pass":
                    if (n == 0):
                        res = (2*(f2-f1)) * window_calc(Wtype, n, N)
                    else:
                        res = ((2*f2*(math.sin(n*2*math.pi*f2)/(n*2*math.pi*f2)))-(2*f1 *
                                                                                   (math.sin(n*2*math.pi*f1)/(n*2*math.pi*f1))))*window_calc(Wtype, n, N)
                case "band-stop":
                    if (n == 0):
                        res = (1 - 2*(f2-f1))*window_calc(Wtype, n, N)
                    else:
                        res = -((2*f2*(math.sin(n*2*math.pi*f2)/(n*2*math.pi*f2)))-(2*f1 *
                                (math.sin(n*2*math.pi*f1)/(n*2*math.pi*f1))))*window_calc(Wtype, n, N)
            result.append(res)
            n = n+1
        with open("filter.txt", "w") as myFile:
            for i in range(len(result)):
                myFile.write(str(int(i - ((N-1)/2))) + ' ' +
                             str(result[i]) + "\n")
        match Ftype:
            case "low-pass":
                comp.Compare_Signals(
                    "signals\FIR test cases\FIR test cases\Testcase 1\LPFCoefficients.txt", [], result)
            case "high-pass":
                comp.Compare_Signals(
                    "signals\FIR test cases\FIR test cases\Testcase 3\HPFCoefficients.txt", [], result)
            case "band-pass":
                comp.Compare_Signals(
                    "D:\DSP\signals\FIR test cases\FIR test cases\Testcase 5\BPFCoefficients.txt", [], result)
            case "band-stop":
                comp.Compare_Signals(
                    "signals\FIR test cases\FIR test cases\Testcase 7\BSFCoefficients.txt", [], result)

        if len(ecg) != 0:
            leng = len(ecg) + len(result) - 1
            result_i = [0] * leng
            signal_padded = [0] * (len(result) - 1) + \
                ecg + [0] * (len(result) - 1)
            for i in range(leng):
                for j in range(len(result)):
                    result_i[i] += signal_padded[i -
                                                 j + len(result) - 1] * result[j]
                filterd.append(result_i[i])
            index = -((N - 1) / 2)
            for i in range(len(filterd)):
                xList.append(index)
                index += 1

            match Ftype:
                case "low-pass":
                    comp.Compare_Signals(
                        "signals\FIR test cases\FIR test cases\Testcase 2\ecg_low_pass_filtered.txt", [], filterd)
                case "high-pass":
                    comp.Compare_Signals(
                        "signals\FIR test cases\FIR test cases\Testcase 4\ecg_high_pass_filtered.txt", [], filterd)
                case "band-pass":
                    comp.Compare_Signals(
                        "signals\FIR test cases\FIR test cases\Testcase 6\ecg_band_pass_filtered.txt", [], filterd)
                case "band-stop":
                    comp.Compare_Signals(
                        "signals\FIR test cases\FIR test cases\Testcase 8\ecg_band_stop_filtered.txt", [], filterd)

    calcBtn = tk.Button(FIR_Frame, text="calc", command=lambda: calc(
        type_var.get(), fs.get(), stop.get(), f1.get(), f2.get(), trans.get(), result, ecg, resultFilterd))
    uploadButton1.pack(pady=10)
    calcBtn.pack(pady=10)
    plotBtn = tk.Button(FIR_Frame, text="plot ecg",
                        command=lambda: plot(xList, resultFilterd))
    plotBtn.pack()
    M = tk.IntVar(FIR_Frame)
    L = tk.IntVar(FIR_Frame)
    MLabel = tk.Label(FIR_Frame, text="M")
    LLabel = tk.Label(FIR_Frame, text="L")
    M_entry = tk.Entry(FIR_Frame, textvariable=M)
    L_entry = tk.Entry(FIR_Frame, textvariable=L)
    MLabel.pack()
    M_entry.pack(pady=10)
    LLabel.pack()
    L_entry.pack(pady=10)

    def upSampling(data, factor):
        zeros_num = factor - 1
        result = []
        for i in range(len(data)):
            result.append(data[i])
            if i != len(data) - 1:
                for j in range(zeros_num):
                    result.append(0)
        return result

    def downSampling(data, factor):
        result = []
        for i in range(len(data)):
            if (i % factor == 0):
                result.append(data[i])
        return result

    def sampling():
        upS = []
        downS = []
        newRes = []
        newResFilterd = []
        if M.get() > 0 and L.get() > 0:
            upS = upSampling(ecg, L.get())
            calc(type_var.get(), fs.get(), stop.get(), f1.get(),
                 f2.get(), trans.get(), newRes, upS, newResFilterd)
            downS = downSampling(newResFilterd, M.get())
            print(len(downS))
            print(downS)
            print("sampling test")
            comp.Compare_Signals(
                "signals\Sampling test cases\Sampling test cases\Testcase 3\Sampling_Up_Down.txt", [], downS)
        if L.get() == 0 and M.get() > 0:
            calc(type_var.get(), fs.get(), stop.get(), f1.get(),
                 f2.get(), trans.get(), newRes, ecg, newResFilterd)
            downS = downSampling(newResFilterd, M.get())
            print("sampling test")
            comp.Compare_Signals(
                "signals\Sampling test cases\Sampling test cases\Testcase 1\Sampling_Down.txt", [], downS)
        if M.get() == 0 and L.get() > 0:
            upS = upSampling(ecg, L.get())
            calc(type_var.get(), fs.get(), stop.get(), f1.get(),
                 f2.get(), trans.get(), newRes, upS, newResFilterd)
            print("sampling test")
            comp.Compare_Signals(
                "signals\Sampling test cases\Sampling test cases\Testcase 2\Sampling_Up.txt", [], newResFilterd)
    samBtn = tk.Button(FIR_Frame, text="sampling", command=lambda: sampling())
    samBtn.pack()
    FIR_Frame.pack()


def task9_frame_window():
    new_window = tk.Toplevel(root)
    new_window.geometry("200x200")
    frame9 = tk.Frame(new_window)
    FIR_Btn = tk.Button(
        frame9, text="FIR", command=lambda: FIR(frame9))
    FIR_Btn.pack(pady=60)
    frame9.pack()


samples = 0


def window_calc(Wtype, n, N):
    match Wtype:
        case "Rectangular":
            return 1
        case "Hanning":
            return 0.5 + (0.5*math.cos((2*math.pi*n)/N))
        case "Hamming":
            return 0.54 + (0.46*math.cos((2*math.pi*n)/N))
        case "Blackman":
            return 0.42 + (0.5*math.cos((2*math.pi*n)/(N-1))) + (0.08*math.cos((4*math.pi*n)/(N-1)))


def calc(Ftype, fs, stop, f1, f2, trans, result, ecg, filterd):
    Wtype = ""
    n = 0
    N = 0
    normalized_trans = trans / fs

    if (stop <= 21):
        Wtype = "Rectangular"
        N = round(0.9/normalized_trans, 0)
    elif (stop <= 44):
        Wtype = "Hanning"
        N = round(3.1/normalized_trans, 0)
    elif (stop <= 53):
        Wtype = "Hamming"
        N = round(3.3/normalized_trans, 0)
    elif (stop <= 74 or stop > 74):
        Wtype = "Blackman"
        N = round(5.5/normalized_trans, 0)

    if (N % 2 == 0):
        N = N + 1
    n = -((N-1)/2)

    match Ftype:
        case "low-pass":
            f1 = (f1 + (trans/2))/fs
        case "high-pass":
            f1 = (f1 - (trans/2))/fs
        case "band-pass":
            f1 = (f1 - (trans/2))/fs
            f2 = (f2 + (trans/2))/fs
        case "band-stop":
            f1 = (f1 + (trans/2))/fs
            f2 = (f2 - (trans/2))/fs
    for i in range(int(N)):
        res = 0
        match Ftype:
            case "low-pass":
                if (n == 0):
                    res = (2 * f1) * window_calc(Wtype, n, N)
                else:
                    res = (2 * f1 * ((math.sin(n*2*math.pi*f1)) /
                                     (n*2*math.pi*f1))) * window_calc(Wtype, n, N)
            case "high-pass":
                if (n == 0):
                    res = (1-2*f1) * window_calc(Wtype, n, N)
                else:
                    res = (-2 * f1 * (math.sin(n*2*math.pi*f1) /
                                      (n*2*math.pi*f1)))*window_calc(Wtype, n, N)
            case "band-pass":
                if (n == 0):
                    res = (2*(f2-f1)) * window_calc(Wtype, n, N)
                else:
                    res = ((2*f2*(math.sin(n*2*math.pi*f2)/(n*2*math.pi*f2)))-(2*f1 *
                                                                               (math.sin(n*2*math.pi*f1)/(n*2*math.pi*f1))))*window_calc(Wtype, n, N)
            case "band-stop":
                if (n == 0):
                    res = (1 - 2*(f2-f1))*window_calc(Wtype, n, N)
                else:
                    res = -((2*f2*(math.sin(n*2*math.pi*f2)/(n*2*math.pi*f2)))-(2*f1 *
                            (math.sin(n*2*math.pi*f1)/(n*2*math.pi*f1))))*window_calc(Wtype, n, N)
        result.append(res)
        n = n+1
    samples = N
    if len(ecg) != 0:
        leng = len(ecg) + len(result) - 1
        result_i = [0] * leng
        signal_padded = [0] * (len(result) - 1) + \
            ecg + [0] * (len(result) - 1)
        for i in range(leng):
            for j in range(len(result)):
                result_i[i] += signal_padded[i -
                                             j + len(result) - 1] * result[j]
            filterd.append(result_i[i])


def upSampling(data, factor):
    zeros_num = factor - 1
    result = []
    for i in range(len(data)):
        result.append(data[i])
        if i != len(data) - 1:
            for j in range(zeros_num):
                result.append(0)
    return result


def downSampling(data, factor):
    result = []
    for i in range(len(data)):
        if (i % factor == 0):
            result.append(data[i])
    return result


def calc_correlation(signalA, signalB, normalized):
    sqr_signalA_sum = 0
    sqr_signalB_sum = 0

    correlation = []
    indecies = []
    r = 0

    for i in range(len(signalA)):

        sqr_signalA_sum += signalA[i]**2
        sqr_signalB_sum += signalB[i]**2
    for j in range(len(signalA)):
        for n in range(len(signalA)):
            r += (1/len(signalA))*(signalA[n]*signalB[(n+j) % len(signalA)])

        if normalized == True:
            result = r/((1/len(signalA)) *
                        (math.sqrt(sqr_signalA_sum*sqr_signalB_sum)))
            correlation.append(round(result, 8))
        else:
            correlation.append(r)
        indecies.append(j)
        r = 0
    if normalized == True:
        comp.Compare_Signals("CorrOutput.txt", indecies, correlation)

    return correlation


def task10_frame_window():
    new_window = tk.Toplevel(root)
    new_window.geometry("200x700")
    frame10 = tk.Frame(new_window)
    minF = tk.IntVar(frame10)
    maxF = tk.IntVar(frame10)
    Fs = tk.IntVar(frame10)
    newFs = tk.IntVar(frame10)

    minFLabel = tk.Label(frame10, text="minF")
    maxFLabel = tk.Label(frame10, text="maxF")
    fsLabel = tk.Label(frame10, text="FS")
    newfsFLabel = tk.Label(frame10, text="newFS")

    minFEntry = tk.Entry(frame10, textvariable=minF)
    minFLabel.pack(pady=5)
    minFEntry.pack(pady=5)
    maxFEntry = tk.Entry(frame10, textvariable=maxF)
    maxFLabel.pack(pady=5)
    maxFEntry.pack(pady=5)
    fsEntry = tk.Entry(frame10, textvariable=Fs)
    fsLabel.pack(pady=5)
    fsEntry.pack(pady=5)
    newfsEntry = tk.Entry(frame10, textvariable=newFs)
    newfsFLabel.pack(pady=5)
    newfsEntry.pack(pady=5)
    filterd = []
    filterdA = []
    filterdB = []
    test = []
    filter = []
    filterA = []
    filterB = []
    correlation = []
    correlationA = []
    correlationB = []
    DCT = []
    DCT_A = []
    DCT_B = []
    newCor = []
    newCorA = []
    newCorB = []
    uploadButton1 = tk.Button(
        frame10, text="upload signal", command=lambda: read_data_new(test))
    uploadButton1.pack(pady=5)

    uploadA = tk.Button(
        frame10, text="upload A", command=lambda: read_data2(listA, "A"))
    uploadA.pack(pady=5)

    uploadB = tk.Button(
        frame10, text="upload B", command=lambda: read_data2(listB, "B"))
    uploadB.pack(pady=5)

    def display_original(y):
        time = np.linspace(0, 100, len(y))
        plt.plot(time, y, label="original ecg")
        plt.legend()
        plt.show()

    def calcClass():
        avg_A = []
        sum_A = 0
        for i in range(len(listA[0])):
            # Calc the avrage
            for j in range(len(listA)):
                sum_A += (listA[j][i]/len(listA))

            # Append in avg list
            avg_A.append(sum_A)
        nonlocal filterdA
        calc("band-pass", Fs.get(), 50, minF.get(),
             maxF.get(), 500, filterA, avg_A, filterdA)
        if newFs.get() / maxF.get() <= 0.5:
            if (newFs.get() > Fs.get()):
                filterdA = upSampling(filterdA, newFs.get() / Fs.get())
            else:
                filterdA = downSampling(filterdA, Fs.get() / newFs.get())
        before = np.array(filterdA)
        after = before - np.mean(before)
        min_value = min(after)
        max_value = max(after)
        normalized_data = [
            (2 * (x - min_value) / (max_value - min_value)) - 1 for x in after]

        sqr_signalA_sum1 = 0
        sqr_signalA_sum2 = 0

        r = 0

        for i in range(len(normalized_data)):

            sqr_signalA_sum1 += normalized_data[i]**2
            sqr_signalA_sum2 += normalized_data[i]**2

        for j in range(len(normalized_data)):
            nonlocal correlationA
            for n in range(len(normalized_data)):
                r += (1/len(normalized_data)) * \
                    (normalized_data[n]*normalized_data[(n+j) %
                     len(normalized_data)])

            correlationA.append(r)
            r = 0
        for i in range(int(len(correlationA)/8)):
            newCorA.append(correlationA[i])
        NDCT = len(newCorA)

        for x in range(NDCT):
            k = 0
            for y in range(NDCT):
                k += newCorA[y] * \
                    math.cos((math.pi / (4 * NDCT)) *
                             (2 * y - 1) * (2 * x - 1))
            k *= math.sqrt(2 / NDCT)
            DCT_A.append(k)
        print(len(DCT_A))

        avg_B = []
        sum_B = 0
        for i in range(len(listB[0])):
            # Calc the avrage
            for j in range(len(listB)):
                sum_B += (listB[j][i]/len(listB))

            # Append in avg list
            avg_B.append(sum_B)

        nonlocal filterdB
        calc("band-pass", Fs.get(), 50, minF.get(),
             maxF.get(), 500, filterB, avg_B, filterdB)
        if newFs.get() / maxF.get() <= 0.5:
            if (newFs.get() > Fs.get()):
                filterdB = upSampling(filterdB, newFs.get() / Fs.get())
            else:
                filterdB = downSampling(filterdB, Fs.get() / newFs.get())
        before = np.array(filterdB)
        after = before - np.mean(before)
        min_value = min(after)
        max_value = max(after)
        normalized_data = [
            (2 * (x - min_value) / (max_value - min_value)) - 1 for x in after]

        sqr_signalA_sum1 = 0
        sqr_signalA_sum2 = 0

        r = 0

        for i in range(len(normalized_data)):

            sqr_signalA_sum1 += normalized_data[i]**2
            sqr_signalA_sum2 += normalized_data[i]**2

        for j in range(len(normalized_data)):
            nonlocal correlationB
            for n in range(len(normalized_data)):
                r += (1/len(normalized_data)) * \
                    (normalized_data[n]*normalized_data[(n+j) %
                     len(normalized_data)])

            correlationB.append(r)
            r = 0
        for i in range(int(len(correlationB)/8)):
            newCorB.append(correlationB[i])
        NDCT = len(newCorB)

        for x in range(NDCT):
            k = 0
            for y in range(NDCT):
                k += newCorB[y] * \
                    math.cos((math.pi / (4 * NDCT)) *
                             (2 * y - 1) * (2 * x - 1))
            k *= math.sqrt(2 / NDCT)
            DCT_B.append(k)

        nonlocal filterd
        calc("band-pass", Fs.get(), 50, minF.get(),
             maxF.get(), 500, filter, test, filterd)
        if newFs.get() / maxF.get() <= 0.5:
            if (newFs.get() > Fs.get()):
                filterd = upSampling(filterd, newFs.get() / Fs.get())
            else:
                filterd = downSampling(filterd, Fs.get() / newFs.get())
        before = np.array(filterd)
        after = before - np.mean(before)
        min_value = min(after)
        max_value = max(after)
        normalized_data = [
            (2 * (x - min_value) / (max_value - min_value)) - 1 for x in after]

        sqr_signalA_sum1 = 0
        sqr_signalA_sum2 = 0

        r = 0

        for i in range(len(normalized_data)):

            sqr_signalA_sum1 += normalized_data[i]**2
            sqr_signalA_sum2 += normalized_data[i]**2

        for j in range(len(normalized_data)):
            nonlocal correlation
            for n in range(len(normalized_data)):
                r += (1/len(normalized_data)) * \
                    (normalized_data[n]*normalized_data[(n+j) %
                     len(normalized_data)])

            correlation.append(r)
            r = 0
        for i in range(int(len(correlation)/8)):
            newCor.append(correlation[i])
        NDCT = len(newCor)

        for x in range(NDCT):
            k = 0
            for y in range(NDCT):
                k += newCor[y] * \
                    math.cos((math.pi / (4 * NDCT)) *
                             (2 * y - 1) * (2 * x - 1))
            k *= math.sqrt(2 / NDCT)
            DCT.append(k)

        corA = calc_correlation(DCT, DCT_A, False)
        corB = calc_correlation(DCT, DCT_B, False)
        countA = 0
        coutnB = 0
    # Classify the test
        for i in range(len(corA)):
            if corA[i] > corB[i]:
                countA += 1
            elif corB[i] > corA[i]:
                coutnB += 1
        if (countA > coutnB):
            print("This signal belongs to class A")
        else:
            print("This signal belongs to class B")

    def calcClassA():
        avg_A = []
        sum_A = 0
        for i in range(len(listA[0])):
            # Calc the avrage
            for j in range(len(listA)):
                sum_A += (listA[j][i]/len(listA))

            # Append in avg list
            avg_A.append(sum_A)
        nonlocal filterdA
        calc("band-pass", Fs.get(), 50, minF.get(),
             maxF.get(), 500, filterA, avg_A, filterdA)
        if newFs.get() / maxF.get() <= 0.5:
            if (newFs.get() > Fs.get()):
                filterdA = upSampling(filterdA, newFs.get() / Fs.get())
            else:
                filterdA = downSampling(filterdA, Fs.get() / newFs.get())
        before = np.array(filterdA)
        after = before - np.mean(before)
        min_value = min(after)
        max_value = max(after)
        normalized_data = [
            (2 * (x - min_value) / (max_value - min_value)) - 1 for x in after]

        sqr_signalA_sum1 = 0
        sqr_signalA_sum2 = 0

        r = 0

        for i in range(len(normalized_data)):

            sqr_signalA_sum1 += normalized_data[i]**2
            sqr_signalA_sum2 += normalized_data[i]**2

        for j in range(len(normalized_data)):
            nonlocal correlationA
            for n in range(len(normalized_data)):
                r += (1/len(normalized_data)) * \
                    (normalized_data[n]*normalized_data[(n+j) %
                     len(normalized_data)])

            correlationA.append(r)
            r = 0
        for i in range(int(len(correlationA)/8)):
            newCorA.append(correlationA[i])
        NDCT = len(correlationA)

        for x in range(NDCT):
            k = 0
            for y in range(NDCT):
                k += correlationA[y] * \
                    math.cos((math.pi / (4 * NDCT)) *
                             (2 * y - 1) * (2 * x - 1))
            k *= math.sqrt(2 / NDCT)
            DCT_A.append(k)
        print(DCT_A)
        # print(DCT_A)

    def calcClassB():
        avg_B = []
        sum_B = 0
        for i in range(len(listB[0])):
            # Calc the avrage
            for j in range(len(listB)):
                sum_B += (listB[j][i]/len(listB))

            # Append in avg list
            avg_B.append(sum_B)
        nonlocal filterdB
        calc("band-pass", Fs.get(), 50, minF.get(),
             maxF.get(), 500, filterB, avg_B, filterdB)
        if newFs.get() / maxF.get() <= 0.5:
            if (newFs.get() > Fs.get()):
                filterdB = upSampling(filterdB, newFs.get() / Fs.get())
            else:
                filterdB = downSampling(filterdB, Fs.get() / newFs.get())
        before = np.array(filterdB)
        after = before - np.mean(before)
        min_value = min(after)
        max_value = max(after)
        normalized_data = [
            (2 * (x - min_value) / (max_value - min_value)) - 1 for x in after]

        sqr_signalA_sum1 = 0
        sqr_signalA_sum2 = 0

        r = 0

        for i in range(len(normalized_data)):

            sqr_signalA_sum1 += normalized_data[i]**2
            sqr_signalA_sum2 += normalized_data[i]**2

        for j in range(len(normalized_data)):
            nonlocal correlationB
            for n in range(len(normalized_data)):
                r += (1/len(normalized_data)) * \
                    (normalized_data[n]*normalized_data[(n+j) %
                     len(normalized_data)])

            correlationB.append(r)
            r = 0
        for i in range(int(len(correlationB)/8)):
            newCorB.append(correlationB[i])
        NDCT = len(correlationB)

        for x in range(NDCT):
            k = 0
            for y in range(NDCT):
                k += correlationB[y] * \
                    math.cos((math.pi / (4 * NDCT)) *
                             (2 * y - 1) * (2 * x - 1))
            k *= math.sqrt(2 / NDCT)
            DCT_B.append(k)
        print(DCT_B)
        # print(DCT_B)

    calcBtnA = tk.Button(frame10, text="calc", command=lambda: calcClass())
    calcBtnA.pack(pady=5)
    calcBtnB = tk.Button(frame10, text="calc A", command=lambda: calcClassA())
    calcBtnB.pack(pady=5)
    calcBtn = tk.Button(frame10, text="calc B", command=lambda: calcClassB())
    calcBtn.pack(pady=5)

    plotFilter = tk.Button(frame10, text="plot original",
                           command=lambda: display_original(test))
    plotFilter.pack(pady=5)

    plotCor = tk.Button(frame10, text="plot cor",
                        command=lambda: display_original(correlation))
    plotCor.pack(pady=5)

    plotCor2 = tk.Button(frame10, text="plot cor 2",
                         command=lambda: display_original(newCor))
    plotCor2.pack(pady=5)
    plotDct = tk.Button(frame10, text="plot DCT",
                        command=lambda: display_original(DCT))
    plotDct.pack(pady=5)

    frame10.pack()


# main GUI
root = tk.Tk()
root.geometry("200x600")
root.title("DSP")
# taskOne
taskOneBtn = tk.Button(root, text="Task# 1",
                       command=taskOneFrame)
taskOneBtn.pack(pady=10)
# taskTwo
taskTwoBtn = tk.Button(root, text="Task# 2",
                       command=taskTwoFrame)
taskTwoBtn.pack(pady=10)
# task three
task3Btn = tk.Button(root, text="Task# 3", command=task3_frame_window)
task3Btn.pack(pady=10)
# task four
taskFourBtn = tk.Button(root, text="Task# 4", command=task4_frame_window)
taskFourBtn.pack(pady=10)
# task five
taskFiveBtn = tk.Button(root, text="Task# 5", command=task5_frame_window)
taskFiveBtn.pack(pady=10)
# task seven
taskSevenBtn = tk.Button(root, text="Task# 7", command=task5_frame_window)
taskSevenBtn.pack(pady=10)
# task eight
taskEightBtn = tk.Button(root, text="Task# 8", command=task8_frame_window)
taskEightBtn.pack(pady=10)
# task nine
taskNineBtn = tk.Button(root, text="Task# 9", command=task9_frame_window)
taskNineBtn.pack(pady=10)
# task ten
taskTenBtn = tk.Button(root, text="Task# 9-2", command=task10_frame_window)
taskTenBtn.pack(pady=10)
root.mainloop()


# Task# 2
# taskTwoLabel = tk.Label(root, text="Task# 2", fg="blue")
# taskTwoLabel.pack()
# multiplyButton = tk.Button(
#     root, text="multiply signals", command=multiply_frame_window)
# multiplyButton.pack(pady=10)
# additionButton = tk.Button(
#     root, text="add signals", command=addition_frame_window)
# additionButton.pack(pady=10)
# subButton = tk.Button(
#     root, text="subtract signals", command=sub_frame_window)
# subButton.pack(pady=10)
# sqButton = tk.Button(
#     root, text="square signal", command=sq_frame_window)
# sqButton.pack(pady=10)
# shiftButton = tk.Button(
#     root, text="Shifting signal", command=shifting_frame_window)
# shiftButton.pack(pady=10)
# normalizationButton = tk.Button(
#     root, text="Normalization signal", command=normalization_frame_window)
# normalizationButton.pack(pady=10)
# accumulationButton = tk.Button(
#     root, text="Accumulation signal", command=accumulation_frame_window)
# accumulationButton.pack(pady=10)
# # Task# 3
# taskThreeLabel = tk.Label(root, text="Task# 3", fg="blue")
# taskThreeLabel.pack()
# task3Btn = tk.Button(root, text="task3", command=task3_frame_window)
# task3Btn.pack(pady=10)
