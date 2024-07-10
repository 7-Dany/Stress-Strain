def create_data_area(self):
    self.data_area = tk.Frame(self.root, bg="black", width=200, height=400)
    self.data_area.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky='nsew')
    
    font = ("Arial", 16)
    self.data_label = tk.Label(self.data_area, text="Force  Displacement", bg="black", fg="white", font=font)
    self.data_label.pack(anchor="nw")
    
    self.data_text = tk.Text(self.data_area, bg="black", fg="white", font=("Arial", 12), width=30)
    self.data_text.pack(fill=tk.BOTH)
