import tkinter as tk
from tkinter import ttk
import numpy as np
import math
import matplotlib.pyplot as plt
from tkinter import filedialog


class FilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Filter Application")

        self.filter_type_var = tk.StringVar()
        self.filter_type_var.set("low_pass")  # Default filter type

        # Option menu for choosing filter type
        filter_type_label = ttk.Label(root, text="Choose Filter Type:")
        filter_type_menu = ttk.OptionMenu(root, self.filter_type_var, "low_pass", "low_pass", "high_pass", "band_pass",
                                          "stop_pass")
        filter_type_label.pack()
        filter_type_menu.pack()

        # Entry widgets for user input
        self.passband_edge_freq_1_entry = self.create_entry(root, "Passband Edge Frequency 1:")
        self.passband_edge_freq_2_entry = self.create_entry(root, "Passband Edge Frequency 2:")
        self.transition_width_entry = self.create_entry(root, "Transition Width:")
        self.stop_band_att_entry = self.create_entry(root, "Stopband Attenuation:")
        self.fs_entry = self.create_entry(root, "Sampling Frequency:")

        # Button to choose file
        file_button = ttk.Button(root, text="Choose File", command=self.choose_file)
        file_button.pack()

        # Button to apply filter
        apply_button = ttk.Button(root, text="Apply Filter", command=self.apply_filter)
        apply_button.pack()

    def create_entry(self, root, label_text):
        label = ttk.Label(root, text=label_text)
        entry = ttk.Entry(root)
        label.pack()
        entry.pack()
        return entry

    def choose_file(self):
        file_path = filedialog.askopenfilename()
        print("File chosen:", file_path)

        # Read points and metadata from the file
        global points
        points = self.read_points_and_metadata_from_file(file_path)
        print("Points:", points)

    def apply_filter(self):
        passband_edge_freq_1 = float(self.passband_edge_freq_1_entry.get())
        passband_edge_freq_2 = float(self.passband_edge_freq_2_entry.get())
        transition_width = float(self.transition_width_entry.get())
        stop_band_att = float(self.stop_band_att_entry.get())
        fs = float(self.fs_entry.get())

        # Assume you have a signal array, replace this with your actual signal
        signal = []
        signal = points

        filter_type = self.filter_type_var.get()

        self.choosing_filter(signal, passband_edge_freq_1, passband_edge_freq_2, transition_width, stop_band_att, fs,
                             filter_type)

    def choosing_filter(self, signal, passband_edge_freq_1, passband_edge_freq_2, transition_width, stop_band_att, fs, filter_type):
        normlized_fs = transition_width / fs
        half_list = []
        full_list = []

        if filter_type == "low_pass":
            filter_low_pass(stop_band_att, normlized_fs, passband_edge_freq_1, half_list)
        if filter_type == "high_pass":
            filter_high_pass(stop_band_att, normlized_fs, passband_edge_freq_1, half_list, full_list)
        if filter_type == "band_pass":
            filter_band_pass(stop_band_att, normlized_fs, passband_edge_freq_1, passband_edge_freq_2, half_list,
                             full_list)
        if filter_type == "stop_pass":
            filter_stop_pass(stop_band_att, normlized_fs, passband_edge_freq_1, passband_edge_freq_2, half_list,
                             full_list)

    def filter_low_pass(self, stop_band_att, normlized_fs, passband_edge_freq_1, half_list):
        if stop_band_att <= 21:
            n = math.ceil(0.9 / normlized_fs)
            if n % 2 == 0:
                n += 1
            n_for_loop = int((np.abs(n) - 1) / 2)

            new_fc = (passband_edge_freq_1 + (transition_width / 2)) / fs
            for i in range(n_for_loop):
                if i == 0:
                    hd = 2 * new_fc
                else:
                    hd = (2 * new_fc) * (math.sin(2 * math.pi * new_fc * i) / (2 * math.pi * new_fc * i))

                w = 1
                hdTw = hd * w
                half_list.append(hdTw)

        elif stop_band_att <= 44:
            n = math.ceil(3.1 / normlized_fs)
            if n % 2 == 0:
                n += 1
            n_for_loop = int((np.abs(n) - 1) / 2)

            new_fc = (passband_edge_freq_1 + (transition_width / 2)) / fs

            for i in range(n_for_loop):
                if i == 0:
                    hd = 2 * new_fc
                else:
                    hd = (2 * new_fc) * (math.sin(2 * math.pi * new_fc * i) / (2 * math.pi * new_fc * i))

                w = 0.54 + 0.5 * math.cos(2 * math.pi * i / n)
                hdTw = hd * w
                half_list.append(hdTw)


        elif stop_band_att <= 53:
            n = math.ceil(3.3 / normlized_fs)
            if n % 2 == 0:
                n += 1
            n_for_loop = int((np.abs(n) - 1) / 2)
            new_fc = (passband_edge_freq_1 + (transition_width / 2)) / fs

            for i in range(n_for_loop):
                if i == 0:
                    hd = 2 * new_fc
                else:
                    hd = (2 * new_fc) * (math.sin(2 * math.pi * new_fc * i) / (2 * math.pi * new_fc * i))

                print(i)
                w = 0.54 + 0.46 * math.cos(2 * math.pi * i / n)
                print(hd)

                hdTw = hd * w
                half_list.append(hdTw)


        elif stop_band_att <= 74:
            n = math.ceil(5.5 / normlized_fs)
            if n % 2 == 0:
                n += 1
            n_for_loop = int((np.abs(n) - 1) / 2)

            new_fc = (passband_edge_freq_1 + (transition_width / 2)) / fs

            for i in range(n_for_loop):
                if i == 0:
                    hd = 2 * new_fc
                else:
                    hd = (2 * new_fc) * (math.sin(2 * math.pi * new_fc * i) / (2 * math.pi * new_fc * i))

                w = 0.42 + 0.5 * math.cos((2 * math.pi * i) / (n - 1)) + 0.08 * math.cos((4 * math.pi * i) / (n - 1))
                hdTw = hd * w
                half_list.append(hdTw)

        for j in range(n):
            if j >= n_for_loop:
                full_list.append(((j - n_for_loop), half_list[j - n_for_loop - 1]))
            else:
                full_list.append(((j - n_for_loop), half_list[n_for_loop - j - 1]))

        signal = full_list

    def filter_high_pass(self, stop_band_att, normlized_fs, passband_edge_freq_1, half_list, full_list):
        if stop_band_att <= 21:
            n = math.ceil(0.9 / normlized_fs)
            if n % 2 == 0:
                n += 1
            n_for_loop = int((np.abs(n) - 1) / 2)

            new_fc = (passband_edge_freq_1 - (transition_width / 2)) / fs

            for i in range(n_for_loop):
                if i == 0:
                    hd = 1 - (2 * new_fc)
                else:
                    hd = -1 * ((2 * new_fc) * (math.sin(2 * math.pi * new_fc * i) / (2 * math.pi * new_fc * i)))

                w = 1
                hdTw = hd * w
                half_list.append(hdTw)

        elif stop_band_att <= 44:
            n = math.ceil(3.1 / normlized_fs)
            if n % 2 == 0:
                n += 1
            n_for_loop = int((np.abs(n) - 1) / 2)

            new_fc = (passband_edge_freq_1 - (transition_width / 2)) / fs

            for i in range(n_for_loop):
                if i == 0:
                    hd = 1 - (2 * new_fc)
                else:
                    hd = -1 * ((2 * new_fc) * (math.sin(2 * math.pi * new_fc * i) / (2 * math.pi * new_fc * i)))

                w = 0.54 + 0.5 * math.cos(2 * math.pi * i / n)
                hdTw = hd * w
                half_list.append(hdTw)

        elif stop_band_att <= 53:
            n = math.ceil(3.3 / normlized_fs)
            if n % 2 == 0:
                n += 1
            n_for_loop = int((np.abs(n) - 1) / 2)

            new_fc = (passband_edge_freq_1 - (transition_width / 2)) / fs

            for i in range(n_for_loop):
                if i == 0:
                    hd = 1 - (2 * new_fc)
                else:
                    hd = -1 * ((2 * new_fc) * (math.sin(2 * math.pi * new_fc * i) / (2 * math.pi * new_fc * i)))

                w = 0.54 + 0.46 * math.cos(2 * math.pi * i / n)
                hdTw = hd * w
                half_list.append(hdTw)

        elif stop_band_att <= 74:
            n = math.ceil(5.5 / normlized_fs)
            if n % 2 == 0:
                n += 1
            n_for_loop = int((np.abs(n) - 1) / 2)

            new_fc = (passband_edge_freq_1 - (transition_width / 2)) / fs

            for i in range(n_for_loop):
                if i == 0:
                    hd = 1 - (2 * new_fc)
                else:
                    hd = -1 * ((2 * new_fc) * (math.sin(2 * math.pi * new_fc * i) / (2 * math.pi * new_fc * i)))

                w = 0.42 + 0.5 * math.cos((2 * math.pi * i) / (n - 1)) + 0.08 * math.cos((4 * math.pi * i) / (n - 1))
                hdTw = hd * w
                half_list.append(hdTw)

        for j in range(n):
            print(j)

            if j >= n_for_loop:
                full_list.append(((j - n_for_loop), half_list[j - n_for_loop - 1]))
            else:
                full_list.append(((j - n_for_loop), half_list[n_for_loop - j - 1]))

    def filter_band_pass(self, stop_band_att, normlized_fs, passband_edge_freq_1, passband_edge_freq_2, half_list, full_list):
        if stop_band_att <= 21:
            n = math.ceil(0.9 / normlized_fs)
            if n % 2 == 0:
                n += 1
            new_fc1 = passband_edge_freq_1 - (transition_width / 2)
            new_fc2 = passband_edge_freq_2 + (transition_width / 2)
            n_for_loop = int((np.abs(n) - 1) / 2)

            for i in range(n_for_loop):
                if i == 0:
                    hd = 2 * (new_fc2 - new_fc1)
                else:
                    hd = (2 * new_fc2) * (math.sin(2 * math.pi * new_fc2 * i) / (2 * math.pi * new_fc2 * i)) - (
                                2 * new_fc1) * (math.sin(2 * math.pi * new_fc1 * i) / (2 * math.pi * new_fc1 * i))

                w = 1
                hdTw = hd * w
                half_list.append(hdTw)

        elif stop_band_att <= 44:
            n = math.ceil(3.1 / normlized_fs)
            if n % 2 == 0:
                n += 1
            new_fc1 = passband_edge_freq_1 - (transition_width / 2)
            new_fc2 = passband_edge_freq_2 + (transition_width / 2)
            n_for_loop = int((np.abs(n) - 1) / 2)

            for i in range(n_for_loop):
                if i == 0:
                    hd = 2 * (new_fc2 - new_fc1)
                else:
                    hd = (2 * new_fc2) * (math.sin(2 * math.pi * new_fc2 * i) / (2 * math.pi * new_fc2 * i)) - (
                                2 * new_fc1) * (math.sin(2 * math.pi * new_fc1 * i) / (2 * math.pi * new_fc1 * i))

                w = 0.54 + 0.5 * math.cos(2 * math.pi * i / n)
                hdTw = hd * w
                half_list.append(hdTw)

        elif stop_band_att <= 53:
            n = math.ceil(3.3 / normlized_fs)
            if n % 2 == 0:
                n += 1
            new_fc1 = passband_edge_freq_1 - (transition_width / 2)
            new_fc2 = passband_edge_freq_2 + (transition_width / 2)
            n_for_loop = int((np.abs(n) - 1) / 2)

            for i in range(n_for_loop):
                if i == 0:
                    hd = 2 * (new_fc2 - new_fc1)
                else:
                    hd = (2 * new_fc2) * (math.sin(2 * math.pi * new_fc2 * i) / (2 * math.pi * new_fc2 * i)) - (
                                2 * new_fc1) * (math.sin(2 * math.pi * new_fc1 * i) / (2 * math.pi * new_fc1 * i))

                w = 0.54 + 0.46 * math.cos(2 * math.pi * i / n)
                hdTw = hd * w
                half_list.append(hdTw)

        elif stop_band_att <= 74:
            n = math.ceil(5.5 / normlized_fs)
            if n % 2 == 0:
                n += 1
            new_fc1 = passband_edge_freq_1 - (transition_width / 2)
            new_fc2 = passband_edge_freq_2 + (transition_width / 2)
            n_for_loop = int((np.abs(n) - 1) / 2)

            for i in range(n_for_loop):
                if i == 0:
                    hd = 2 * (new_fc2 - new_fc1)
                else:
                    hd = (2 * new_fc2) * (math.sin(2 * math.pi * new_fc2 * i) / (2 * math.pi * new_fc2 * i)) - (
                                2 * new_fc1) * (math.sin(2 * math.pi * new_fc1 * i) / (2 * math.pi * new_fc1 * i))

                w = 0.42 + 0.5 * math.cos((2 * math.pi * i) / (n - 1)) + 0.08 * math.cos((4 * math.pi * i) / (n - 1))
                hdTw = hd * w
                half_list.append(hdTw)

        for j in range(n):
            if j >= n_for_loop:
                full_list.append(((j - n_for_loop), half_list[j - n_for_loop - 1]))
            else:
                full_list.append(((j - n_for_loop), half_list[n_for_loop - j - 1]))

    def filter_stop_pass(self, stop_band_att, normlized_fs, passband_edge_freq_1, passband_edge_freq_2, half_list,
                         full_list):
        if stop_band_att <= 21:
            n = math.ceil(0.9 / normlized_fs)
            if n % 2 == 0:
                n += 1
            new_fc1 = passband_edge_freq_1 + (transition_width / 2)
            new_fc2 = passband_edge_freq_2 - (transition_width / 2)
            n_for_loop = int((np.abs(n) - 1) / 2)

            for i in range(n_for_loop):
                if i == 0:
                    hd = -2 * (new_fc2 - new_fc1)
                else:
                    hd = -1 * (2 * new_fc2) * (math.sin(2 * math.pi * new_fc2 * i) / (2 * math.pi * new_fc2 * i)) + (
                                2 * new_fc1) * (math.sin(2 * math.pi * new_fc1 * i) / (2 * math.pi * new_fc1 * i))

                w = 1
                hdTw = hd * w
                half_list.append(hdTw)

        elif stop_band_att <= 44:
            n = math.ceil(3.1 / normlized_fs)
            if n % 2 == 0:
                n += 1
            new_fc1 = passband_edge_freq_1 + (transition_width / 2)
            new_fc2 = passband_edge_freq_2 - (transition_width / 2)
            n_for_loop = int((np.abs(n) - 1) / 2)

            for i in range(n_for_loop):
                if i == 0:
                    hd = -2 * (new_fc2 - new_fc1)
                else:
                    hd = -1 * (2 * new_fc2) * (math.sin(2 * math.pi * new_fc2 * i) / (2 * math.pi * new_fc2 * i)) + (
                                2 * new_fc1) * (math.sin(2 * math.pi * new_fc1 * i) / (2 * math.pi * new_fc1 * i))

                w = 0.54 + 0.5 * math.cos(2 * math.pi * i / n)
                hdTw = hd * w
                half_list.append(hdTw)


        elif stop_band_att <= 53:
            n = math.ceil(3.3 / normlized_fs)
            if n % 2 == 0:
                n += 1
            new_fc1 = passband_edge_freq_1 + (transition_width / 2)
            new_fc2 = passband_edge_freq_2 - (transition_width / 2)
            n_for_loop = int((np.abs(n) - 1) / 2)

            for i in range(n_for_loop):
                if i == 0:
                    hd = -2 * (new_fc2 - new_fc1)
                else:
                    hd = -1 * (2 * new_fc2) * (math.sin(2 * math.pi * new_fc2 * i) / (2 * math.pi * new_fc2 * i)) + (
                                2 * new_fc1) * (math.sin(2 * math.pi * new_fc1 * i) / (2 * math.pi * new_fc1 * i))

                w = 0.54 + 0.46 * math.cos(2 * math.pi * i / n)
                hdTw = hd * w
                half_list.append(hdTw)

        elif stop_band_att <= 74:
            n = math.ceil(5.5 / normlized_fs)
            if n % 2 == 0:
                n += 1
            new_fc1 = passband_edge_freq_1 + (transition_width / 2)
            new_fc2 = passband_edge_freq_2 - (transition_width / 2)
            n_for_loop = int((np.abs(n) - 1) / 2)

            for i in range(n_for_loop):
                if i == 0:
                    hd = -2 * (new_fc2 - new_fc1)
                else:
                    hd = -1 * (2 * new_fc2) * (math.sin(2 * math.pi * new_fc2 * i) / (2 * math.pi * new_fc2 * i)) + (
                                2 * new_fc1) * (math.sin(2 * math.pi * new_fc1 * i) / (2 * math.pi * new_fc1 * i))

                w = 0.42 + 0.5 * math.cos((2 * math.pi * i) / (n - 1)) + 0.08 * math.cos((4 * math.pi * i) / (n - 1))
                hdTw = hd * w
                half_list.append(hdTw)

        for j in range(n):
            if j >= n_for_loop:
                full_list.append(((j - n_for_loop), half_list[j - n_for_loop - 1]))
            else:
                full_list.append(((j - n_for_loop), half_list[n_for_loop - j - 1]))


    def read_points_and_metadata_from_file(self, file_path):
        points = []
        X_label = None

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

        return points


if __name__ == "__main__":
    root = tk.Tk()
    app = FilterApp(root)
    root.mainloop()
