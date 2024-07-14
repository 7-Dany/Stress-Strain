# Stress-Strain Curve Generator

This program receives force and displacement data from an Arduino and converts it into a stress-strain curve. It also provides simulation capabilities and result visualization.
![Programm Image](./program.png)

## Features

- Specimen detail input (shape, dimensions, initial length)
- Real-time data acquisition from Arduino via serial port
- Stress-strain curve generation
- Force-displacement curve plotting
- Material property calculation (yield stress, ultimate stress, Young's modulus, strain)
- Stress-strain curve simulation based on user-input material properties
- Graph and result saving functionality

## Requirements

- Python 3.10
- pip (Python package installer)

## Installation

1. Clone this repository or download the source code.
```
git clone https://github.com/7-Dany/Stress-Strain.git
```

2. Navigate to the project directory.
```
cd Stress-Strain
```

3. Install the required libraries using pip:

```
pip install -r requirements.txt
```

## Usage

1. Set up a virtual serial port:
   - We recommend using Virtual Serial Port Driver or com0com to create a virtual COM port pair.
   - Create a pair of virtual COM ports (e.g., COM2 and COM3).

Adjust the serial port settings in app.py:
Locate line 93 in app.py and modify it according to your setup:
```python
# Replace "COM4" with the appropriate serial port for the Arduino, or the receiver serial port.
# Replace "COM2" with the virtual serial port that will send the data.
app = App(root, "COM4", "COM2")
```

2. Run the program using Python:
```terminal
python app.py
```

Important Note: For the simulation to work properly, you must use a virtual serial port. The program uses two COM ports:

One for the Arduino or the actual receiver (e.g., COM4 in the example above)
One for the virtual serial port that will send simulated data (e.g., COM2 in the example above)

Make sure to adjust these port numbers according to your specific setup.

## How it works

The program prompts the user for specimen details:

- Shape (rectangular or round)
- Dimensions (width and height for rectangular, diameter for round)
- Initial length


It then begins receiving force and displacement data from the Arduino through the serial port.
The program converts the force and displacement data into stress and strain values.
Stress-strain and force-displacement curves are plotted in real-time.
After the test, the program calculates and displays:

- Yield stress
- Ultimate stress
- Young's modulus
- Strain at each significant point


Users can simulate stress-strain curves by clicking the "Simulate" button and entering material properties.
Graphs and results can be saved as images on the local machine.

## Libraries Used

- pyserial: For serial communication with Arduino
- matplotlib: For plotting graphs
- numpy: For numerical computations
- tkinter: For the graphical user interface