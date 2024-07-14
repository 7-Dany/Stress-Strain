import tkinter as tk
from TestingSimulator import MaterialTestingSimulator
from DataCollector import DataCollector
from MainFrame import MainFrame
from InputFrame import InputFrame
from math import pi

class App:
    """
    Main application class managing the GUI and data flow for material testing simulation.

    Attributes:
        root (tk.Tk): The main tkinter root window.
        data_collector (DataCollector): Instance of DataCollector for collecting data from a serial port.
        testing_simulator (MaterialTestingSimulator): Instance of MaterialTestingSimulator for simulation.
        input_frame (InputFrame): Instance of InputFrame for gathering input parameters.
        main_frame (MainFrame): Instance of MainFrame for displaying simulation results.
    """

    def __init__(self, root, serial_place):
        """
        Initializes the application with the root window and sets up initial components.

        Args:
            root (tk.Tk): The main tkinter root window.
            serial_place (str): Serial port address for data collection.
        """
        self.root = root
        self.root.title("Data Collection and Graphing")
        
        # Initialize data collector and testing simulator
        self.data_collector = DataCollector(serial_place)
        self.testing_simulator = MaterialTestingSimulator(self.root)
        
        # Show the input frame initially
        self.show_input_frame()

    def show_input_frame(self):
        """
        Displays the input frame for gathering user input parameters.
        """
        self.input_frame = InputFrame(self.root, self.on_submit)
        self.input_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

    def on_submit(self, shape, diameter, width, height, initial_length):
        """
        Callback function called when user submits input data.

        Args:
            shape (str): Shape of the material ("rounded" or "rectangular").
            diameter (float): Diameter of the rounded material.
            width (float): Width of the rectangular material.
            height (float): Height of the rectangular material.
            initial_length (float): Initial length of the material.

        Constructs data dictionary based on shape and passes it to main frame for simulation display.
        """
        if shape == "rounded":
            data = {
                "shape": shape,
                "diameter": diameter,
                "area": (pi / 4) * (diameter ** 2),
                "initial_length": initial_length
            }
        else:
            data = {
                "shape": shape,
                "width": width,
                "height": height,
                "area": (width * height),
                "initial_length": initial_length
            }

        # Hide input frame and display main frame with collected data
        self.input_frame.grid_remove()
        self.show_main_frame(data)

    def show_main_frame(self, data):
        """
        Displays the main frame with simulation results.

        Args:
            data (dict): Dictionary containing input parameters for the simulation.
        """
        self.main_frame = MainFrame(self.root, data, self.data_collector, self.testing_simulator, self.show_input_frame)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

if __name__ == "__main__":
    # Initialize tkinter root window and application
    root = tk.Tk()
    app = App(root, "COM4")  # Replace "COM4" with the appropriate serial port
    root.mainloop()
