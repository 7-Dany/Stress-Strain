import serial
import threading

class DataCollector:
    def __init__(self, port):
        self.port = port
        self.ser = serial.Serial(port, baudrate=9600, timeout=1)
        self.collecting = False
        self.thread = None

    def start_collecting(self, callback):
        self.collecting = True
        self.callback = callback
        self.thread = threading.Thread(target=self.collect_data)
        self.thread.start()

    def stop_collecting(self):
        self.collecting = False
        if self.thread:
            self.thread.join()

    def collect_data(self):
        while self.collecting:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').strip()
                if line:
                    force, displacement = map(float, line.split(','))
                    self.callback(force, displacement)
