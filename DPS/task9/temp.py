
import tkinter as tk
from tkinter import ttk
import numpy as np
import math
import matplotlib.pyplot as plt
from tkinter import filedialog


def filter(signal, passband_edge_freq_1 , passband_edge_freq_2, transition_width, stop_band_att, fs, filter_type):

    normlized_fs = transition_width / fs
    half_list = []
    full_list = []

    if filter_type == "low_pass" :
        if stop_band_att <= 21:
            n = math.ceil(0.9 / normlized_fs)
            if n % 2 == 0 :
                n += 1
            n_for_loop =int( ( np.abs(n) -1 ) / 2 )

            new_fc = (passband_edge_freq_1 + ( transition_width / 2)) / fs
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
            if n % 2 == 0 :
                n += 1
            n_for_loop =int( ( np.abs(n) -1 ) / 2 )

            new_fc = (passband_edge_freq_1 + ( transition_width / 2)) / fs

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
            if n % 2 == 0 :
                n += 1
            n_for_loop =int( ( np.abs(n) -1 ) / 2 )
            new_fc = (passband_edge_freq_1 + ( transition_width / 2)) / fs

            for i in range( n_for_loop + 1):
                if i == 0:
                    hd = 2 * new_fc
                else:
                    hd = (2 * new_fc) * (math.sin(2 * math.pi * new_fc * i) / (2 * math.pi * new_fc * i))

                w = 0.54 + 0.46 * math.cos(2 * math.pi * i / n )

                hdTw = hd * w
                half_list.append(hdTw)


        elif stop_band_att <= 74:
            n = math.ceil(5.5 / normlized_fs)
            if n % 2 == 0 :
                n += 1
            n_for_loop =int( ( np.abs(n) -1 ) / 2 )

            new_fc = (passband_edge_freq_1 + ( transition_width / 2)) / fs

            for i in range( n_for_loop + 1 ):
                if i == 0:
                    hd = 2 * new_fc
                else:
                    hd = (2 * new_fc) * (math.sin(2 * math.pi * new_fc * i) / (2 * math.pi * new_fc * i))

                w = 0.42 + 0.5 * math.cos((2 * math.pi * i) / (n - 1) ) + 0.08 * math.cos((4 * math.pi * i) / (n - 1))
                hdTw = hd * w
                half_list.append(hdTw)


        for j in range(-n_for_loop, n_for_loop + 1):
            if j < 0:
                full_list.append((j, half_list[-n_for_loop + np.abs(j) - 1]))
            elif j == 0:
                full_list.append((j, half_list[0]))
            else:
                full_list.append((j, half_list[j]))

        signal = full_list



    if filter_type == "high_pass":
        if stop_band_att <= 21:
            n = math.ceil(0.9/ normlized_fs)
            if n % 2 == 0 :
                n += 1
            n_for_loop =int( ( np.abs(n) -1 ) / 2 )

            new_fc = (passband_edge_freq_1 - ( transition_width / 2)) / fs

            for i in range(n_for_loop + 1):
                if i == 0:
                    hd = 1 - (2 *new_fc)
                else:
                    hd = -1 * ((2 * new_fc) * (math.sin(2 * math.pi * new_fc * i) / (2 * math.pi * new_fc * i)))

                w = 1
                hdTw = hd * w
                half_list.append(hdTw)

        elif stop_band_att <= 44:
            n = math.ceil(3.1 / normlized_fs)
            if n % 2 == 0 :
                n += 1
            n_for_loop =int( ( np.abs(n) -1 ) / 2 )

            new_fc = (passband_edge_freq_1 - ( transition_width / 2)) / fs

            for i in range(n_for_loop + 1):
                if i == 0:
                    hd = 1 - (2 *new_fc)
                else:
                    hd = -1 * ((2 * new_fc) * (math.sin(2 * math.pi * new_fc * i) / (2 * math.pi * new_fc * i)))

                w = 0.54 + 0.5 * math.cos(2 * math.pi * i / n)
                hdTw = hd * w
                half_list.append(hdTw)

        elif stop_band_att <= 53:
            n = math.ceil(3.3 / normlized_fs)
            if n % 2 == 0 :
                n += 1
            n_for_loop =int( ( np.abs(n) -1 ) / 2 )

            new_fc = (passband_edge_freq_1 - ( transition_width / 2)) / fs

            for i in range(n_for_loop + 1):
                if i == 0:
                    hd = 1 - (2 *new_fc)
                else:
                    hd = -1 * ((2 * new_fc) * (math.sin(2 * math.pi * new_fc * i) / (2 * math.pi * new_fc * i)))

                w = 0.54 + 0.46 * math.cos(2 * math.pi * i / n)
                hdTw = hd * w
                half_list.append(hdTw)

        elif stop_band_att <= 74:
            n = math.ceil(5.5 / normlized_fs)
            if n % 2 == 0 :
                n += 1
            n_for_loop =int( ( np.abs(n) -1 ) / 2 )


            new_fc = (passband_edge_freq_1 - ( transition_width / 2)) / fs

            for i in range(n_for_loop + 1):

                # print(i)
                if i == 0:
                    hd = 1 - (2 *new_fc)
                else:
                    hd = -1 * ((2 * new_fc) * (math.sin(2 * math.pi * new_fc * i) / (2 * math.pi * new_fc * i)))

                w = 0.42 + 0.5 * math.cos((2 * math.pi * i) / (n - 1) ) + 0.08 * math.cos((4 * math.pi * i) / (n - 1))
                hdTw = hd * w
                half_list.append(hdTw)
                # if i == 0:
                #     print(half_list)
                #
                #     break

        for j in range(-n_for_loop, n_for_loop + 1):
            if j < 0:
                full_list.append((j, half_list[-n_for_loop + np.abs(j) - 1]))
            elif j == 0:
                full_list.append((j, half_list[0]))
            else:
                full_list.append((j, half_list[j]))

        signal = full_list




    if filter_type == "band_pass" :
        if stop_band_att <= 21:
            n = math.ceil(0.9/ normlized_fs)
            if n % 2 == 0 :
                n += 1
            new_fc1 = passband_edge_freq_1 - (transition_width / 2)
            new_fc2 = passband_edge_freq_2 + (transition_width / 2)
            n_for_loop =int( ( np.abs(n) -1 ) / 2 )


            for i in range(n_for_loop):
                if i == 0:
                    hd = 2 *(new_fc2 - new_fc1)
                else:
                    hd = (2 * new_fc2) * (math.sin(2 * math.pi * new_fc2 * i) / (2 * math.pi * new_fc2 * i)) - (2 * new_fc1) * (math.sin(2 * math.pi * new_fc1 * i) / (2 * math.pi * new_fc1 * i))

                w = 1
                hdTw = hd * w
                half_list.append(hdTw)

        elif stop_band_att <= 44:
            n = math.ceil(3.1 / normlized_fs)
            if n % 2 == 0 :
                n += 1
            new_fc1 = passband_edge_freq_1 - (transition_width / 2)
            new_fc2 = passband_edge_freq_2 + (transition_width / 2)
            n_for_loop =int( ( np.abs(n) -1 ) / 2 )


            for i in range(n_for_loop):
                if i == 0:
                    hd = 2 *(new_fc2 - new_fc1)
                else:
                    hd = (2 * new_fc2) * (math.sin(2 * math.pi * new_fc2 * i) / (2 * math.pi * new_fc2 * i)) - (2 * new_fc1) * (math.sin(2 * math.pi * new_fc1 * i) / (2 * math.pi * new_fc1 * i))

                w = 0.54 + 0.5 * math.cos(2 * math.pi * i / n)
                hdTw = hd * w
                half_list.append(hdTw)

        elif stop_band_att <= 53:
            n = math.ceil(3.3 / normlized_fs)
            if n % 2 == 0 :
                n += 1
            new_fc1 = passband_edge_freq_1 - (transition_width / 2)
            new_fc2 = passband_edge_freq_2 + (transition_width / 2)
            n_for_loop =int( ( np.abs(n) -1 ) / 2 )


            for i in range(n_for_loop):
                if i == 0:
                    hd = 2 *(new_fc2 - new_fc1)
                else:
                    hd = (2 * new_fc2) * (math.sin(2 * math.pi * new_fc2 * i) / (2 * math.pi * new_fc2 * i)) - (2 * new_fc1) * (math.sin(2 * math.pi * new_fc1 * i) / (2 * math.pi * new_fc1 * i))

                w = 0.54 + 0.46 * math.cos(2 * math.pi * i / n)
                hdTw = hd * w
                half_list.append(hdTw)

        elif stop_band_att <= 74:
            n = math.ceil(5.5 / normlized_fs)
            if n % 2 == 0 :
                n += 1
            new_fc1 = passband_edge_freq_1 - (transition_width / 2)
            new_fc2 = passband_edge_freq_2 + (transition_width / 2)
            n_for_loop =int( ( np.abs(n) -1 ) / 2 )


            for i in range(n_for_loop):
                if i == 0:
                    hd = 2 *(new_fc2 - new_fc1)
                else:
                    hd = (2 * new_fc2) * (math.sin(2 * math.pi * new_fc2 * i) / (2 * math.pi * new_fc2 * i)) - (2 * new_fc1) * (math.sin(2 * math.pi * new_fc1 * i) / (2 * math.pi * new_fc1 * i))

                w = 0.42 + 0.5 * math.cos((2 * math.pi * i) / (n - 1) ) + 0.08 * math.cos((4 * math.pi * i) / (n - 1))
                hdTw = hd * w
                half_list.append(hdTw)

        for j in range(-n_for_loop, n_for_loop + 1):
            if j < 0:
                full_list.append((j, half_list[-n_for_loop + np.abs(j) - 1]))
            elif j == 0:
                full_list.append((j, half_list[0]))
            else:
                full_list.append((j, half_list[j]))

        signal = full_list


    if filter_type == "stop_pass" :
        if stop_band_att <= 21:
            n = math.ceil(0.9/ normlized_fs)
            if n % 2 == 0 :
                n += 1
            new_fc1 = passband_edge_freq_1 + (transition_width / 2)
            new_fc2 = passband_edge_freq_2 - (transition_width / 2)
            n_for_loop =int( ( np.abs(n) -1 ) / 2 )


            for i in range(n_for_loop):
                if i == 0:
                    hd = -2 *(new_fc2 - new_fc1)
                else:
                    hd = -1 * (2 * new_fc2) * (math.sin(2 * math.pi * new_fc2 * i) / (2 * math.pi * new_fc2 * i)) + (2 * new_fc1) * (math.sin(2 * math.pi * new_fc1 * i) / (2 * math.pi * new_fc1 * i))

                w = 1
                hdTw = hd * w
                half_list.append(hdTw)

        elif stop_band_att <= 44:
            n = math.ceil(3.1 / normlized_fs)
            if n % 2 == 0 :
                n += 1
            new_fc1 = passband_edge_freq_1 + (transition_width / 2)
            new_fc2 = passband_edge_freq_2 - (transition_width / 2)
            n_for_loop =int( ( np.abs(n) -1 ) / 2 )


            for i in range(n_for_loop):
                if i == 0:
                    hd = -2 *(new_fc2 - new_fc1)
                else:
                    hd = -1 * (2 * new_fc2) * (math.sin(2 * math.pi * new_fc2 * i) / (2 * math.pi * new_fc2 * i)) + (2 * new_fc1) * (math.sin(2 * math.pi * new_fc1 * i) / (2 * math.pi * new_fc1 * i))

                w = 0.54 + 0.5 * math.cos(2 * math.pi * i / n)
                hdTw = hd * w
                half_list.append(hdTw)


        elif stop_band_att <= 53:
            n = math.ceil(3.3 / normlized_fs)
            if n % 2 == 0 :
                n += 1
            new_fc1 = passband_edge_freq_1 + (transition_width / 2)
            new_fc2 = passband_edge_freq_2 - (transition_width / 2)
            n_for_loop =int( ( np.abs(n) -1 ) / 2 )


            for i in range(n_for_loop):
                if i == 0:
                    hd = -2 *(new_fc2 - new_fc1)
                else:
                    hd = -1 * (2 * new_fc2) * (math.sin(2 * math.pi * new_fc2 * i) / (2 * math.pi * new_fc2 * i)) + (2 * new_fc1) * (math.sin(2 * math.pi * new_fc1 * i) / (2 * math.pi * new_fc1 * i))

                w = 0.54 + 0.46 * math.cos(2 * math.pi * i / n)
                hdTw = hd * w
                half_list.append(hdTw)

        elif stop_band_att <= 74:
            n = math.ceil(5.5 / normlized_fs)
            if n % 2 == 0 :
                n += 1
            new_fc1 = passband_edge_freq_1 + (transition_width / 2)
            new_fc2 = passband_edge_freq_2 - (transition_width / 2)
            n_for_loop =int( ( np.abs(n) -1 ) / 2 )


            for i in range(n_for_loop):
                if i == 0:
                    hd = -2 *(new_fc2 - new_fc1)
                else:
                    hd = -1 * (2 * new_fc2) * (math.sin(2 * math.pi * new_fc2 * i) / (2 * math.pi * new_fc2 * i)) + (2 * new_fc1) * (math.sin(2 * math.pi * new_fc1 * i) / (2 * math.pi * new_fc1 * i))

                w = 0.42 + 0.5 * math.cos((2 * math.pi * i) / (n - 1) ) + 0.08 * math.cos((4 * math.pi * i) / (n - 1))
                hdTw = hd * w
                half_list.append(hdTw)

        for j in range(-n_for_loop, n_for_loop + 1):
            if j < 0:
                full_list.append((j, half_list[-n_for_loop + np.abs(j) - 1]))
            elif j == 0:
                full_list.append((j, half_list[0]))
            else:
                full_list.append((j, half_list[j]))

        signal = full_list


    print(len( half_list))
    print(half_list)
    print(signal)

sig = []
filter(sig, 1500, 0,500, 50, 8000, "low_pass")


