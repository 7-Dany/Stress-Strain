import tkinter as tk
from GraphPlotter import GraphPlotter

class MainFrame(tk.Frame):
    def __init__(self, parent, data, data_collector, testing_simulator):
        super().__init__(parent)
        
        self.data_collector = data_collector
        self.testing_simulator = testing_simulator
        self.graph_plotter = GraphPlotter(parent)
        
        self.inital_data = data
        self.force_data = []
        self.displacement_data = []
        self.stress_data = []
        self.strain_data = []

        self.create_widgets()

    def create_widgets(self):
        self.create_graph_area()
        self.create_force_displacement_area()
        self.create_button_area()
        self.create_stress_strain_area()

    def create_graph_area(self):
        self.graph1_area = tk.Frame(self, bg="white", width=700, height=400)
        self.graph1_area.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.slider_frame = tk.Frame(self, bg="white")
        self.slider_frame.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        self.prev_button = tk.Button(self.slider_frame, text="Previous", command=self.show_prev_graph)
        self.prev_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.next_button = tk.Button(self.slider_frame, text="Next", command=self.show_next_graph)
        self.next_button.pack(side=tk.RIGHT, padx=2, pady=2)

        self.graph_type = tk.StringVar(value="Stress vs Strain")
        self.graph_label = tk.Label(self.slider_frame, textvariable=self.graph_type, bg="white")
        self.graph_label.pack(side=tk.LEFT, expand=True)

    def show_prev_graph(self):
        current = self.graph_plotter.current_plot.get()
        if current > 0:
            self.graph_plotter.current_plot.set(current - 1)
            self.graph_plotter.update_plot()
            self.update_graph_label()

    def show_next_graph(self):
        current = self.graph_plotter.current_plot.get()
        if current < 1:
            self.graph_plotter.current_plot.set(current + 1)
            self.graph_plotter.update_plot()
            self.update_graph_label()

    def update_graph_label(self):
        graph_labels = ["Stress vs Strain", "Force vs Displacement"]
        self.graph_type.set(graph_labels[self.graph_plotter.current_plot.get()])

    def create_force_displacement_area(self):
        self.f_d_area = tk.Frame(self, bg="black", width=300, height=400)
        self.f_d_area.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky='nsew')
        
        self.f_d_label = tk.Label(self.f_d_area, text="Force  Displacement", bg="black", fg="white", font=("Arial", 16))
        self.f_d_label.pack(anchor="nw")
        
        self.f_d_text = tk.Text(self.f_d_area, bg="black", fg="white", font=("Arial", 12), width=25)
        self.f_d_text.pack(fill=tk.BOTH)
        
    def create_stress_strain_area(self):
        self.stress_area = tk.Frame(self, bg="black", width=300, height=400)
        self.stress_area.grid(row=0, column=2, rowspan=3, padx=10, pady=10, sticky='nsew')
        
        self.stress_label = tk.Label(self.stress_area, text="Stress  Strain", bg="black", fg="white", font=("Arial", 16))
        self.stress_label.pack(anchor="nw")
        
        self.stress_text = tk.Text(self.stress_area, bg="black", fg="white", font=("Arial", 12), width=25)
        self.stress_text.pack(fill=tk.BOTH)

    def create_button_area(self):
        self.button_area = tk.Frame(self, width=700, height=100)
        self.button_area.grid(row=2, column=0, padx=10, pady=10)
        
        self.start_button = tk.Button(self.button_area, text="Start", command=self.start_data_collection, width=15)
        self.start_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.stop_button = tk.Button(self.button_area, text="Stop", command=self.stop_data_collection, width=15)
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.show_graph_button = tk.Button(self.button_area, text="Plot", command=self.show_graph, width=15)
        self.show_graph_button.grid(row=1, column=0, padx=10, pady=10)
        
        self.simulate_button = tk.Button(self.button_area, text="Simulate", command=self.start_simulation, width=15)
        self.simulate_button.grid(row=1, column=1,padx=10, pady=10)
        
    
    def data_callback(self, force, displacement):
        area = self.inital_data["area"]
        initial_length = self.inital_data["initial_length"]
        
        stress = (force / area) / 1e6
        
        if len(self.displacement_data) > 0:
            strain = (displacement - self.displacement_data[0]) / initial_length
        else:
            strain = 0

        self.force_data.append(force)
        self.displacement_data.append(displacement)
        
        self.stress_data.append(stress)
        self.strain_data.append(strain)
        
        self.f_d_text.insert("1.0", f"{force:.2f}\t {displacement:.2f}\n")
        self.stress_text.insert("1.0", f"{stress:.2f}\t{strain:.2f}\n")
        
        
    def start_data_collection(self):
        self.force_data = []
        self.displacement_data = []
        self.stress_data = []
        self.strain_data = []
        self.data_collector.start_collecting(self.data_callback)
        

    def stop_data_collection(self):
        self.data_collector.stop_collecting()


    def show_graph(self):
        self.graph_plotter.plot_graph(self.graph1_area, self.force_data, self.displacement_data, self.stress_data, self.strain_data)
        
    def start_simulation(self):
        self.testing_simulator.start_simulation(self.inital_data["diameter"], self.inital_data["initial_length"])
