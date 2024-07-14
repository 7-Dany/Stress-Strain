import tkinter as tk
from GraphPlotter import GraphPlotter

class MainFrame(tk.Frame):
    """
    MainFrame class represents the main GUI frame for a material testing simulation application.

    Args:
        parent (tk.Tk or tk.Frame): Parent tkinter widget.
        data (dict): Initial data for the simulation.
        data_collector (object): Object responsible for collecting data during the simulation.
        testing_simulator (object): Object handling the simulation logic.
        show_input_frame (function): Function to switch to the input frame.

    Attributes:
        data_collector (object): Instance managing data collection.
        testing_simulator (object): Instance managing simulation.
        show_input_frame (function): Function to switch to input frame.
        graph_plotter (GraphPlotter): Instance to handle plotting graphs.
        initial_data (dict): Initial data for the simulation.
        force_data (list): List to store force data during the simulation.
        displacement_data (list): List to store displacement data during the simulation.
        stress_data (list): List to store stress data during the simulation.
        strain_data (list): List to store strain data during the simulation.
        graph1_area (tk.Frame): Frame for displaying graphs.
        slider_frame (tk.Frame): Frame containing navigation buttons for graphs.
        prev_button (tk.Button): Button to navigate to previous graph.
        next_button (tk.Button): Button to navigate to next graph.
        graph_type (tk.StringVar): Variable to hold the current graph type label.
        graph_label (tk.Label): Label displaying the current graph type.
        f_d_area (tk.Frame): Frame for displaying force-displacement data.
        f_d_label (tk.Label): Label for force-displacement area.
        f_d_text (tk.Text): Text area to display force-displacement data.
        stress_area (tk.Frame): Frame for displaying stress-strain data.
        stress_label (tk.Label): Label for stress-strain area.
        stress_text (tk.Text): Text area to display stress-strain data.
        button_area (tk.Frame): Frame containing various control buttons.
        start_button, stop_button, new_test_button, show_graph_button,
        simulate_button, save_results_button (tk.Button): Buttons for starting/stopping,
        new test, plotting, simulating, and saving results respectively.
    """

    def __init__(self, parent, data, data_collector, testing_simulator, show_input_frame):
        super().__init__(parent)
        
        # Initialize instances and data
        self.data_collector = data_collector
        self.testing_simulator = testing_simulator
        self.show_input_frame = show_input_frame
        self.graph_plotter = GraphPlotter(parent)
        
        self.initial_data = data
        self.force_data = []
        self.displacement_data = []
        self.stress_data = []
        self.strain_data = []

        # Create GUI widgets
        self.create_widgets()

    def create_widgets(self):
        """
        Create all GUI widgets: graph area, force-displacement area, button area, and stress-strain area.
        """
        self.create_graph_area()
        self.create_force_displacement_area()
        self.create_button_area()
        self.create_stress_strain_area()

    def create_graph_area(self):
        """
        Create the graph display area including navigation buttons and graph type label.
        """
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
        """
        Switch to the previous graph in the sequence.
        """
        current = self.graph_plotter.current_plot.get()
        if current > 0:
            self.graph_plotter.current_plot.set(current - 1)
            self.graph_plotter.update_plot()
            self.update_graph_label()

    def show_next_graph(self):
        """
        Switch to the next graph in the sequence.
        """
        current = self.graph_plotter.current_plot.get()
        if current < 2:
            self.graph_plotter.current_plot.set(current + 1)
            self.graph_plotter.update_plot()
            self.update_graph_label()

    def update_graph_label(self):
        """
        Update the graph type label based on the current plot index.
        """
        graph_labels = ["Stress vs Strain", "Force vs Displacement", "Results"]
        self.graph_type.set(graph_labels[self.graph_plotter.current_plot.get()])

    def create_force_displacement_area(self):
        """
        Create the area for displaying force-displacement data.
        """
        self.f_d_area = tk.Frame(self, bg="black", width=300, height=400)
        self.f_d_area.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky='nsew')
        
        self.f_d_label = tk.Label(self.f_d_area, text="Force  Displacement", bg="black", fg="white", font=("Arial", 16))
        self.f_d_label.pack(anchor="nw")
        
        self.f_d_text = tk.Text(self.f_d_area, bg="black", fg="white", font=("Arial", 12), width=25)
        self.f_d_text.pack(fill=tk.BOTH)
        
    def create_stress_strain_area(self):
        """
        Create the area for displaying stress-strain data.
        """
        self.stress_area = tk.Frame(self, bg="black", width=300, height=400)
        self.stress_area.grid(row=0, column=2, rowspan=3, padx=10, pady=10, sticky='nsew')
        
        self.stress_label = tk.Label(self.stress_area, text="Stress  Strain", bg="black", fg="white", font=("Arial", 16))
        self.stress_label.pack(anchor="nw")
        
        self.stress_text = tk.Text(self.stress_area, bg="black", fg="white", font=("Arial", 12), width=25)
        self.stress_text.pack(fill=tk.BOTH)

    def create_button_area(self):
        """
        Create the area for control buttons.
        """
        self.button_area = tk.Frame(self, width=700, height=100)
        self.button_area.grid(row=2, column=0, padx=10, pady=10)
        
        self.start_button = tk.Button(self.button_area, text="Start", command=self.start_data_collection, width=15)
        self.start_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.stop_button = tk.Button(self.button_area, text="Stop", command=self.stop_data_collection, width=15)
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.new_test_button = tk.Button(self.button_area, text="New", command=self.start_new_test, width=15)
        self.new_test_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")
        
        self.show_graph_button = tk.Button(self.button_area, text="Plot", command=self.show_graph, width=15)
        self.show_graph_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.simulate_button = tk.Button(self.button_area, text="Simulate", command=self.start_simulation, width=15)
        self.simulate_button.grid(row=1, column=1,padx=10, pady=10)
        
        self.save_results_button = tk.Button(self.button_area, text="Save", command=self.save_results,width=15)
        self.save_results_button.grid(row=1, column=2, padx=10, pady=10, sticky="e")
    
    def data_callback(self, force, displacement):
        """
        Callback function to receive and process data from data collector.

        Args:
            force (float): Current force value.
            displacement (float): Current displacement value.
        """
        area = self.initial_data["area"]
        initial_length = self.initial_data["initial_length"]
        
        stress = force / area
        
        if len(self.displacement_data) > 0:
            strain = (displacement - self.displacement_data[0]) / initial_length
        else:
            strain = 0

        self.force_data.append(force)
        self.displacement_data.append(displacement)
        
        self.stress_data.append(stress)
        self.strain_data.append(strain)
        
        self.f_d_text.insert("1.0", f"{force:.2f}\t {displacement:.3f}\n")
        self.stress_text.insert("1.0", f"{stress:.2f}\t{strain:.5f}\n")
        
        
    def start_data_collection(self):
        """
        Start data collection process.
        """
        self.create_widgets()  # Reset widgets
        self.force_data = []
        self.displacement_data = []
        self.stress_data = []
        self.strain_data = []
        self.data_collector.start_collecting(self.data_callback)
        

    def stop_data_collection(self):
        """
        Stop data collection process.
        """
        self.data_collector.stop_collecting()

    def start_new_test(self):
        """
        Start a new test with fresh initial data.
        """
        self.initial_data = {}
        self.force_data = []
        self.displacement_data = []
        self.stress_data = []
        self.strain_data = []
        self.destroy()  # Destroy current frame
        self.show_input_frame()  # Show input frame
        
    def show_graph(self):
        """
        Plot the current data on the graph.
        """
        self.graph_plotter.plot_graph(self.graph1_area, self.force_data, self.displacement_data, self.stress_data, self.strain_data)
        
    def start_simulation(self):
        """
        Start simulation with the current initial data.
        """
        self.testing_simulator.start_simulation(self.initial_data["area"], self.initial_data["initial_length"])

    def save_results(self):
        """
        Save results from the current simulation or test.
        """
        self.graph_plotter.save_results()
