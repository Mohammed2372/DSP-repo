import tkinter as tk
from tkinter import ttk
import numpy as np
import math
import matplotlib.pyplot as plt
from tkinter import filedialog
import copy


class DSPApplication:
    def __init__(self, root):
        self.root = root
        self.root.geometry("200x300")
        self.root.title("DSP")

        # Variables
        self.minF = tk.IntVar()
        self.maxF = tk.IntVar()
        self.Fs = tk.IntVar()
        self.newFs = tk.IntVar()

        if self.newFs.get() < 2*self.maxF:
            print("error, this process can't be done because newFs is lower than half of maxFs")
            return

        # GUI Elements
        self.frame10 = tk.Frame(self.root)
        self.setup_gui()

    def setup_gui(self):
        self.minFLabel = tk.Label(self.frame10, text="minF")
        self.maxFLabel = tk.Label(self.frame10, text="maxF")
        self.fsLabel = tk.Label(self.frame10, text="FS")
        self.newfsFLabel = tk.Label(self.frame10, text="newFS")

        self.minFEntry = tk.Entry(self.frame10, textvariable=self.minF)
        self.minFLabel.pack()
        self.minFEntry.pack()

        self.maxFEntry = tk.Entry(self.frame10, textvariable=self.maxF)
        self.maxFLabel.pack()
        self.maxFEntry.pack()

        self.fsEntry = tk.Entry(self.frame10, textvariable=self.Fs)
        self.fsLabel.pack()
        self.fsEntry.pack()

        self.newfsEntry = tk.Entry(self.frame10, textvariable=self.newFs)
        self.newfsFLabel.pack()
        self.newfsEntry.pack()

        # Other elements (filterd, filterdA, etc.) are removed for simplicity

        self.uploadButton1 = tk.Button(self.frame10, text="upload signal", command=self.read_data_new)
        self.uploadButton1.pack()
        global listA
        listA = []
        global listB
        listB = []
        global filterd, filterA,filterdA,filterB,filterdB,correlation,correlationA,correlationB,DCT,DCT_A,DCT_B,newCor,newCorA,newCorB,test
        filterA = []
        filterdA = []
        filterdB = []
        filterB = []
        filterd = []
        correlation = []
        correlationA = []
        correlationB = []
        test = []
        DCT = []
        DCT_A = []
        DCT_B = []
        newCor = []
        newCorA = []
        newCorB = []
        self.uploadA = tk.Button(self.frame10, text="upload A", command=lambda: self.read_data2(listA, "A"))
        self.uploadA.pack()

        self.uploadB = tk.Button(self.frame10, text="upload B", command=lambda: self.read_data2(listB, "B"))
        self.uploadB.pack()

        self.calcBtnA = tk.Button(self.frame10, text="calc", command=self.calcClass)
        self.calcBtnA.pack()

        self.frame10.pack()

    def read_data_new(self):
        global div_x
        div_x = []
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                for line in file:
                    number = float(line.strip())
                    div_x.append(number)

    def read_data2(self, classT, type):

        signals = []
        if type == "A":
            for i in range(6):
                with open("C:\\Users\\Mohammed237\\PycharmProjects\\DSP_Task\\DPS\\task9\\A\\ASeg" + str(i + 1) + ".txt",'r') as file:
                    for line in file:
                        line = file.readline().strip()
                        if line:
                            parts = line.split()

                            signals.append(float(parts[0]))
                    classT.append(signals)
        else:
            for i in range(6):
                with open("C:\\Users\\Mohammed237\\PycharmProjects\\DSP_Task\\DPS\\task9\\B\\BSeg" + str(i + 1) + ".txt",'r') as file:
                    for line in file:
                        line = file.readline().strip()
                        if line:
                            parts = line.split()

                            signals.append(float(parts[0]))
                    classT.append(signals)

    def window_calc(self, Wtype, n, N):
        match Wtype:
            case "Rectangular":
                return 1
            case "Hanning":
                return 0.5 + (0.5*math.cos((2*math.pi*n)/N))
            case "Hamming":
                return 0.54 + (0.46*math.cos((2*math.pi*n)/N))
            case "Blackman":
                return 0.42 + (0.5*math.cos((2*math.pi*n)/(N-1))) + (0.08*math.cos((4*math.pi*n)/(N-1)))

    def calc(self, Ftype, fs, stop, f1, f2, trans, result, ecg, filterd):
        Wtype = ""
        n = 0
        N = 0
        normalized_trans = trans / fs
        result = []

        if (stop <= 21):
            Wtype = "Rectangular"
            N = round(0.9 / normalized_trans, 0)
        elif (stop <= 44):
            Wtype = "Hanning"
            N = round(3.1 / normalized_trans, 0)
        elif (stop <= 53):
            Wtype = "Hamming"
            N = round(3.3 / normalized_trans, 0)
        elif (stop <= 74 or stop > 74):
            Wtype = "Blackman"
            N = round(5.5 / normalized_trans, 0)

        if (N % 2 == 0):
            N = N + 1
        n = -((N - 1) / 2)

        match Ftype:
            case "low-pass":
                f1 = (f1 + (trans / 2)) / fs
            case "high-pass":
                f1 = (f1 - (trans / 2)) / fs
            case "band-pass":
                f1 = (f1 - (trans / 2)) / fs
                f2 = (f2 + (trans / 2)) / fs
            case "band-stop":
                f1 = (f1 + (trans / 2)) / fs
                f2 = (f2 - (trans / 2)) / fs
        for i in range(int(N)):
            res = 0
            match Ftype:
                case "low-pass":
                    if (n == 0):
                        res = (2 * f1) * self.window_calc(Wtype, n, N)
                    else:
                        res = (2 * f1 * ((math.sin(n * 2 * math.pi * f1)) /
                                         (n * 2 * math.pi * f1))) * self.window_calc(Wtype, n, N)
                case "high-pass":
                    if (n == 0):
                        res = (1 - 2 * f1) * self.window_calc(Wtype, n, N)
                    else:
                        res = (-2 * f1 * (math.sin(n * 2 * math.pi * f1) /
                                          (n * 2 * math.pi * f1))) * self.window_calc(Wtype, n, N)
                case "band-pass":
                    if n == 0:
                        res = (2 * (f2 - f1)) * self.window_calc(Wtype, n, N)
                    else:
                        res = ((2 * f2 * (math.sin(n * 2 * math.pi * f2) / (n * 2 * math.pi * f2))) - (2 * f1 *(math.sin(n * 2 * math.pi * f1) / (
                                                                                    n * 2 * math.pi * f1)))) * self.window_calc(Wtype, n, N)
                case "band-stop":
                    if n == 0:
                        res = (1 - 2 * (f2 - f1)) * self.window_calc(Wtype, n, N)
                    else:
                        res = -((2 * f2 * (math.sin(n * 2 * math.pi * f2) / (n * 2 * math.pi * f2))) - (2 * f1 *
                                (math.sin(n * 2 * math.pi * f1) / (n * 2 * math.pi * f1)))) * self.window_calc(Wtype, n, N)
            result.append(res)
            n = n + 1
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

    def upSampling(self, data, factor):
        zeros_num = factor - 1
        result = []
        for i in range(len(data)):
            result.append(data[i])
            if i != len(data) - 1:
                for j in range(zeros_num):
                    result.append(0)
        return result

    def downSampling(self, data, factor):
        result = []
        for i in range(len(data)):
            if (i % factor == 0):
                result.append(data[i])
        return result

    def calc_correlation(self, signalA, signalB, normalized):
        sqr_signalA_sum = 0
        sqr_signalB_sum = 0

        correlation = []
        indecies = []
        r = 0

        for i in range(len(signalA)):
            sqr_signalA_sum += signalA[i] ** 2
            sqr_signalB_sum += signalB[i] ** 2
        for j in range(len(signalA)):
            for n in range(len(signalA)):
                r += (1 / len(signalA)) * (signalA[n] * signalB[(n + j) % len(signalA)])

            if normalized:
                result = r / ((1 / len(signalA)) *
                              (math.sqrt(sqr_signalA_sum * sqr_signalB_sum)))
                correlation.append(round(result, 8))
            else:
                correlation.append(r)
            indecies.append(j)
            r = 0
        if normalized:
            comp.Compare_Signals("CorrOutput.txt", indecies, correlation)

        return correlation

    def calcClass(self):
        avg_A = []
        sum_A = 0
        for i in range(len(listA[0])):
            # Calc the avrage
            for j in range(len(listA)):
                sum_A += (listA[j][i] / len(listA))

            # Append in avg list
            avg_A.append(sum_A)
        global filterdA
        self.calc("band-pass", self.Fs.get(), 50, self.minF.get(),
                  self.maxF.get(), 500, filterA, avg_A, filterdA)
        if self.newFs.get() / self.maxF.get() <= 0.5:
            if (self.newFs.get() > self.Fs.get()):
                filterdA = filter.upSampling(filterdA,self.newFs.get() / self.Fs.get())
            else:
                filterdA = downSampling(filterdA, self.Fs.get() / self.newFs.get())
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
            sqr_signalA_sum1 += normalized_data[i] ** 2
            sqr_signalA_sum2 += normalized_data[i] ** 2

        for j in range(len(normalized_data)):
            global correlationA
            for n in range(len(normalized_data)):
                r += (1 / len(normalized_data)) * \
                     (normalized_data[n] * normalized_data[(n + j) %
                                                           len(normalized_data)])

            correlationA.append(r)
            r = 0
        for i in range(int(len(correlationA) / 8)):
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
                sum_B += (listB[j][i] / len(listB))

            # Append in avg list
            avg_B.append(sum_B)

        global filterdB
        self.calc("band-pass", self.Fs.get(), 50, self.minF.get(),
                  self.maxF.get(), 500, filterB, avg_B, filterdB)
        if self.newFs.get() / self.maxF.get() <= 0.5:
            if (self.newFs.get() > self.Fs.get()):
                filterdB = upSampling(filterdB, self.newFs.get() / self.Fs.get())
            else:
                filterdB = downSampling(filterdB, self.Fs.get() / self.newFs.get())
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
            sqr_signalA_sum1 += normalized_data[i] ** 2
            sqr_signalA_sum2 += normalized_data[i] ** 2

        for j in range(len(normalized_data)):
            global correlationB
            for n in range(len(normalized_data)):
                r += (1 / len(normalized_data)) * \
                     (normalized_data[n] * normalized_data[(n + j) %
                                                           len(normalized_data)])

            correlationB.append(r)
            r = 0
        for i in range(int(len(correlationB) / 8)):
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

        global filterd
        self.calc("band-pass", self.Fs.get(), 50, self.minF.get(),
                  self.maxF.get(), 500, filter, test, filterd)
        if self.newFs.get() / self.maxF.get() <= 0.5:
            if self.newFs.get() > self.Fs.get():
                filterd = upSampling(filterd, self.newFs.get() / self.Fs.get())
            else:
                filterd = downSampling(filterd, self.Fs.get() / self.newFs.get())
        before = np.array(filterd)
        after = before - np.mean(before)
        min_value = 0
        max_value = 0

        for i in range(len(after)):
            if min_value > after[i]:
                 min_value = after[i]
            if after[i] > max_value:
                max_value = after[i]

        normalized_data = [
            (2 * (x - min_value) / (max_value - min_value)) - 1 for x in after]

        sqr_signalA_sum1 = 0
        sqr_signalA_sum2 = 0

        r = 0

        for i in range(len(normalized_data)):
            sqr_signalA_sum1 += normalized_data[i] ** 2
            sqr_signalA_sum2 += normalized_data[i] ** 2

        for j in range(len(normalized_data)):
            global correlation
            for n in range(len(normalized_data)):
                r += (1 / len(normalized_data)) * \
                     (normalized_data[n] * normalized_data[(n + j) %
                                                           len(normalized_data)])

            correlation.append(r)
            r = 0
        for i in range(int(len(correlation) / 8)):
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

        corA = self.calc_correlation(DCT, DCT_A, False)
        corB = self.calc_correlation(DCT, DCT_B, False)
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

    def calcClassA(self):
        avg_A = []
        sum_A = 0
        for i in range(len(listA[0])):
            # Calc the avrage
            for j in range(len(listA)):
                sum_A += (listA[j][i] / len(listA))

            # Append in avg list
            avg_A.append(sum_A)
        global filterdA
        calc("band-pass", self.Fs.get(), 50, self.minF.get(),
             self.maxF.get(), 500, filterA, avg_A, filterdA)
        if self.newFs.get() / self.maxF.get() <= 0.5:
            if (self.newFs.get() > self.Fs.get()):
                filterdA = upSampling(filterdA, self.newFs.get() / self.Fs.get())
            else:
                filterdA = downSampling(filterdA, self.Fs.get() / self.newFs.get())
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
            sqr_signalA_sum1 += normalized_data[i] ** 2
            sqr_signalA_sum2 += normalized_data[i] ** 2

        for j in range(len(normalized_data)):
            global correlationA
            for n in range(len(normalized_data)):
                r += (1 / len(normalized_data)) * \
                     (normalized_data[n] * normalized_data[(n + j) %
                                                           len(normalized_data)])

            correlationA.append(r)
            r = 0
        for i in range(int(len(correlationA) / 8)):
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

    def calcClassB(self):
        avg_B = []
        sum_B = 0
        for i in range(len(listB[0])):
            # Calc the avrage
            for j in range(len(listB)):
                sum_B += (listB[j][i] / len(listB))

            # Append in avg list
            avg_B.append(sum_B)
        global filterdB
        self.calc("band-pass", self.Fs.get(), 50, self.minF.get(),
                  self.maxF.get(), 500, filterB, avg_B, filterdB)
        if self.newFs.get() / self.maxF.get() <= 0.5:
            if (self.newFs.get() > self.Fs.get()):
                filterdB = upSampling(filterdB, self.newFs.get() / self.Fs.get())
            else:
                filterdB = downSampling(filterdB, self.Fs.get() / self.newFs.get())
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
            sqr_signalA_sum1 += normalized_data[i] ** 2
            sqr_signalA_sum2 += normalized_data[i] ** 2

        for j in range(len(normalized_data)):
            global correlationB
            for n in range(len(normalized_data)):
                r += (1 / len(normalized_data)) * \
                     (normalized_data[n] * normalized_data[(n + j) %
                                                           len(normalized_data)])

            correlationB.append(r)
            r = 0
        for i in range(int(len(correlationB) / 8)):
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


if __name__ == "__main__":
    root = tk.Tk()
    app = DSPApplication(root)
    root.mainloop()
