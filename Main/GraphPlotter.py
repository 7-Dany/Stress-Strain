import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class GraphPlotter:
    """
    Class for plotting and saving graphs using tkinter and matplotlib.

    Attributes:
        root (tk.Tk): The main tkinter root window.
        canvas (FigureCanvasTkAgg or None): Canvas for displaying matplotlib plots.
        graph_area (tk.Frame or None): Frame area to embed the canvas.
        force_data (list): List of force data points.
        displacement_data (list): List of displacement data points.
        stress_data (list): List of stress data points.
        strain_data (list): List of strain data points.
        current_plot (tk.IntVar): Integer variable to track current plot type.
    """

    def __init__(self, root):
        """
        Initializes the GraphPlotter with the root window and sets up initial variables.

        Args:
            root (tk.Tk): The main tkinter root window.
        """
        self.root = root
        self.canvas = None
        self.graph_area = None
        self.force_data = []
        self.displacement_data = []
        self.stress_data = []
        self.strain_data = []
        self.initial_data = {}
        self.current_plot = tk.IntVar(value=0)  # 0 for stress-strain, 1 for force-displacement, 2 for results
        self.current_plot.trace_add('write', self.update_plot)

    def plot_graph(self, graph_area, force_data, displacement_data, stress_data, strain_data, initial_data):
        """
        Plots a graph based on provided data.

        Args:
            graph_area (tk.Frame): Frame to embed the graph canvas.
            force_data (list): List of force data points.
            displacement_data (list): List of displacement data points.
            stress_data (list): List of stress data points.
            strain_data (list): List of strain data points.
        """
        self.graph_area = graph_area
        self.force_data = force_data
        self.displacement_data = displacement_data
        self.stress_data = stress_data
        self.strain_data = strain_data
        self.initial_data = initial_data
        self.update_plot()

    def update_plot(self, *args):
        """
        Updates the plot based on the selected plot type.
        """
        plot_type = self.current_plot.get()
        
        # Clear previous plot if canvas exists
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if plot_type == 1:  # Force vs Displacement
            ax.plot(self.displacement_data, self.force_data, 'b')
            ax.set_xlabel('Displacement (mm)')
            ax.set_ylabel('Force (N)')
            ax.set_title('Force vs Displacement')
        elif plot_type == 2:  # Results
            self.display_results(ax)
        else:  # Stress vs Strain
            ax.plot(self.strain_data, self.stress_data, 'r')
            ax.set_xlabel('Strain')
            ax.set_ylabel('Stress (MPa)')
            ax.set_title('Stress vs Strain')

        if self.graph_area is None:
            return
        
        # Create new FigureCanvasTkAgg object
        self.canvas = FigureCanvasTkAgg(fig, master=self.graph_area)
        self.canvas.get_tk_widget().configure(width=600, height=400)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        # Close the figure after it's drawn to release memory
        plt.close(fig)

    def save_plot(self, fig, title):
        """
        Saves the current matplotlib figure as a PNG file.

        Args:
            fig (matplotlib.figure.Figure): Matplotlib figure object to save.
            title (str): Title for the save dialog window.
        """
        file_path = filedialog.asksaveasfilename(defaultextension=".png", title=title,
                                                 filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            fig.savefig(file_path)
            plt.close(fig)  # Close the figure after saving

    def save_results(self):
        """
        Saves multiple plots related to force-displacement and stress-strain as PNG files.
        """
        plots = [
            (self.displacement_data, self.force_data, 'Force vs Displacement', 'Displacement (mm)', 'Force (N)'),
            (self.strain_data, self.stress_data, 'Stress vs Strain', 'Strain', 'Stress (MPa)')
        ]
        
        for i, (x_data, y_data, title, x_label, y_label) in enumerate(plots):
            fig, ax = plt.subplots(figsize=(10, 6))
            
            if title == "Stress vs Strain":
                color = 'r'
            else:
                color = 'b'
                
            ax.plot(x_data, y_data, color)
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            ax.set_title(title)
            self.save_plot(fig, f"Save {title} plot as")
        
        # Save results plot
        fig, ax = plt.subplots(figsize=(10, 6))
        self.display_results(ax)
        self.save_plot(fig, "Save Results plot as")

    def get_young_modulus(self, strain, stress):
        """
        Calculates the Young's modulus from strain and stress data.

        Args:
            strain (list): List of strain data points.
            stress (list): List of stress data points.

        Returns:
            float: Calculated Young's modulus.
        """
        first = 0
        second = 0
        
        for i in range(0, len(strain)):
            if strain[i] != 0:
                first = i
                break
        
        for i in range(first, len(strain)):
            if strain[i] != strain[first]:
                second = i
                break
        
        return (stress[second] - stress[first]) / (strain[second] - strain[first]) 
    
    def calculate_properties(self, strain, stress):
        """
        Calculates material properties such as yield stress, ultimate tensile strength, etc.

        Args:
            strain (list): List of strain data points.
            stress (list): List of stress data points.

        Returns:
            dict: Dictionary containing calculated material properties.
        """
        youngs_modulus = self.get_young_modulus(strain, stress)
        
        # 0.2% offset yield strength
        offset_strain = 0.002
        offset_stress = youngs_modulus * (np.array(strain) - offset_strain)
        yield_idx = np.argmin(np.abs(stress - offset_stress))
        
        # Refine yield point
        for i in range(max(0, yield_idx - 100), min(len(stress), yield_idx + 100)):
            if stress[i] >= offset_stress[i]:
                yield_idx = i
                break
        
        yield_stress = stress[yield_idx]
        yield_strain = strain[yield_idx]
        
        # Ultimate tensile strength
        uts_idx = np.argmax(stress)
        ultimate_stress = stress[uts_idx]
        strain_at_uts = strain[uts_idx]
        
        # Fracture point
        fracture_stress = stress[-1]
        fracture_strain = strain[-1]
        
        return {
            "Yield Stress (MPa)": yield_stress,
            "Yield Strain": yield_strain,
            "Force at Yield (N)": yield_stress * self.initial_data["area"],
            "Ultimate Tensile Strength (MPa)": ultimate_stress,
            "Strain at UTS": strain_at_uts,
            "Force at UTS (N)": ultimate_stress * self.initial_data["area"],
            "Fracture Stress (MPa)": fracture_stress,
            "Fracture Strain": fracture_strain,
            "Young's Modulus (MPa)": youngs_modulus,
        }

    def display_results(self, ax):
        """
        Displays calculated material properties on a matplotlib axes.

        Args:
            ax (matplotlib.axes.Axes): Axes object to display the results.
        """
        results = self.calculate_properties(self.strain_data, self.stress_data)
        text_str = "\n".join([f"Specimen {key}: {value}" for key, value in self.initial_data.items()])
        text_str += "\n"
        text_str += "\n".join([f"{key}: {value:.4f}" for key, value in results.items()])
        ax.text(0.05, 0.95, text_str, transform=ax.transAxes, fontsize=16, verticalalignment='top', horizontalalignment='left')
        ax.axis('off')
        ax.grid(False)
