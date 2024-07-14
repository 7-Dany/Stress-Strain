# Stress-Strain Curve Generator

This program receives force and displacement data from an Arduino and converts it into a stress-strain curve. It also provides simulation capabilities and result visualization.

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

Run the program using Python:
```
python -u app.py
```

## How it works

The program prompts the user for specimen details:

Shape (rectangular or round)
Dimensions (width and height for rectangular, diameter for round)
Initial length


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