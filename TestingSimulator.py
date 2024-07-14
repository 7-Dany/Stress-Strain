import time
import serial
import numpy as np
import threading
from TestingInput import MaterialInputDialog

class MaterialTestingSimulator:
    def __init__(self, root, port='COM2', baudrate=9600):
        self.ser = serial.Serial(port, baudrate)
        self.dialog = MaterialInputDialog(root)
        self.inputs = None

    def signal_to_force(self, value):
        max_voltage = 10
        max_pressure = 250  # in bar (assumed max pressure for simulation)
        voltage = value * (max_voltage / 1023)
        pressure = (voltage / max_voltage) * max_pressure
        piston_area = 0.016  # in m^2 (piston area)
        pressure_pascal = pressure * 1e5  # converting bar to Pascals (1 bar = 1e5 Pascals)
        force = piston_area * pressure_pascal  # Force in Newtons
        return force

    def signal_to_displacement(self, value):
        pot_length = 50  # in mm
        displacement = (value / 1023) * pot_length
        return displacement

    def generate_signals(self, stress, strain, area, initial_length):
        force = stress * area  # stress in MPa and area in mm^2 gives force in N
        displacement = strain * initial_length

        adc_displacement = (displacement / 50) * 1023
        adc_displacement = np.clip(adc_displacement, 0, 1023).astype(int)

        pressure = force / 0.016 / 1e5  # converting N/m^2 to bar
        adc_pressure = (pressure / 250) * 1023
        adc_pressure = np.clip(adc_pressure, 0, 1023).astype(int)

        return adc_pressure.tolist(), adc_displacement.tolist()

    def generate_stress_strain(self, yield_stress, ultimate_stress, youngs_modulus, fracture_strain):
        strain_yield = yield_stress / youngs_modulus
        strain_ultimate = 0.15  # Typical value for metals
        
        strain = np.concatenate([
            np.linspace(0, strain_yield, 5000),
            np.linspace(strain_yield, strain_ultimate, 3000)[1:],
            np.linspace(strain_ultimate, fracture_strain, 2000)[1:]
        ])
        
        stress = np.piecewise(strain, 
            [strain <= strain_yield, (strain > strain_yield) & (strain <= strain_ultimate), strain > strain_ultimate],
            [lambda e: youngs_modulus * e,
            lambda e: yield_stress + (ultimate_stress - yield_stress) * ((e - strain_yield) / (strain_ultimate - strain_yield))**0.5,
            lambda e: ultimate_stress - (ultimate_stress - yield_stress) * ((e - strain_ultimate) / (fracture_strain - strain_ultimate))**0.5]
        )
        
        return stress, strain

    def get_stress_strain(self, yield_stress, ultimate_stress, youngs_modulus, fracture_strain):
        return self.generate_stress_strain(yield_stress, ultimate_stress, youngs_modulus, fracture_strain)

    def serial_send(self, force, displacement):
        data = f"{force},{displacement}\n"
        self.ser.write(data.encode())
        time.sleep(0.02)

    def simulate_and_send(self, yield_stress, ultimate_stress, modulus_of_elasticity, fracture_strain, area, initial_length):
        mod_of_elasticity_in_gpa = modulus_of_elasticity * 10**3
        
        stress, strain = self.get_stress_strain(yield_stress, ultimate_stress, mod_of_elasticity_in_gpa, fracture_strain)
        pressure_signals, displacement_signals = self.generate_signals(stress, strain, area, initial_length)
        
        forces = [self.signal_to_force(p) for p in pressure_signals]
        displacements = [self.signal_to_displacement(d) for d in displacement_signals]
        
        for force, displacement in zip(forces, displacements):
            self.serial_send(force, displacement)
    
    
    def start_simulation(self, area, length):
        self.inputs = self.dialog.show()
        
        if self.inputs:
            simulation_thread = threading.Thread(target=self.simulate_and_send, args=(
                self.inputs['yield_stress'],
                self.inputs['ultimate_stress'],
                self.inputs['modulus_of_elasticity'],
                self.inputs['fracture_stress'],
                area,  # Specimen area value in mm^2
                length  # Specimen initial length value in mm
            ))
            simulation_thread.start()
