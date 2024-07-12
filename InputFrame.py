import tkinter as tk

class InputFrame(tk.Frame):
    def __init__(self, parent, on_submit):
        super().__init__(parent)
        self.on_submit = on_submit
        self.shape_var = tk.StringVar(value="rounded")
        
        self.create_widgets()
        self.update_geometry_inputs()

    def create_widgets(self):
        self.shape_label = tk.Label(self, text="Select the shape of the specimen:")
        self.shape_label.grid(row=0, column=0, pady=5, sticky="w")
        
        self.shape_option = tk.OptionMenu(self, self.shape_var, "rounded", "rectangular", command=self.update_geometry_inputs)
        self.shape_option.grid(row=0, column=1, pady=5)

        self.diameter_label = tk.Label(self, text="Enter the diameter of the specimen:")
        self.diameter_entry = tk.Entry(self)
        
        self.width_label = tk.Label(self, text="Enter the width of the specimen:")
        self.width_entry = tk.Entry(self)
        
        self.height_label = tk.Label(self, text="Enter the height of the specimen:")
        self.height_entry = tk.Entry(self)

        self.initial_length_label = tk.Label(self, text="Enter the initial length of the specimen:")
        self.initial_length_label.grid(row=3, column=0, pady=5, sticky="w")
        
        self.initial_length_entry = tk.Entry(self)
        self.initial_length_entry.grid(row=3, column=1, pady=5)

        self.submit_button = tk.Button(self, text="Submit", command=self.submit_specimen_details, width=20)
        self.submit_button.grid(row=4, column=0, columnspan=2, padx=5,pady=15)

    def update_geometry_inputs(self, *args):
        shape = self.shape_var.get()
        if shape == "rounded":
            self.width_label.grid_remove()
            self.width_entry.grid_remove()
            self.height_label.grid_remove()
            self.height_entry.grid_remove()
            self.diameter_label.grid(row=1, column=0, pady=5, sticky="w")
            self.diameter_entry.grid(row=1, column=1, pady=5)
        else:
            self.diameter_label.grid_remove()
            self.diameter_entry.grid_remove()
            self.width_label.grid(row=1, column=0, pady=5, sticky="w")
            self.width_entry.grid(row=1, column=1, pady=5)
            self.height_label.grid(row=2, column=0, pady=5, sticky="w")
            self.height_entry.grid(row=2, column=1, pady=5)

    def submit_specimen_details(self):
        shape = self.shape_var.get()
        if shape == 'rounded':
            diameter = float(self.diameter_entry.get())
            width, height = None, None
        else:
            width = float(self.width_entry.get())
            height = float(self.height_entry.get())
            diameter = None
        
        initial_length = float(self.initial_length_entry.get())
        self.on_submit(shape, diameter, width, height, initial_length)
