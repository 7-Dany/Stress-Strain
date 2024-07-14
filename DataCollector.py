import serial
import threading

class DataCollector:
    """
    Class for collecting data from a serial port asynchronously.

    Attributes:
        port (str): Serial port address.
        ser (serial.Serial): Serial connection object.
        collecting (bool): Flag indicating if data collection is active.
        thread (threading.Thread): Thread for asynchronous data collection.
        callback (function): Callback function for processing collected data.
    """

    def __init__(self, port):
        """
        Initializes the DataCollector with the serial port address.

        Args:
            port (str): Serial port address (e.g., "COM1", "/dev/ttyUSB0").
        """
        self.port = port
        self.ser = serial.Serial(port, baudrate=9600, timeout=1)
        self.collecting = False
        self.thread = None

    def start_collecting(self, callback):
        """
        Starts collecting data asynchronously from the serial port.

        Args:
            callback (function): Callback function to handle collected data.
        """
        self.collecting = True
        self.callback = callback
        self.thread = threading.Thread(target=self.collect_data)
        self.thread.start()

    def stop_collecting(self):
        """Stops the data collection thread."""
        self.collecting = False
        if self.thread:
            self.thread.join()

    def collect_data(self):
        """Collects data from the serial port as long as collecting flag is True."""
        while self.collecting:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').strip()
                if line:
                    force, displacement = map(float, line.split(','))
                    self.callback(force, displacement)
