import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class GraphPlotter:
    def __init__(self, root):
        self.root = root
        self.canvas = None
        
        self.graph_area = None
        
        self.force_data = []
        self.displacement_data = []
        self.stress_data = []
        self.strain_data = []
        
        self.current_plot = tk.IntVar(value=0)  # 0 for stress-strain, 1 for force-displacement, 2 for results

        self.current_plot.trace_add('write', self.update_plot)

    def plot_graph(self, graph_area, force_data, displacement_data, stress_data, strain_data):
        self.graph_area = graph_area
        self.force_data = force_data
        self.displacement_data = displacement_data
        self.stress_data = stress_data
        self.strain_data = strain_data
        
        self.update_plot()

    def update_plot(self, *args):
        plot_type = self.current_plot.get()
        
        # Clear previous plot if canvas exists
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        
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
        
    def get_young_modulus(self, strain, stress):
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
        youngs_modulus = self.get_young_modulus(strain, stress)
        
        # 0.2% offset yield strength
        offset_strain = 0.002
        offset_stress = youngs_modulus * (np.array(strain) - offset_strain)
        yield_idx = np.argmin(np.abs(stress - offset_stress))
        
        # Refine yield point
        for i in range(yield_idx - 100, yield_idx + 100):
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
            "Ultimate Tensile Strength (MPa)": ultimate_stress,
            "Strain at UTS": strain_at_uts,
            "Fracture Stress (MPa)": fracture_stress,
            "Fracture Strain": fracture_strain,
            "Young's Modulus (MPa)": youngs_modulus
        }

    def display_results(self, ax):
        results = self.calculate_properties(self.strain_data, self.stress_data)
        text_str = "\n".join([f"{key}: {value:.4f}" for key, value in results.items()])
        ax.text(0.05, 0.95, text_str, transform=ax.transAxes, fontsize=16, verticalalignment='top', horizontalalignment='left')
        ax.axis('off')
        ax.grid(False)
