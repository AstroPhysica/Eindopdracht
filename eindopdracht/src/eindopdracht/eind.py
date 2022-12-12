import sys
import time
from PySide6.QtWidgets import QApplication
import pyqtgraph as pg
from PySide6.QtCore import Slot
from eindopdracht.arduino_device import ArduinoVISADevice, list_devices
import numpy as np
from eindopdracht.zc_experiment import zonnecel_experiment
from eindopdracht.design import Ui_MainWindow
from PySide6 import QtWidgets, QtCore
import pandas


# PyQtGraph global options
pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")

class UserInterface(QtWidgets.QMainWindow):
    """Class in which creates the userinterface which makes use of functions, defined in the class,
    that are run when requested by buttons of the interface.

    """    

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #list of devices
        print(list_devices())
        self.ui.list_devices.addItem('No device selected')
        self.ui.list_devices.addItems(list_devices())

        #set range for spinboxes
        self.ui.start_button.setMinimum(0)
        self.ui.start_button.setMaximum(3.3)
        self.ui.stop_button.setMinimum(0)
        self.ui.stop_button.setMaximum(3.3)
        self.ui.runs_button.setMinimum(1)

        #set default value spinboxes
        self.ui.stop_button.setValue(3.3)
        self.ui.start_button.setValue(0)
        self.ui.runs_button.setValue(1)

        #set step size spinboxes
        self.ui.stop_button.setSingleStep(0.1)
        self.ui.start_button.setSingleStep(0.1)
        #button plots the graph
        self.ui.plot_button.clicked.connect(self.start_scan)
        #button saves the data
        self.ui.save_button.clicked.connect(self.save_data)
        #plot_timer
        self.plot_timer = QtCore.QTimer()
        self.plot_timer.timeout.connect(self.graph)
        self.plot_timer.start(100)

        self.ui.text_line.setReadOnly(True)
        self.ui.Pstring.setReadOnly(True)

        self.ui.list_devices.currentIndexChanged.connect(self.device)


    @Slot()
    def device(self):
        """Function in which the port/device is selected
        """        
        self.port = self.ui.list_devices.currentText()
        print(self.port)
        self.zc = zonnecel_experiment(self.port)
    
    @Slot()
    def start_scan(self):
        """Function in which the scan starts running when plot_button is clicked
        """        
        self.ui.IU_graph.clear()
        self.ui.PU_graph.clear()
        self.ui.text_line.clear()
        start = int(self.ui.start_button.value())
        end = int(self.ui.stop_button.value())
        runs = self.ui.runs_button.value()
        if self.port == None:
            print("No device selected")
        else:
            self.zc.scan_start(start, end, runs)

    @Slot()
    def graph(self):
        """Function in which the graphs are made and the ff value and P-max value are shown. One is a graph of I_gem and U_gem, the other is a graph of P_gem and U_gem.
        For each graph are both the horizontal and vertical errors plotted.
        When the last point of data has been plotted the ff value and p-max value are shown, completing the process
        """        
        self.ui.IU_graph.plot(self.zc.U_gem, self.zc.I_gem, symbol="o", symbolSize=5, pen=None)
        error_bars = pg.ErrorBarItem(x=np.array(self.zc.U_gem), y=np.array(self.zc.I_gem), height = 2*np.array(self.zc.I_error), width= 2*np.array(self.zc.U_error))
        self.ui.IU_graph.addItem(error_bars)
        self.ui.IU_graph.setLabel('left', text='Current in Ampére')
        self.ui.IU_graph.setLabel('bottom', text='Voltage in Volt')
        
        self.ui.PU_graph.plot(self.zc.U_gem, self.zc.P_gem, symbol="o", symbolSize=5, pen=None)
        errors = pg.ErrorBarItem(x=np.array(self.zc.U_gem), y=np.array(self.zc.P_gem), height = 2*np.array(self.zc.P_error), width= 2*np.array(self.zc.U_error))
        self.ui.PU_graph.addItem(errors)
        self.ui.PU_graph.setLabel('left', text='Power in Watt')
        self.ui.PU_graph.setLabel('bottom', text='Voltage in Volt')     
        if len(self.zc.P_gem) == 1023:
            #ff value
            self.ui.text_line.clear()
            self.ui.text_line.setText(f'{round(self.zc.ff, 2)}')
            #power value
            self.ui.Pstring.clear()
            self.ui.Pstring.setText(f'{round(max(self.zc.P_gem), 2)} Watt')


    @Slot()
    def save_data(self):
        """Function in which the acquired data is saved to a self named .csv file.
        The csv file stores the Voltage, Voltage-error, Current, Current-error, Power, Power-error, Resistance, Fill Factor
        """        

        current = all(1*10**-9 if i==0 else i for i in self.zc.I_gem)


        filename, _ = QtWidgets.QFileDialog.getSaveFileName(filter="CSV files (*.csv)")
        pairs = {'Voltage': self.zc.U_gem, 'Voltage-error':self.zc.U_error, 'Current': self.zc.I_gem, 'Current-error': self.zc.I_error, 'Power': self.zc.P_gem, 'Power-error':self.zc.P_error, 'Resistance':np.array(self.zc.U_gem)/current, 'Fill Factor':self.zc.ff}

        df = pandas.DataFrame.from_dict(pairs)

        df.to_csv(filename)

#        file = open("data.csv")

def main():
    """Runs the class if the file is run.
    File can be run on command run_eind.
    """    
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
