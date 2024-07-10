import tkinter as tk
from DataCollector import DataCollector
from GraphPlotter import GraphPlotter

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Collection and Graphing")
        
        # Create DataCollector instance
        self.data_collector = DataCollector("COM4")
        self.force_data = []
        self.displacement_data = []
        
        # Create GraphPlotter to plot the graph
        self.graph_plotter = GraphPlotter(self.root)

        # Configure grid layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, minsize=200,weight=0)

        # Create main frames
        self.create_graph_area()
        self.create_button_area()
        self.create_data_area()

    def create_graph_area(self):
        self.graph1_area = tk.Frame(self.root, bg="white", width=600, height=400)
        self.graph1_area.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

    def create_data_area(self):
        self.data_area = tk.Frame(self.root, bg="black", width=200, height=400)
        self.data_area.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky='nsew')
        
        self.data_label = tk.Label(self.data_area, text="Force  Displacement", bg="black", fg="white", font=("Arial", 16))
        self.data_label.pack(anchor="nw")
        
        self.data_text = tk.Text(self.data_area, bg="black", fg="white", font=("Arial", 12), width=30)
        self.data_text.pack(fill=tk.BOTH)

    def create_button_area(self):
        self.button_area = tk.Frame(self.root, width=600, height=100)
        self.button_area.grid(row=1, column=0, padx=10, pady=10)
        
        self.start_button = tk.Button(self.button_area, text="Start", command=self.start_data_collection, width=15)
        self.start_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.stop_button = tk.Button(self.button_area, text="Stop", command=self.stop_data_collection, width=15)
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.show_graph_button = tk.Button(self.button_area, text="Plot", command=self.show_graph, width=15)
        self.show_graph_button.grid(row=0, column=2, padx=10, pady=10)
    
    def start_data_collection(self):
        self.force_data = []
        self.displacement_data = []
        self.data_collector.start_collecting(self.data_callback)

    def stop_data_collection(self):
        self.data_collector.stop_collecting()

    def data_callback(self, force, displacement):
        self.force_data.append(force)
        self.displacement_data.append(displacement)
        self.data_text.insert("1.0", f"{force:.2f}\t{displacement:.2f}\n")

    def show_graph(self):
        self.graph_plotter.plot_graph(self.graph1_area, self.force_data, self.displacement_data)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
