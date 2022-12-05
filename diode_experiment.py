from pythondaq.arduino_device import ArduinoVISADevice, list_devices
import numpy as np
import matplotlib.pyplot as plt
import threading

# class for the data to make an U,I plot with errorbars
class DiodeExperiment:
    """Class in which the arduino_device import is used in an attempt to create an accurate list of current, voltage and error data
    """    
    
    def __init__(self, port):
        """Function sets initial conditions for the class

        Args:
            port (string): port is the name of the port
        """           
        self.device = ArduinoVISADevice(port = port)
        self.U_gem = []
        self.I_gem = []
        self.error = []

    def scan(self, start, stop, runs):
        """Function calculates the average current, average voltage and error
        The measurement value is variable for the same input
        Multiple runs are done in the function to increase the accuracy and determine error, hence the avareges in the return
        Function doesn't work with threading, use function measurement when using threading

        Args:
            start (integer): start value for the input
            stop (integer): last value for the input
            runs (integer): number of times the sequence of gathering data of current and voltage occurs
        Returns:
            list: list of voltages
            list: list of currents
            list: list of errors    
        """        

        U_total = []
        I_total = []

# loop for certain number of runs to determain a mean and error
        start_value = int(start*1024/3.3)
        stop_value = int(stop*1024/3.3)

        for x in range(0, runs):

            voltage = []
            current = []
# loop to determine the data for each run

            for x in np.arange(start_value, stop_value):


                self.device.set_output(value=x)
                voltage.append(self.device.get_input_voltage(channel=1)-float(self.device.get_input_value(channel=2))*3.3/1024)
                current.append((float(self.device.get_input_value(channel=2))*3.3/1024)/220)

            U_total.append(voltage)
            I_total.append(current)

            U_gem = np.mean(U_total, axis=0)
            I_gem = np.mean(I_total, axis=0)
            err = np.std(I_total, axis=0)/np.sqrt(runs)
        self.device.output_zero()

# return data
        return U_gem, I_gem, err




    def measurement(self, start, stop, runs):
        """Function calculates the average current, average voltage and error
        The measurement value is variable for the same input
        Multiple runs are done in the function to increase the accuracy and determine error, hence the avareges in the return
        This function is made to work with threading, unlike function scan

        Args:
            start (integer): start value for the input
            stop (integer): last value for the input
            runs (integer): number of times the sequence of gathering data of current and voltage occurs
        Returns:
            _type_: _description_
        """        

        self.U_gem = []
        self.I_gem = []
        self.error = []
        start_value = int(start*1024/3.3)
        stop_value = int(stop*1024/3.3)

        for x in np.arange(start_value, stop_value):
            U_total = []
            I_total = []
            self.device.set_output(value=x)
            for z in range(0, runs):
                U_total.append(self.device.get_input_voltage(channel=1)-int(self.device.get_input_value(channel=2))*3.3/1024)
                I_total.append((int(self.device.get_input_value(channel=2))*3.3/1024)/220)

            self.U_gem.append(np.mean(U_total))
            self.I_gem.append(np.mean(I_total))
            self.error.append(2*float(np.std(I_total))/np.sqrt(runs))

            self.device.output_zero()
        return self.U_gem, self.I_gem, self.error
    
    def scan_start(self, start, stop, runs):
        """Function to start scanning when using threading

        Args:
            start (float): starting value in Voltage
            stop (float): ending value in Voltage
            runs (integer): number of runs to execute
        """        
        self._scan_thread = threading.Thread(
        target=self.measurement, args=(start, stop, runs)
        )
        self._scan_thread.start()