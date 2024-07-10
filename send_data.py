import time
import serial
import numpy as np

# Configure the serial port (adjust the port name as needed)
ser = serial.Serial('COM2', 9600)

# Convert the signal received from pressure sensor to force
def signal_to_force(value):
    max_voltage = 10
    max_pressure = 10  # in bar (assumed max pressure for simulation)
    voltage = value * (max_voltage / 1023)
    pressure = (voltage / max_voltage) * max_pressure
    piston_area = 0.016  # in m^2 (piston area)
    pressure_pascal = pressure * 1e5  # converting bar to Pascals (1 bar = 1e5 Pascals)
    force = piston_area * pressure_pascal  # Force in Newtons
    return force

# Convert signal from displacement sensor to displacement in mm
def signal_to_displacement(value):
    pot_length = 200  # in mm
    displacement = (value / 1023) * pot_length
    return displacement

# Function to simulate pressure and displacement signals
def simulate_signals(num_points=100, max_pressure_bar=250, max_displacement_mm=200):
    # Simulate pressure signals in the range of 0 to 1023
    pressure_signals = np.linspace(0, 200, num_points)
    # Simulate displacement signals in the range of 0 to 1023
    displacement_signals = np.linspace(0, 400, num_points)
    return pressure_signals, displacement_signals

# Function to simulate the entire process and send results over serial
def simulate_and_send(num_points=100):
    time.sleep(10)
    pressure_signals, displacement_signals = simulate_signals(num_points)
    forces = [signal_to_force(p) for p in pressure_signals]
    displacements = [signal_to_displacement(d) for d in displacement_signals]
    
    # `serial_send` is a function that sends data over serial
    for force, displacement in zip(forces, displacements):
        serial_send(force, displacement)  # You need to implement `serial_send` according to your serial communication setup

# Example of serial send function
def serial_send(force, displacement):
    data = f"{force},{displacement}\n"
    ser.write(data.encode())

    # Print the data to the console for debugging
    print(f"Sent: {data.strip()}")

    # Wait for a short period
    time.sleep(0.1)

# Simulate and send data
simulate_and_send()
