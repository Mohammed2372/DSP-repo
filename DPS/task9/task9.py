import tkinter as tk
from tkinter import ttk
import numpy as np
import math
import matplotlib.pyplot as plt
from tkinter import filedialog


def choosing_filter(signal, passband_edge_freq_1, passband_edge_freq_2, transition_width, stop_band_att, fs,
                    filter_type):
    normlized_fs = transition_width / fs
    half_list = []
    full_list = []

    if filter_type == "low_pass":
        filter_low_pass(stop_band_att, normlized_fs, passband_edge_freq_1, half_list)
    if filter_type == "high_pass":
        filter_high_pass(stop_band_att, normlized_fs, passband_edge_freq_1, half_list, full_list)
    if filter_type == "band_pass":
        filter_band_pass(stop_band_att, normlized_fs, passband_edge_freq_1, passband_edge_freq_2, half_list, full_list)
    if filter_type == "stop_pass":
        filter_stop_pass(stop_band_att, normlized_fs, passband_edge_freq_1, passband_edge_freq_2, half_list, full_list)


def filter_low_pass(stop_band_att, normlized_fs, passband_edge_freq_1, half_list, full_list):
    if stop_band_att <= 21:
        n = math.ceil(0.9 / normlized_fs)
        n_for_loop = (np.abs(n) - 1) / 2

        for i in n_for_loop:
            new_fc = passband_edge_freq_1 + (normlized_fs / 2)
            if n == 0:
                hd = 2 * new_fc
            else:
                hd = (2 * new_fc / 2 * math.pi * i) * math.sin(2 * math.pi * new_fc * i)

            w = 1
            hdTw = hd * w
            half_list.append(hdTw)

    elif stop_band_att <= 44:
        n = math.ceil(3.1 / normlized_fs)
        n_for_loop = (np.abs(n) - 1) / 2

        for i in n_for_loop:
            new_fc = passband_edge_freq_1 + (normlized_fs / 2)
            if n == 0:
                hd = 2 * new_fc
            else:
                hd = (2 * new_fc / 2 * math.pi * i) * math.sin(2 * math.pi * new_fc * i)

            w = 0.54 + 0.5 * math.cos(2 * math.pi * i / n)
            hdTw = hd * w
            half_list.append(hdTw)

    elif stop_band_att <= 53:
        n = math.ceil(3.3 / normlized_fs)
        n_for_loop = (np.abs(n) - 1) / 2

        for i in n_for_loop:
            new_fc = passband_edge_freq_1 + (normlized_fs / 2)
            if n == 0:
                hd = 2 * new_fc
            else:
                hd = (2 * new_fc / 2 * math.pi * i) * math.sin(2 * math.pi * new_fc * i)

            w = 0.54 + 0.46 * math.cos(2 * math.pi * i / n)
            hdTw = hd * w
            half_list.append(hdTw)

    elif stop_band_att <= 74:
        n = math.ceil(5.5 / normlized_fs)
        n_for_loop = (np.abs(n) - 1) / 2

        for i in n_for_loop:
            new_fc = passband_edge_freq_1 + (normlized_fs / 2)
            if n == 0:
                hd = 2 * new_fc
            else:
                hd = (2 * new_fc / 2 * math.pi * i) * math.sin(2 * math.pi * new_fc * i)

            w = 0.42 + 0.5 * math.cos((2 * math.pi * i) / (n - 1)) + 0.08 * math.cos((4 * math.pi * i) / (n - 1))
            hdTw = hd * w
            half_list.append(hdTw)

    for j in n:

        if j >= n_for_loop:
            full_list.append(((j - n_for_loop), half_list[j]))

        else:
            full_list.append(((j - n_for_loop), half_list[n_for_loop - j]))


def filter_high_pass(stop_band_att, normlized_fs, passband_edge_freq_1, half_list, full_list):
    if stop_band_att <= 21:
        n = math.ceil(0.9 / normlized_fs)
        n_for_loop = (np.abs(n) - 1) / 2

        for i in n_for_loop:
            new_fc = passband_edge_freq_1 + (normlized_fs / 2)
            if n == 0:
                hd = 1 - (2 * new_fc)
            else:
                hd = -1 * (2 * new_fc / 2 * math.pi * i) * math.sin(2 * math.pi * new_fc * i)

            w = 1
            hdTw = hd * w

    elif stop_band_att <= 44:
        n = math.ceil(3.1 / normlized_fs)
        n_for_loop = (np.abs(n) - 1) / 2

        for i in n_for_loop:
            new_fc = passband_edge_freq_1 + (normlized_fs / 2)
            if n == 0:
                hd = 1 - (2 * new_fc)
            else:
                hd = -1 * (2 * new_fc / 2 * math.pi * i) * math.sin(2 * math.pi * new_fc * i)

            w = 0.54 + 0.5 * math.cos(2 * math.pi * i / n)
            hdTw = hd * w

    elif stop_band_att <= 53:
        n = math.ceil(3.3 / normlized_fs)
        n_for_loop = (np.abs(n) - 1) / 2

        for i in n_for_loop:
            new_fc = passband_edge_freq_1 + (normlized_fs / 2)
            if n == 0:
                hd = 1 - (2 * new_fc)
            else:
                hd = -1 * (2 * new_fc / 2 * math.pi * i) * math.sin(2 * math.pi * new_fc * i)

            w = 0.54 + 0.46 * math.cos(2 * math.pi * i / n)
            hdTw = hd * w

    elif stop_band_att <= 74:
        n = math.ceil(5.5 / normlized_fs)
        n_for_loop = (np.abs(n) - 1) / 2

        for i in n_for_loop:
            new_fc = passband_edge_freq_1 + (normlized_fs / 2)
            if n == 0:
                hd = 1 - (2 * new_fc)
            else:
                hd = -1 * (2 * new_fc / 2 * math.pi * i) * math.sin(2 * math.pi * new_fc * i)

            w = 0.42 + 0.5 * math.cos((2 * math.pi * i) / (n - 1)) + 0.08 * math.cos((4 * math.pi * i) / (n - 1))
            hdTw = hd * w

    for j in n:

        if j >= n_for_loop:
            full_list.append(((j - n_for_loop), half_list[j]))

        else:
            full_list.append(((j - n_for_loop), half_list[n_for_loop - j]))


def filter_band_pass(stop_band_att, normlized_fs, passband_edge_freq_1, passband_edge_freq_2, half_list, full_list):
    if stop_band_att <= 21:
        n = math.ceil(0.9 / normlized_fs)
        new_fc1 = passband_edge_freq_1 + (normlized_fs / 2)
        new_fc2 = passband_edge_freq_2 + (normlized_fs / 2)
        n_for_loop = (np.abs(n) - 1) / 2

        for i in n_for_loop:

            if n == 0:
                hd = 2 * (new_fc2 - new_fc1)
            else:
                hd = (2 * new_fc2 / 2 * math.pi * i) * math.sin(2 * math.pi * new_fc2 * i) - (
                        2 * new_fc1 / 2 * math.pi * i) * math.sin(2 * math.pi * new_fc1 * i)

            w = 1
            hdTw = hd * w

    elif stop_band_att <= 44:
        n = math.ceil(3.1 / normlized_fs)
        new_fc1 = passband_edge_freq_1 + (normlized_fs / 2)
        new_fc2 = passband_edge_freq_2 + (normlized_fs / 2)

        n_for_loop = (np.abs(n) - 1) / 2

        for i in n_for_loop:
            if n == 0:
                hd = 2 * (new_fc2 - new_fc1)
            else:
                hd = (2 * new_fc2 / 2 * math.pi * i) * math.sin(2 * math.pi * new_fc2 * i) - (
                        2 * new_fc1 / 2 * math.pi * i) * math.sin(2 * math.pi * new_fc1 * i)

            w = 0.54 + 0.5 * math.cos(2 * math.pi * i / n)
            hdTw = hd * w

    elif stop_band_att <= 53:
        n = math.ceil(3.3 / normlized_fs)
        new_fc1 = passband_edge_freq_1 + (normlized_fs / 2)
        new_fc2 = passband_edge_freq_2 + (normlized_fs / 2)
        n_for_loop = (np.abs(n) - 1) / 2

        for i in n_for_loop:

            if n == 0:
                hd = 2 * (new_fc2 - new_fc1)
            else:
                hd = (2 * new_fc2 / 2 * math.pi * i) * math.sin(2 * math.pi * new_fc2 * i) - (
                        2 * new_fc1 / 2 * math.pi * i) * math.sin(2 * math.pi * new_fc1 * i)

            w = 0.54 + 0.46 * math.cos(2 * math.pi * i / n)
            hdTw = hd * w

    elif stop_band_att <= 74:
        n = math.ceil(5.5 / normlized_fs)
        new_fc1 = passband_edge_freq_1 + (normlized_fs / 2)
        new_fc2 = passband_edge_freq_2 + (normlized_fs / 2)
        n_for_loop = (np.abs(n) - 1) / 2

        for i in n_for_loop:

            if n == 0:
                hd = 2 * (new_fc2 - new_fc1)
            else:
                hd = (2 * new_fc2 / 2 * math.pi * i) * math.sin(2 * math.pi * new_fc2 * i) - (
                        2 * new_fc1 / 2 * math.pi * i) * math.sin(2 * math.pi * new_fc1 * i)

            w = 0.42 + 0.5 * math.cos((2 * math.pi * i) / (n - 1)) + 0.08 * math.cos((4 * math.pi * i) / (n - 1))
            hdTw = hd * w

    for j in n:

        if j >= n_for_loop:
            full_list.append(((j - n_for_loop), half_list[j]))

        else:
            full_list.append(((j - n_for_loop), half_list[n_for_loop - j]))


def filter_stop_pass(stop_band_att, normlized_fs, passband_edge_freq_1, passband_edge_freq_2, half_list, full_list):
    if stop_band_att <= 21:
        n = math.ceil(0.9 / normlized_fs)
        new_fc1 = passband_edge_freq_1 + (normlized_fs / 2)
        new_fc2 = passband_edge_freq_2 + (normlized_fs / 2)
        n_for_loop = (np.abs(n) - 1) / 2

        for i in n_for_loop:

            if n == 0:
                hd = 1 - (2 * (new_fc2 - new_fc1))
            else:
                hd = - (2 * new_fc2 / 2 * math.pi * i) * math.sin(2 * math.pi * new_fc2 * i) + (
                        2 * new_fc1 / 2 * math.pi * i) * math.sin(2 * math.pi * new_fc1 * i)

            w = 1
            hdTw = hd * w

    elif stop_band_att <= 44:
        n = math.ceil(3.1 / normlized_fs)
        new_fc1 = passband_edge_freq_1 + (normlized_fs / 2)
        new_fc2 = passband_edge_freq_2 + (normlized_fs / 2)

        n_for_loop = (np.abs(n) - 1) / 2

        for i in n_for_loop:
            if n == 0:
                hd = 1 - (2 * (new_fc2 - new_fc1))
            else:
                hd = - (2 * new_fc2 / 2 * math.pi * i) * math.sin(2 * math.pi * new_fc2 * i) + (
                        2 * new_fc1 / 2 * math.pi * i) * math.sin(2 * math.pi * new_fc1 * i)

            w = 0.54 + 0.5 * math.cos(2 * math.pi * i / n)
            hdTw = hd * w

    elif stop_band_att <= 53:
        n = math.ceil(3.3 / normlized_fs)
        new_fc1 = passband_edge_freq_1 + (normlized_fs / 2)
        new_fc2 = passband_edge_freq_2 + (normlized_fs / 2)
        n_for_loop = (np.abs(n) - 1) / 2

        for i in n_for_loop:

            if n == 0:
                hd = 1 - (2 * (new_fc2 - new_fc1))
            else:
                hd = - (2 * new_fc2 / 2 * math.pi * i) * math.sin(2 * math.pi * new_fc2 * i) + (
                        2 * new_fc1 / 2 * math.pi * i) * math.sin(2 * math.pi * new_fc1 * i)

            w = 0.54 + 0.46 * math.cos(2 * math.pi * i / n)
            hdTw = hd * w

    elif stop_band_att <= 74:
        n = math.ceil(5.5 / normlized_fs)
        new_fc1 = passband_edge_freq_1 + (normlized_fs / 2)
        new_fc2 = passband_edge_freq_2 + (normlized_fs / 2)
        n_for_loop = (np.abs(n) - 1) / 2

        for i in n_for_loop:

            if n == 0:
                hd = 1 - (2 * (new_fc2 - new_fc1))
            else:
                hd = - (2 * new_fc2 / 2 * math.pi * i) * math.sin(2 * math.pi * new_fc2 * i) + (
                        2 * new_fc1 / 2 * math.pi * i) * math.sin(2 * math.pi * new_fc1 * i)

            w = 0.42 + 0.5 * math.cos((2 * math.pi * i) / (n - 1)) + 0.08 * math.cos((4 * math.pi * i) / (n - 1))
            hdTw = hd * w

    for j in n:

        if j >= n_for_loop:
            full_list.append(((j - n_for_loop), half_list[j]))

        else:
            full_list.append(((j - n_for_loop), half_list[n_for_loop - j]))

    # signal = full_list    why to make variable that save full_list while you have the original list if you want to return it
