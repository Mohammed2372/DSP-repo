import tkinter as tk
from tkinter import ttk
import numpy as np
import math
import matplotlib.pyplot as plt
from tkinter import filedialog
import copy


class FilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Filter Application")

        self.filter_type_var = tk.StringVar()
        self.filter_type_var.set("low_pass")  # Default filter type

        # New checkbox to control "Use Filter" checkbox state
        self.use_low_pass_only_var = tk.IntVar()
        use_low_pass_only_checkbox = tk.Checkbutton(root, text="Use Low Pass Only",
                                                    variable=self.use_low_pass_only_var,
                                                    command=self.toggle_filter_options)
        use_low_pass_only_checkbox.pack()

        # Option menu for choosing filter type
        filter_type_label = ttk.Label(root, text="Choose Filter Type:")
        filter_type_label.pack()

        # Option menu for choosing filter type, initially with all options
        self.filter_type_options = ["low_pass", "high_pass", "band_pass", "stop_pass"]
        self.filter_type_menu = ttk.OptionMenu(root, self.filter_type_var, *self.filter_type_options)
        self.filter_type_menu.pack()

        # Entry widgets for user input
        self.passband_edge_freq_1_entry = self.create_entry(root, "Passband Edge Frequency 1:")
        self.passband_edge_freq_2_entry = self.create_entry(root, "Passband Edge Frequency 2:")
        self.transition_width_entry = self.create_entry(root, "Transition Width:")
        self.stop_band_att_entry = self.create_entry(root, "Stopband Attenuation:")
        self.fs_entry = self.create_entry(root, "Sampling Frequency:")

        # Checkbox to enable/disable file choosing
        self.use_filter_checkbox_var = tk.IntVar()
        use_filter_checkbox = tk.Checkbutton(root, text="Use Filter on Signal", variable=self.use_filter_checkbox_var,
                                             command=self.toggle_filter_button)
        use_filter_checkbox.pack()

        # Button to choose file, initially disabled
        self.choose_file_button = ttk.Button(root, text="Choose File", command=self.choose_file)
        self.choose_file_button.pack()
        self.choose_file_button["state"] = "disabled"  # Initially disabled

        # Button to apply filter
        apply_button = ttk.Button(root, text="Apply Filter", command=self.apply_filter)
        apply_button.pack()

        # Button to choose file for comparison
        choose_compare_file_button = ttk.Button(root, text="Choose File to Compare", command=self.choose_compare_file)
        choose_compare_file_button.pack()

        # Variable to store the file path for comparison
        self.compare_file_path = None

    def create_entry(self, root, label_text):
        label = ttk.Label(root, text=label_text)
        entry = ttk.Entry(root)
        label.pack()
        entry.pack()
        return entry

    def apply_filter(self):
        passband_edge_freq_1 = float(self.passband_edge_freq_1_entry.get())
        passband_edge_freq_2 = float(self.passband_edge_freq_2_entry.get())
        transition_width = float(self.transition_width_entry.get())
        stop_band_att = float(self.stop_band_att_entry.get())
        fs = float(self.fs_entry.get())

        # Assume you have a signal array, replace this with your actual signal
        signal = points

        filter_type = self.filter_type_var.get()

        filtered_signal = self.choosing_filter(passband_edge_freq_1, passband_edge_freq_2, transition_width,
                                               stop_band_att, fs, filter_type)

        # Save the filtered signal to a file
        filtered_file_path = "filtered_signal.txt"
        self.save_filtered_signal_to_file(filtered_signal, filtered_file_path)

        # split x and y
        x_values = []
        y_values = []
        for pair in filtered_signal:
            x_values.append(pair[0])
            y_values.append(pair[1])

        # Multiply signal with the filter only if the checkbox is checked
        if self.use_filter_checkbox_var.get():
            signal_tuple = [list(t) for t in signal]
            filter_tuple = [list(t) for t in filtered_signal]
            filter_conv = self.conv(signal_tuple, filter_tuple)

        # split conv result in x and y
        print(filter_conv)
        conv_x = []
        conv_y = []
        for i in filter_conv:
            conv_x.append(i[0])
            conv_y.append(i[1])

        # Compare the filtered file with the chosen file for comparison
        if self.use_filter_checkbox_var.get():
            self.compare_files((self.compare_file_path, conv_x, conv_y))
        elif self.compare_file_path:
            self.compare_files(self.compare_file_path, x_values, y_values)
        else:
            print("Please choose a file for comparison.")

        # Plot the filtered signal
        # self.plot_signal(signal, filtered_signal)
        print(filter_conv)

    def choosing_filter(self, passband_edge_freq_1, passband_edge_freq_2, transition_width, stop_band_att, fs,
                        filter_type):
        normlized_fs = transition_width / fs
        half_list = []
        full_list = []

        if filter_type == "low_pass":
            signal = self.filter_low_pass(stop_band_att, normlized_fs, transition_width, fs, passband_edge_freq_1,
                                          half_list, full_list)
        if filter_type == "high_pass":
            signal = self.filter_high_pass(stop_band_att, normlized_fs, transition_width, fs, passband_edge_freq_1,
                                           half_list, full_list)
        if filter_type == "band_pass":
            signal = self.filter_band_pass(stop_band_att, normlized_fs, transition_width, fs, passband_edge_freq_1,
                                           passband_edge_freq_2,
                                           half_list, full_list)
        if filter_type == "stop_pass":
            signal = self.filter_stop_pass(stop_band_att, normlized_fs, transition_width, fs, passband_edge_freq_1,
                                           passband_edge_freq_2,
                                           half_list, full_list)
        return signal

    def filter_low_pass(self, stop_band_att, normlized_fs, transition_width, fs, passband_edge_freq_1, half_list,
                        full_list):
        if stop_band_att <= 21:
            n = math.ceil(0.9 / normlized_fs)
            if n % 2 == 0:
                n += 1
            n_for_loop = int((np.abs(n) - 1) / 2)

            new_fc = (passband_edge_freq_1 + (transition_width / 2)) / fs
            for i in range(n_for_loop + 1):
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

            for i in range(n_for_loop + 1):
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

            for i in range(n_for_loop + 1):
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

            for i in range(n_for_loop + 1):
                if i == 0:
                    hd = 2 * new_fc
                else:
                    hd = (2 * new_fc) * (math.sin(2 * math.pi * new_fc * i) / (2 * math.pi * new_fc * i))

                w = 0.42 + 0.5 * math.cos((2 * math.pi * i) / (n - 1)) + 0.08 * math.cos((4 * math.pi * i) / (n - 1))
                hdTw = hd * w
                half_list.append(hdTw)

        for j in range(-n_for_loop, n_for_loop + 1):
            if j < 0:
                full_list.append((j, half_list[-n_for_loop + np.abs(j) - 1]))
            elif j == 0:
                full_list.append((j, half_list[0]))
            else:
                full_list.append((j, half_list[j]))

        return full_list

    def filter_high_pass(self, stop_band_att, normlized_fs, transition_width, fs, passband_edge_freq_1, half_list,
                         full_list):
        if stop_band_att <= 21:
            n = math.ceil(0.9 / normlized_fs)
            if n % 2 == 0:
                n += 1
            n_for_loop = int((np.abs(n) - 1) / 2)

            new_fc = (passband_edge_freq_1 - (transition_width / 2)) / fs

            for i in range(n_for_loop + 1):
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

            for i in range(n_for_loop + 1):
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

            for i in range(n_for_loop + 1):
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

            for i in range(n_for_loop + 1):
                if i == 0:
                    hd = 1 - (2 * new_fc)
                else:
                    hd = -1 * ((2 * new_fc) * (math.sin(2 * math.pi * new_fc * i) / (2 * math.pi * new_fc * i)))

                w = 0.42 + 0.5 * math.cos((2 * math.pi * i) / (n - 1)) + 0.08 * math.cos((4 * math.pi * i) / (n - 1))
                hdTw = hd * w
                half_list.append(hdTw)

        for j in range(-n_for_loop, n_for_loop + 1):
            if j < 0:
                full_list.append((j, half_list[-n_for_loop + np.abs(j) - 1]))
            elif j == 0:
                full_list.append((j, half_list[0]))
            else:
                full_list.append((j, half_list[j]))

        return full_list

    def filter_band_pass(self, stop_band_att, normlized_fs, transition_width, fs, passband_edge_freq_1,
                         passband_edge_freq_2, half_list,
                         full_list):
        if stop_band_att <= 21:
            n = math.ceil(0.9 / normlized_fs)
            if n % 2 == 0:
                n += 1
            new_fc1 = passband_edge_freq_1 - (transition_width / 2) / fs
            new_fc2 = passband_edge_freq_2 + (transition_width / 2) / fs
            n_for_loop = int((np.abs(n) - 1) / 2)

            for i in range(n_for_loop + 1):
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
            new_fc1 = passband_edge_freq_1 - (transition_width / 2) / fs
            new_fc2 = passband_edge_freq_2 + (transition_width / 2) / fs
            n_for_loop = int((np.abs(n) - 1) / 2)

            for i in range(n_for_loop + 1):
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
            new_fc1 = passband_edge_freq_1 - (transition_width / 2) / fs
            new_fc2 = passband_edge_freq_2 + (transition_width / 2) / fs
            n_for_loop = int((np.abs(n) - 1) / 2)

            for i in range(n_for_loop + 1):
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
            new_fc1 = passband_edge_freq_1 - (transition_width / 2) / fs
            new_fc2 = passband_edge_freq_2 + (transition_width / 2) / fs
            n_for_loop = int((np.abs(n) - 1) / 2)

            for i in range(n_for_loop + 1):
                if i == 0:
                    hd = 2 * (new_fc2 - new_fc1)
                else:
                    hd = (2 * new_fc2) * (math.sin(2 * math.pi * new_fc2 * i) / (2 * math.pi * new_fc2 * i)) - (
                            2 * new_fc1) * (math.sin(2 * math.pi * new_fc1 * i) / (2 * math.pi * new_fc1 * i))

                w = 0.42 + 0.5 * math.cos((2 * math.pi * i) / (n - 1)) + 0.08 * math.cos((4 * math.pi * i) / (n - 1))
                hdTw = hd * w
                half_list.append(hdTw)

        for j in range(-n_for_loop, n_for_loop + 1):
            if j < 0:
                full_list.append((j, half_list[-n_for_loop + np.abs(j) - 1]))
            elif j == 0:
                full_list.append((j, half_list[0]))
            else:
                full_list.append((j, half_list[j]))

        return full_list

    def filter_stop_pass(self, stop_band_att, normlized_fs, transition_width, fs, passband_edge_freq_1,
                         passband_edge_freq_2, half_list, full_list):
        if stop_band_att <= 21:
            n = math.ceil(0.9 / normlized_fs)
            if n % 2 == 0:
                n += 1
            new_fc1 = passband_edge_freq_1 + (transition_width / 2) / fs
            new_fc2 = passband_edge_freq_2 - (transition_width / 2) / fs
            n_for_loop = int((np.abs(n) - 1) / 2)

            for i in range(n_for_loop + 1):
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
            new_fc1 = passband_edge_freq_1 + (transition_width / 2) / fs
            new_fc2 = passband_edge_freq_2 - (transition_width / 2) / fs
            n_for_loop = int((np.abs(n) - 1) / 2)

            for i in range(n_for_loop + 1):
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
            new_fc1 = passband_edge_freq_1 + (transition_width / 2) / fs
            new_fc2 = passband_edge_freq_2 - (transition_width / 2) / fs
            n_for_loop = int((np.abs(n) - 1) / 2)

            for i in range(n_for_loop + 1):
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
            new_fc1 = passband_edge_freq_1 + (transition_width / 2) / fs
            new_fc2 = passband_edge_freq_2 - (transition_width / 2) / fs
            n_for_loop = int((np.abs(n) - 1) / 2)

            for i in range(n_for_loop + 1):
                if i == 0:
                    hd = -2 * (new_fc2 - new_fc1)
                else:
                    hd = -1 * (2 * new_fc2) * (math.sin(2 * math.pi * new_fc2 * i) / (2 * math.pi * new_fc2 * i)) + (
                            2 * new_fc1) * (math.sin(2 * math.pi * new_fc1 * i) / (2 * math.pi * new_fc1 * i))

                w = 0.42 + 0.5 * math.cos((2 * math.pi * i) / (n - 1)) + 0.08 * math.cos((4 * math.pi * i) / (n - 1))
                hdTw = hd * w
                half_list.append(hdTw)

        for j in range(-n_for_loop, n_for_loop + 1):
            if j < 0:
                full_list.append((j, half_list[-n_for_loop + np.abs(j) - 1]))
            elif j == 0:
                full_list.append((j, half_list[0]))
            else:
                full_list.append((j, half_list[j]))

        return full_list

    def toggle_filter_button(self):
        # Enable/Disable the choose_file_button based on the checkbox state
        if self.use_filter_checkbox_var.get():
            self.choose_file_button["state"] = "normal"
        else:
            self.choose_file_button["state"] = "disabled"

    def toggle_filter_options(self):
        # Enable/Disable the "Use Filter" checkbox based on the new checkbox state
        if self.use_low_pass_only_var.get():
            self.use_filter_checkbox_var.set(1)  # Set "Use Filter" checkbox to true
            self.toggle_filter_button()
            self.filter_type_menu["menu"].delete(0, "end")  # Clear existing options
            self.filter_type_menu["menu"].add_command(label="low_pass",
                                                      command=tk._setit(self.filter_type_var, "low_pass"))
        else:
            # turn check box off
            self.use_filter_checkbox_var.set(0)  # Set "Use Filter" checkbox to true
            self.toggle_filter_button()

            self.filter_type_menu["menu"].delete(0, "end")  # Clear existing options
            self.filter_type_menu["menu"].add_command(label="low_pass",
                                                      command=tk._setit(self.filter_type_var, "low_pass"))
            self.filter_type_menu["menu"].add_command(label="high_pass",
                                                      command=tk._setit(self.filter_type_var, "high_pass"))
            self.filter_type_menu["menu"].add_command(label="band_pass",
                                                      command=tk._setit(self.filter_type_var, "band_pass"))
            self.filter_type_menu["menu"].add_command(label="stop_pass",
                                                      command=tk._setit(self.filter_type_var, "stop_pass"))

    def multiply_signal_with_filter(self, signal, filter):
        # Perform element-wise multiplication of signal and filter
        return [(point[0], point[1] * filter_value) for point, filter_value in zip(signal, filter)]

    # apply the filter on signal
    def conv(self, signal, filter):
        # print("signal:", signal)
        # print("filter:", filter)
        # res = []
        # n = len(signal) + len(filter) - 1
        # result = [0] * n
        # signal_padded = [0] * (len(filter) - 1) + signal + [0] * (len(filter) - 1)
        #
        #
        # for i in range(n):
        #     for j in range(len(filter)):
        #         result[i] += signal_padded[i - j + len(filter) - 1] * float(filter[j][1])
        #         # print(f"Index: {i - j + len(filter) - 1}")
        #         # print(f"Signal element: {signal_padded[i - j + len(filter) - 1]}")
        #         # print(f"Filter element: {float(filter[j][1])}")
        #     res.append(result[i])

        leng = len(signal) + len(filter) - 1
        result_i = [0] * leng
        signal_padded = [0] * (len(filter) - 1) + signal + [0] * (len(filter) - 1)
        for i in range(leng):
            for j in range(len(filter)):
                result_i[i] += signal_padded[i - j + len(filter) - 1] * filter[j]
            res.append(result_i[i])
        return res

    def up_resample(self, signal, l_factor):
        upscaled = []
        for i in range(len(signal)):
            upscaled.append(signal[i])
            for j in range(l_factor - 1):
                upscaled.append(signal[i] * (l_factor - 1 - j) / l_factor)
        return upscaled

    def down_resample(self, signal, m_factor):
        downscaled = []
        for i in range(len(signal)):
            if i % m_factor != 0:
                continue
            downscaled.append(signal[i])
        return downscaled

    def resampling(self, signal, l_factor, m_factor, stop_band_att, normalized_fs, transition_width, fs,
                   passband_edge_freq_1, half_list, full_list):
        resampled_signal = []
        filter_coeff = []
        final_signal = []

        if l_factor > 0 and m_factor == 0:
            resampled_signal = self.up_resample(signal, l_factor)
            filter_coeff = self.filter_low_pass(stop_band_att, normalized_fs, transition_width, fs,
                                                passband_edge_freq_1, half_list, full_list)
            final_signal = self.conv(resampled_signal, filter_coeff)
            return final_signal

        if m_factor > 0 and l_factor == 0:
            filter_coeff = self.filter_low_pass(stop_band_att, normalized_fs, transition_width, fs,
                                                passband_edge_freq_1, half_list, full_list)
            resampled_signal = self.down_resample(signal, m_factor)
            final_signal = self.conv(resampled_signal, filter_coeff)
            return final_signal

        if m_factor > 0 and l_factor > 0:
            resampled_signal = self.up_resample(signal, l_factor)
            filter_coeff = self.filter_low_pass(stop_band_att, normalized_fs, transition_width, fs,
                                                passband_edge_freq_1, half_list, full_list)
            final_signal = self.down_resample(self.conv(resampled_signal, filter_coeff), m_factor)
            return final_signal
        else:
            return "error"

    def plot_signal(self, original_signal, filtered_signal):
        original_x = [point[0] for point in original_signal]
        original_y = [point[1] for point in original_signal]

        filtered_x = [point[0] for point in filtered_signal]
        filtered_y = [point[1] for point in filtered_signal]

        plt.plot(original_x, original_y, label="Original Signal")
        plt.plot(filtered_x, filtered_y, label="Filtered Signal")
        plt.xlabel("Time or Frequency")
        plt.ylabel("Amplitude")
        plt.legend()
        plt.show()

    def choose_file(self):
        file_path = filedialog.askopenfilename()
        # print("File chosen:", file_path)

        # Read points and metadata from the file
        global points
        points = self.read_points_and_metadata_from_file(file_path)
        print("Points:", points)

    def read_points_and_metadata_from_file(self, file_path):
        points = []
        global SignalType, IsPeriodic, X_label
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

    def save_filtered_signal_to_file(self, signal, file_path):
        if not signal:
            print("No signal to save.")
            return

        try:
            with open(file_path, 'w') as file:
                # Save signal type, periodicity, and size
                file.write(f"{0}\n")
                file.write(f"{0}\n")
                file.write(f"{len(signal)}\n")

                # Save the signal data
                for point in signal:
                    file.write(f"{point[0]} {point[1]}\n")

            print(f"Filtered signal saved to {file_path}")
        except Exception as e:
            print(f"An error occurred while saving the filtered signal: {str(e)}")

    def choose_compare_file(self):
        # Open a file dialog to choose a file for comparison
        self.compare_file_path = filedialog.askopenfilename()
        # print("File chosen for comparison:", self.compare_file_path)

    def compare_files(self, file_name, Your_indices, Your_samples):
        expected_indices = []
        expected_samples = []

        try:
            with open(file_name, 'r') as f:
                # Skipping the first four lines
                for _ in range(4):
                    line = f.readline()

                # Reading the rest of the lines
                while line:
                    L = line.strip()
                    if len(L.split(' ')) == 2:
                        L = L.split(' ')
                        V1 = int(L[0])
                        V2 = float(L[1])
                        expected_indices.append(V1)
                        expected_samples.append(V2)
                        line = f.readline()
                    else:
                        break

            print("Current Output Test file is:")
            print(file_name)
            print("\n")

            if len(expected_samples) != len(Your_samples) or len(expected_indices) != len(Your_indices):
                print("Test case failed, your signal has a different length from the expected one")
                return

            for i in range(len(Your_indices)):
                if Your_indices[i] != expected_indices[i]:
                    print("Test case failed, your signal has different indices from the expected one")
                    return

            for i in range(len(expected_samples)):
                if abs(Your_samples[i] - expected_samples[i]) < 0.01:
                    continue
                else:
                    print("Test case failed, your signal has different values from the expected one")
                    return

            print("Test case passed successfully")

        except Exception as e:
            print(f"An error occurred during file comparison: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FilterApp(root)
    root.mainloop()
