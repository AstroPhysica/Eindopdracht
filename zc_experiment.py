from arduino_device import ArduinoVISADevice, list_devices
import numpy as np
import matplotlib.pyplot as plt
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
    
    def measure(self, U_0, runs):
        
        U_total = []
        I_total = []
        R_total = []
        P_total = []
        adc_value = int(U_0*1024/3.3)


        self.device.set_output(value=adc_value)
        for z in range(0, runs):
            U = self.device.get_input_voltage(channel=1)*3
            U_total.append(U)
            I = self.device.get_input_voltage(channel=2)/4.7
            I_total.append(I)
           # R = U/I
           # R_total.append(R)
            P = U*I
            P_total.append(P)

        return I_total, U_total, P_total

    def scan(self, start, stop, runs):
        start_value = int(start*1024/3.3)
        stop_value = int(stop*1024/3.3)

        for x in np.linspace(start_value, stop_value, 1024):
            I_total, U_total, P_total = self.measure(start_value, runs)

            self.I_gem.append(np.mean(I_total))
            self.I_error.append(float(np.std(I_total))/np.sqrt(runs))
            self.U_gem.append(np.mean(U_total))
            self.U_error.append(float(np.std(U_total)/np.sqrt(runs)))
            self.P_gem.append(np.mean(P_total))

        return self.U_gem, self.I_gem, self.I_error, self.P_gem

zc = zonnecel_experiment(port = 'ASRL4::INSTR')

I, U, P = zc.measure(0, 2)
print(I, U)

voltage, current, I_error, power = zc.scan(0, 3.3, 5)
print(voltage)
plt.plot(voltage, current, 'o')
plt.xlabel('voltage')
plt.ylabel('current')
plt.show()