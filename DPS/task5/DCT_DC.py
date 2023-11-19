import tkinter as tk
from tkinter import ttk
import math
from DPS.task5 import tst


class Task5:
    def __init__(self):
        pass

    def DCT_DEF(self, user_var):
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

    def DC_DEF(self):
        before = [10.4628, 7.324, 7.8834, 11.3679, 12.962, 10.4628, 7.324,
                  7.8834, 11.3679, 12.962, 11.3679, 12.962, 10.4628, 7.324, 7.8834, 12.962]

        sum = 0

        for j in before:
            sum += j

        before_mean = sum / len(before)

        for j in range(len(before)):
            before[j] = round((before[j] - before_mean), 3)
        global after
        after = before

        with open("DC_output.txt", "w") as myFile:
            for i in range(len(after)):
                myFile.write(str(i) + '  ' + str(after[i]) + '\n')

        print(after)

    def saveToFile(self):
        tst.SignalSamplesAreEqual("DCT_output.txt", DCT)
        tst.SignalSamplesAreEqual("DC_component_output.txt", after)

    def all(self, user_var):
        self.DCT_DEF(user_var)
        self.DC_DEF()
        self.saveToFile()


class Task5GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task5 GUI")

        self.label = ttk.Label(self, text="Enter number of DCT:")
        self.label.pack(pady=10)

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.entry_var)
        self.entry.pack(pady=10)

        self.calculate_button = ttk.Button(self, text="Calculate", command=self.calculate_all)
        self.calculate_button.pack(pady=10)

    def calculate_all(self):
        user_var = self.entry_var.get()
        task5_instance = Task5()
        task5_instance.all(user_var)


if __name__ == "__main__":
    app = Task5GUI()
    app.mainloop()
