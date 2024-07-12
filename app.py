import tkinter as tk
from TestingSimulator import MaterialTestingSimulator
from DataCollector import DataCollector
from MainFrame import MainFrame
from InputFrame import InputFrame
from math import pi

class App:
    def __init__(self, root, serial_place):
        self.root = root
        self.root.title("Data Collection and Graphing")
        
        self.data_collector = DataCollector(serial_place)
        self.testing_simulator = MaterialTestingSimulator(self.root)
        
        self.show_input_frame()

    def show_input_frame(self):
        self.input_frame = InputFrame(self.root, self.on_submit)
        self.input_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

    def on_submit(self, shape, diameter, width, height, initial_length):
        if shape == "rounded":
            data = {
                "shape": shape,
                "diameter": diameter,
                "area": ((pi / 4) * (diameter ** 2)) * (10 ** -6),
                "initial_length": initial_length
            }
        else:
            data = {
                "shape": shape,
                "width": width,
                "height": height,
                "area": (width * height) * (10 ** -6),
                "initial_length": initial_length
            }

        self.input_frame.grid_remove()
        self.show_main_frame(data)

    def show_main_frame(self, data):
        self.main_frame = MainFrame(self.root, data, self.data_collector, self.testing_simulator)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root, "COM4")
    root.mainloop()
    