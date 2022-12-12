from eindopdracht.arduino_device import ArduinoVISADevice, list_devices
import numpy as np
import threading

class zonnecel_experiment:
    
    def __init__(self, port):

        self.device = ArduinoVISADevice(port = port)
        self.U_gem = []
        self.I_gem = []
        self.R_gem = []
        self.P_gem = []
        self.I_error = []
        self.U_error = []
        self.P_error = []
    
    def measure(self, U_0, runs):
        
        U_total = []
        I_total = []
        R_total = []
        P_total = []
      #  adc_value = int(U_0*1024/3.3)


        self.device.set_output(value=U_0)
        for z in range(0, int(runs)):
            U = self.device.get_input_voltage(channel=1)*3
           # print(self.device.get_input_voltage(channel=1), self.device.get_input_voltage(channel=2), self.device.get_output_value(), U_0)
            U_total.append(U)
            I = self.device.get_input_voltage(channel=2)/4.7
            I_total.append(I)
           # R = U/I
           # R_total.append(R)
            P = U*I
            P_total.append(P)

        return I_total, U_total, P_total

    def scan(self, start, stop, runs):
        start_value = float(start*1023/3.3)
        stop_value = float(stop*1023/3.3)

        for x in np.linspace(start_value, stop_value, 1023):
            I_total, U_total, P_total = self.measure(x, runs)

            self.I_gem.append(np.mean(I_total))
            self.I_error.append(float(np.std(I_total))/np.sqrt(runs))
            self.U_gem.append(np.mean(U_total))
            self.U_error.append(float(np.std(U_total)/np.sqrt(runs)))
            self.P_gem.append(np.mean(P_total))
            self.P_error.append(float(np.std(P_total)/np.sqrt(runs)))
            self.ff = max(self.P_gem)/(max(self.U_gem)*max(self.I_gem))
                
        return self.U_gem, self.I_gem, self.I_error, self.P_gem, self.P_error, self.ff, self.U_error
    
    def scan_start(self, start, stop, runs):
        """Function to start scanning when using threading

        Args:
            start (float): starting value in Voltage
            stop (float): ending value in Voltage
            runs (integer): number of runs to execute
        """        
        self._scan_thread = threading.Thread(
        target=self.scan, args=(start, stop, runs)
        )
        self._scan_thread.start()