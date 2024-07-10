import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphPlotter:
    def __init__(self, root):
        self.root = root
        self.canvas = None

    def plot_graph(self, graph_area, force_data, displacement_data):
        # Clear previous plot if canvas exists
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            
        fig, ax = plt.subplots()
        ax.plot(displacement_data, force_data, 'bo-')
        ax.set_xlabel('Displacement (mm)')
        ax.set_ylabel('Force (KN)')
        ax.set_title('Force vs Displacement')

        # Create new FigureCanvasTkAgg object
        canvas = FigureCanvasTkAgg(fig, master=graph_area)
        canvas.get_tk_widget().configure(width=600, height=400)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.canvas = canvas

