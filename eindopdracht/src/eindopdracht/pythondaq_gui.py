import sys
import time
from PySide6.QtWidgets import QApplication
import pyqtgraph as pg
from PySide6.QtCore import Slot
from pythondaq.arduino_device import ArduinoVISADevice, list_devices
from pythondaq.diode_experiment import DiodeExperiment
import numpy as np
from pythondaq.design_coen import Ui_MainWindow
from PySide6 import QtWidgets, QtCore
import pandas



# PyQtGraph global options
pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")


# uiclass, baseclass = pg.Qt.loadUiType("src\pythondaq\mainwindow.ui")

class UserInterface(QtWidgets.QMainWindow):
    """Class which creates the GUI for the U,I graph
    Start & End values can be set
    Amount of runs can be set
    Data can be plot
    Data can be saved
    """    
    def __init__(self):
        """Initial setting of the GUI
        """        

        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #list of devices
        self.ui.devices.addItem('No device selected')
        self.ui.devices.addItem('arduino' )

        self.port = None
        #set range for spinboxes
        self.ui.start_value_doubleSpinBox.setMinimum(0)
        self.ui.start_value_doubleSpinBox.setMaximum(3.3)
        self.ui.stop_value_doubleSpinBox.setMinimum(0)
        self.ui.stop_value_doubleSpinBox.setMaximum(3.3)
        self.ui.runs_spinbox.setMinimum(1)
 
        #button plots the graph
        self.ui.plot_graph_button.clicked.connect(self.start_scan)
        #button saves the data
        self.ui.save_button.clicked.connect(self.save_data) 
        #plot_timer
        self.plot_timer = QtCore.QTimer()
        self.plot_timer.timeout.connect(self.graph)
        self.plot_timer.start(100)


        self.ui.devices.currentIndexChanged.connect(self.device)


    @Slot()
    def device(self):
        """Function in which the selected device gets opened
        If no device is selected error message will display
        """        
        if self.ui.devices.currentIndex() == 1:
            self.port = 'ASRL4::INSTR'
            self.DE = DiodeExperiment(self.port)
        else:
            self.port = None

        return

    @Slot()
    def start_scan(self):
        """Starts a scan if a port is selected and the graph plot button is clicked
        scan is based on start, end and run values
        scan also returns error
        """        
        start = int(self.ui.start_value_doubleSpinBox.value())
        end = int(self.ui.stop_value_doubleSpinBox.value())
        runs = self.ui.runs_spinbox.value()
        if self.port == None:
            print("No device selected")
        else:
            self.DE.scan_start(start, end, runs)

    @Slot()
    def graph(self):
        """Graphs the function if the plot graph button is clicked
        Vertical axis is the current in Ampére
        Horizontal axis is the voltage in Volt
        Error bars are plotted for the current
        """        
        self.ui.graphicsView.clear()
        self.ui.graphicsView.plot(self.DE.U_gem, self.DE.I_gem, symbol="o", symbolSize=5, pen=None)
        error_bars = pg.ErrorBarItem(x=np.array(self.DE.U_gem), y=np.array(self.DE.I_gem), height = np.array(self.DE.error))
        self.ui.graphicsView.addItem(error_bars)
        self.ui.graphicsView.setLabel('left', text='Current in Ampére')
        self.ui.graphicsView.setLabel('bottom', text='Voltage in Volt')
        self.show()

    @Slot()
    def save_data(self, port):
        """Runs the graph function and saves the data to a csv file which can be custom named

        Args:
            port (string): name of the port in which the device is connected
        """        
        if self.ui.devices.currentIndex() == 1:
            port = 'ASRL4::INSTR'

        start = int(self.ui.start_value_doubleSpinBox.value())
        end = int(self.ui.stop_value_doubleSpinBox.value())
        runs = self.ui.runs_spinbox.value()
        DE = DiodeExperiment(port)

        diode = DE.measurement(start, end, runs)
        current = diode[1]
        voltage = diode[0]
        error = diode[2]

        filename, _ = QtWidgets.QFileDialog.getSaveFileName(filter="CSV files (*.csv)")
        pairs = {'Voltage': voltage, 'Current': current}

        df = pandas.DataFrame.from_dict(pairs)

        df.to_csv(filename)

        file = open("data.csv")

def main():
    """Runs the class if the file is run
    """    
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()