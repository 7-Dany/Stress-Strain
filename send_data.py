import time
import serial

# Convert the signal recieved from pressure sensor to arduino into bar
def signal_to_force(value):
    max_voltage = 10
    max_pressure = 250
    voltage = value * (max_voltage/ 1023)
    pressure = (voltage / max_voltage) * max_pressure
    area = 0.016
    force = area * pressure
    return force

# Convert signal from displacement sensor to arduino into mm
def signal_to_displacement(value):
    pot_length = 200
    displacement = (value / 1023) * pot_length
    return displacement

# Configure the serial port (adjust the port name as needed)
ser = serial.Serial('COM2', 9600)

try:
    for i in range(0, 500):
        # Generate dummy data
        pressure = i
        displacement = i

        # Send the data over the serial port
        data = f"{signal_to_force(pressure)},{signal_to_displacement(displacement)}\n"
        ser.write(data.encode())

        # Print the data to the console for debugging
        print(f"Sent: {data.strip()}")

        # Wait for a short period
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stopped by user")
finally:
    ser.close()
