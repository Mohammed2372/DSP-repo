import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import math


class DSPApplication:
    def __init__(self, root):
        self.root = root
        self.root.geometry("200x600")
        self.root.title("DSP")

        # Variables
        self.minF = tk.IntVar()
        self.maxF = tk.IntVar()
        self.Fs = tk.IntVar()
        self.newFs = tk.IntVar()

        # GUI Elements
        self.frame10 = tk.Frame(self.root)
        self.setup_gui()

    def setup_gui(self):
        self.minFLabel = tk.Label(self.frame10, text="minF")
        self.maxFLabel = tk.Label(self.frame10, text="maxF")
        self.fsLabel = tk.Label(self.frame10, text="FS")
        self.newfsFLabel = tk.Label(self.frame10, text="newFS")

        self.minFEntry = tk.Entry(self.frame10, textvariable=self.minF)
        self.minFLabel.pack(pady=5)
        self.minFEntry.pack(pady=5)

        self.maxFEntry = tk.Entry(self.frame10, textvariable=self.maxF)
        self.maxFLabel.pack(pady=5)
        self.maxFEntry.pack(pady=5)

        self.fsEntry = tk.Entry(self.frame10, textvariable=self.Fs)
        self.fsLabel.pack(pady=5)
        self.fsEntry.pack(pady=5)

        self.newfsEntry = tk.Entry(self.frame10, textvariable=self.newFs)
        self.newfsFLabel.pack(pady=5)
        self.newfsEntry.pack(pady=5)

        # Other elements (filterd, filterdA, etc.) are removed for simplicity

        self.uploadButton1 = tk.Button(self.frame10, text="upload signal", command=self.read_data_new)
        self.uploadButton1.pack(pady=5)

        self.uploadA = tk.Button(self.frame10, text="upload A", command=lambda: self.read_data2(self.listA, "A"))
        self.uploadA.pack(pady=5)

        self.uploadB = tk.Button(self.frame10, text="upload B", command=lambda: self.read_data2(self.listB, "B"))
        self.uploadB.pack(pady=5)

        self.calcBtnA = tk.Button(self.frame10, text="calc", command=self.calc_class)
        self.calcBtnA.pack(pady=5)

        self.plotFilter = tk.Button(self.frame10, text="plot original",
                                    command=lambda: self.display_original(self.test))
        self.plotFilter.pack(pady=5)

        self.plotCor = tk.Button(self.frame10, text="plot cor", command=lambda: self.display_original(self.correlation))
        self.plotCor.pack(pady=5)

        self.plotCor2 = tk.Button(self.frame10, text="plot cor 2", command=lambda: self.display_original(self.newCor))
        self.plotCor2.pack(pady=5)

        self.plotDct = tk.Button(self.frame10, text="plot DCT", command=lambda: self.display_original(self.DCT))
        self.plotDct.pack(pady=5)

        self.frame10.pack()

    def read_data_new(self):
        # Implement this method according to your needs
        pass

    def read_data2(self, data_list, label):
        # Implement this method according to your needs
        pass

    def display_original(self, y):
        time = np.linspace(0, 100, len(y))
        plt.plot(time, y, label="original ecg")
        plt.legend()
        plt.show()

    def calcClass(self):
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


if __name__ == "__main__":
    root = tk.Tk()
    app = DSPApplication(root)
    root.mainloop()
