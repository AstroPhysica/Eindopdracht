import pyvisa
import numpy as np


#class for the basic operations of the Arduino device
class ArduinoVISADevice:
    """ Class with wich the Arduino device is operated in python
    """    
    def __init__(self,port):
        """Function sets initial conditions for the class

        Args:
            port (string): port is the name of the port
        """        
        rm = pyvisa.ResourceManager("@py")
        self.device=rm.open_resource(port, read_termination="\r\n", write_termination="\n")
        self.value = np.array([0])
        self.digital = np.array([0])
        self.input_value = np.array([0])


    def get_identification(self):
        """"Function requests the identification of the device in use in the port as set in the initial condition

        """        
        self.id = self.device.query("*IDN?")
        return self.id


    def set_output(self, value):
        """Function sets the output value of the device

        Args:
            value (integer): output value

        Returns:
            array: returns value in array
        """        
        self.digital = np.array([value])
        return self.digital


    def get_output_value(self):
        """Function requests the set output value

        Returns:
            _array: array of the set output value
        """        
        self.value = [self.device.query(f"OUT:CH0 {self.digital[0]}")]
        return self.value


    def get_input_value(self, channel):
        """Function requests input value of the requested channel

        Args:
            channel (integer): channel ID

        Returns:
            integer: input value of the requested channel
        """        
        self.input = self.device.query(f"MEAS:CH{channel}?")
        return self.input


    def get_input_voltage(self, channel):
        """Function requests the input voltage of the requested channel by conferting the measurment of the channel, which is based on the set output value, to voltge

        Args:
            channel (integer): channel ID

        Returns:
            integer: channel voltage
        """        
        self.value = [self.device.query(f"OUT:CH0 {self.digital[0]}")]
        self.input_voltage = (int(self.device.query(f"MEAS:CH{channel}?")))*3.3/1023
        return self.input_voltage

    def output_zero(self):
        """Function sets the output to 0 to shut off the LED light

        Returns:
            integer: returns output value which should be 0
        """        
        output = self.device.query(f"OUT:CH0 {0}")
        return output


def list_devices():
    rm = pyvisa.ResourceManager("@py")
    return rm.list_resources()

