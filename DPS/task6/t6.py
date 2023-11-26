import tkinter as tk
from tkinter import filedialog, messagebox
from typing import List, Any
from derivative import DerivativeSignal
import numpy as np


class SignalProcessingApp:
    points1: list[list[Any]]

    def __init__(self, master):
        self.points2 = None
        self.master = master
        master.title("Signal Processing Tool")

        # Set the initial size of the window
        master.geometry("80x60")

        self.task6_button = tk.Button(master, text="Task 6", command=self.open_task6_frame)
        self.task6_button.pack()

    def open_task6_frame(self):
        task6_frame = tk.Toplevel(self.master)
        task6_frame.title("Task 6 Options")

        # Set the size of the internal frame
        task6_frame.geometry("600x400")

        # Buttons for each operation
        smoothing_button = tk.Button(task6_frame, text="1. Smoothing", command=self.open_smoothing_frame)
        smoothing_button.pack()

        sharpening_button = tk.Button(task6_frame, text="2. Sharpening",
                                      command=lambda: self.perform_operation("Sharpening"))
        sharpening_button.pack()

        delay_advance_button = tk.Button(task6_frame, text="3. Delaying/Advancing", command=lambda: DerivativeSignal())
        delay_advance_button.pack()

        fold_button = tk.Button(task6_frame, text="4. Folding", command=lambda: self.perform_operation("Folding"))
        fold_button.pack()

        delay_advance_folded_button = tk.Button(task6_frame, text="5. Delay/Advance Folded Signal",
                                                command=lambda: self.perform_operation("Delay/Advance Folded"))
        delay_advance_folded_button.pack()

        remove_dc_component_button = tk.Button(task6_frame, text="6. Remove DC Component",
                                               command=lambda: self.perform_operation("Remove DC Component"))
        remove_dc_component_button.pack()

        convolve_signals_button = tk.Button(task6_frame, text="7. Convolve Two Signals",
                                            command=self.open_convolve_frame)
        convolve_signals_button.pack()

    def open_convolve_frame(self):
        convolve_frame = tk.Toplevel(self.master)
        convolve_frame.title("Convolution Options")
        convolve_frame.geometry("400x200")

        choose_file_button1 = tk.Button(convolve_frame, text="Choose First Signal",
                                        command=lambda: self.read_and_store_points(1))
        choose_file_button1.pack()

        choose_file_button2 = tk.Button(convolve_frame, text="Choose Second Signal",
                                        command=lambda: self.read_and_store_points(2))
        choose_file_button2.pack()

        execute_button = tk.Button(convolve_frame, text="Execute Convolution", command=self.perform_convolution)
        execute_button.pack()

    def perform_convolution(self):
        if not hasattr(self, 'points1') or not hasattr(self, 'points2'):
            self.display_error_message("Please choose both signals first.", 3)
            return

        try:
            # Extract the y values from the stored points
            signal1 = np.array([point[1] for point in self.points1])
            signal2 = np.array([point[1] for point in self.points2])

            # Perform custom convolution
            result = self.convolve_custom(signal1, signal2)

            # Do something with the result, like display it or use it further
            print("Convolution Result:", result)

            # Call the ConvTest function to perform the test
            self.ConvTest(np.arange(len(result)) - 2, result)

            self.show_message("Operation", "Convolution completed")

            # You can add further actions specific to the Convolution operation here

        except Exception as e:
            self.display_error_message(f"An error occurred: {str(e)}", 3)

    def convolve_custom(self, signal1, signal2):
        len1, len2 = len(signal1), len(signal2)
        result_len = len1 + len2 - 1
        result = np.zeros(result_len)

        # Perform convolution
        for i in range(result_len):
            for j in range(len1):
                if i - j >= 0 and i - j < len2:
                    result[i] += signal1[j] * signal2[i - j]

        return result

    def ConvTest(self, Your_indices, Your_samples):
        expected_indices = [-2, -1, 0, 1, 2, 3, 4, 5, 6]
        expected_samples = [1, 1, -1, 0, 0, 3, 3, 2, 1]

        if len(expected_samples) != len(Your_samples) or len(expected_indices) != len(Your_indices):
            print("Conv Test case failed, your signal has a different length from the expected one")
            return
        for i in range(len(Your_indices)):
            if Your_indices[i] != expected_indices[i]:
                print("Conv Test case failed, your signal has different indices from the expected one")
                return
        for i in range(len(expected_samples)):
            if abs(Your_samples[i] - expected_samples[i]) < 0.01:
                continue
            else:
                print("Conv Test case failed, your signal has different values from the expected one")
                return
        print("Conv Test case passed successfully")

    def open_smoothing_frame(self):
        smoothing_frame = tk.Toplevel(self.master)
        smoothing_frame.title("Smoothing Options")
        smoothing_frame.geometry("400x200")

        choose_file_button = tk.Button(smoothing_frame, text="Choose File", command=self.read_and_store_points)
        choose_file_button.pack()

        input_label = tk.Label(smoothing_frame, text="Enter the number of points for smoothing:")
        input_label.pack()

        self.smoothing_input = tk.Entry(smoothing_frame)
        self.smoothing_input.pack()

        perform_smoothing_button = tk.Button(smoothing_frame, text="Perform Smoothing", command=self.perform_smoothing)
        perform_smoothing_button.pack()

    def read_and_store_points(self, signal_number):
        file_path = self.open_file_dialog()
        signal_type, is_periodic, points = self.read_points_and_metadata_from_file(file_path)

        if signal_number == 1:
            self.points1 = points
        elif signal_number == 2:
            self.points2 = points
        elif signal_number == 0:
            self.points0 = points  # For smoothing

    def read_and_store_points(self, signal_number):
        file_path = self.open_file_dialog()
        signal_type, is_periodic, points = self.read_points_and_metadata_from_file(file_path)

        if signal_number == 1:
            self.points1 = points
        elif signal_number == 2:
            self.points2 = points

    def read_points_and_metadata_from_file(self, file_path):
        points = []
        SignalType, IsPeriodic, size = None, None, None

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

            except Exception as e:
                print(f"An error occurred: {str(e)}")
                self.display_error_message("An error occurred. Choose a file and try again.", 3)

        return SignalType, IsPeriodic, points

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename()
        return file_path

    def perform_operation(self, operation):
        self.show_message("Operation", f"Performing {operation} operation")

    def perform_smoothing(self):
        try:
            num_points = int(self.smoothing_input.get())
            # Perform smoothing operation with num_points
            self.show_message("Smoothing", f"Performing smoothing with {num_points} points")
        except ValueError:
            self.display_error_message("Please enter a valid number of points.", 3)

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def display_error_message(self, message, duration):
        messagebox.showerror("Error", message)
        self.master.after(duration * 1000, lambda: self.close_error_message())

    def close_error_message(self):
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SignalProcessingApp(root)
    root.mainloop()
