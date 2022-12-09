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

        #button plots the graph
        self.ui.plot_button.clicked.connect(self.start_scan)
        #button saves the data
        self.ui.save_button.clicked.connect(self.save_data)
        #plot_timer
        self.plot_timer = QtCore.QTimer()
        self.plot_timer.timeout.connect(self.graph)
        self.plot_timer.start(100)

        self.ui.list_devices.currentIndexChanged.connect(self.device)

        #print ff value
        self.ui.text_line.setReadOnly(True)
        self.ui.ff_button.clicked.connect(self.ff)

    @Slot()
    def device(self):
        self.port = self.ui.list_devices.currentText()
        print(self.port)
        self.zc = zonnecel_experiment(self.port)
    
    @Slot()
    def start_scan(self):
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
        self.ui.IU_graph.plot(self.zc.U_gem, self.zc.I_gem, symbol="o", symbolSize=5, pen=None)
        error_bars = pg.ErrorBarItem(x=np.array(self.zc.U_gem), y=np.array(self.zc.I_gem), height = np.array(self.zc.I_error))
        self.ui.IU_graph.addItem(error_bars)
        self.ui.IU_graph.setLabel('left', text='Current in Ampére')
        self.ui.IU_graph.setLabel('bottom', text='Voltage in Volt')
        
        self.ui.PU_graph.plot(self.zc.U_gem, self.zc.P_gem, symbol="o", symbolSize=5, pen=None)
        errors = pg.ErrorBarItem(x=np.array(self.zc.U_gem), y=np.array(self.zc.P_gem), height = 2*np.array(self.zc.P_error))
        self.ui.PU_graph.addItem(errors)


    @Slot()
    def ff(self):
        self.ui.text_line.clear()
        self.ui.text_line.setText(f'{self.zc.ff}')

    @Slot()
    def save_data(self, port):
        if self.ui.list_devices.currentIndex() == 1:
            port = 'ASRL::SIMPV_BRIGHT::INSTR'

        start = int(self.ui.start_button.value())
        end = int(self.ui.end_button.value())
        runs = int(self.runs_button.value())
        zc = zonnecel_experiment(port)

        diode = zc.scan(start, end, runs)
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
