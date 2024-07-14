import tkinter as tk
from tkinter import messagebox

class MaterialInputDialog:
    """
    MaterialInputDialog class provides a dialog window for entering material properties.

    Args:
        parent (tk.Tk or tk.Frame): Parent tkinter widget.

    Attributes:
        parent (tk.Tk or tk.Frame): Parent tkinter widget.
        result (dict): Dictionary to store entered material properties.

    Methods:
        show(): Displays the dialog window and waits for user input.
        on_cancel(): Handles cancel button click event.
        on_ok(): Handles confirm button click event, validates inputs, and stores results.
    """

    def __init__(self, parent):
        """
        Initializes the MaterialInputDialog instance.

        Args:
            parent (tk.Tk or tk.Frame): Parent tkinter widget.
        """
        self.parent = parent
        self.result = {}

    def show(self):
        """
        Displays the dialog window for entering material properties.

        Returns:
            dict: Dictionary containing entered material properties.
        """
        self.result = {}
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Material Input")
        self.dialog.geometry("450x200")

        # Create labels and entry fields
        tk.Label(self.dialog, text="Enter yield stress (MPa):", anchor='w').grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.yield_stress_entry = tk.Entry(self.dialog, width=30)
        self.yield_stress_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.dialog, text="Enter ultimate stress (MPa):", anchor='w').grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.ultimate_stress_entry = tk.Entry(self.dialog, width=30)
        self.ultimate_stress_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.dialog, text="Enter modulus of elasticity (GPa):", anchor='w').grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.modulus_of_elasticity_entry = tk.Entry(self.dialog, width=30)
        self.modulus_of_elasticity_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.dialog, text="Enter fracture strain:", anchor='w').grid(row=3, column=0, padx=10, pady=5, sticky='w')
        self.fracture_stress_entry = tk.Entry(self.dialog, width=30)
        self.fracture_stress_entry.grid(row=3, column=1, padx=10, pady=5)

        # Confirm button
        ok_button = tk.Button(self.dialog, text="Confirm", command=self.on_ok, width=10)
        ok_button.grid(row=4, column=1, pady=15, padx=10, sticky='e')

        # Cancel button
        cancel_button = tk.Button(self.dialog, text="Cancel", command=self.on_cancel, width=10)
        cancel_button.grid(row=4, column=0, pady=15, padx=10, sticky='w')

        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        self.parent.wait_window(self.dialog)

        return self.result
    
    def on_cancel(self):
        """
        Handles the cancel button click event by clearing the result dictionary and destroying the dialog window.
        """
        self.result = {}
        self.dialog.destroy()

    def on_ok(self):
        """
        Handles the confirm button click event by validating inputs, storing the entered values in the result dictionary,
        and destroying the dialog window. Displays an error message if inputs are not valid numbers.
        """
        try:
            self.result['yield_stress'] = float(self.yield_stress_entry.get())
            self.result['ultimate_stress'] = float(self.ultimate_stress_entry.get())
            self.result['modulus_of_elasticity'] = float(self.modulus_of_elasticity_entry.get())
            self.result['fracture_stress'] = float(self.fracture_stress_entry.get())
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Input error", "Please enter valid numbers")
