import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphPlotter:
    def __init__(self, root):
        self.root = root
        self.canvas = None
        
        self.graph_area = None
        
        self.force_data = []
        self.displacement_data = []
        self.stress_data = []
        self.strain_data = []
        
        self.current_plot = tk.IntVar(value=0)  # 0 for stress-strain, 1 for force-displacement,

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
        
        fig, ax = plt.subplots(figsize=(10,6))
        
        if plot_type == 1:  # Force vs Displacement
            ax.plot(self.displacement_data, self.force_data, 'b')
            ax.set_xlabel('Displacement (mm)')
            ax.set_ylabel('Force (N)')
            ax.set_title('Force vs Displacement')
        else:  # Stress vs Strain
            ax.plot(self.strain_data, self.stress_data, 'r')
            ax.set_xlabel('Strain')
            ax.set_ylabel('Stress (MPa)')
            ax.set_title('Stress vs Strain')

        if self.graph_area == None: return
        
        # Create new FigureCanvasTkAgg object
        self.canvas = FigureCanvasTkAgg(fig, master=self.graph_area)
        self.canvas.get_tk_widget().configure(width=600, height=400)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
