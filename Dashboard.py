import pyqtgraph as pg
from PyQt6 import QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Temperature vs time plot
        self.plot_graph = pg.PlotWidget()
        self.setCentralWidget(self.plot_graph)
        minutes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [3, 2, 6, 7, 5, 5, 5, 5, 6, 4]
        self.plot_graph.plot(minutes, temperature)

app = QtWidgets.QApplication([])
main = MainWindow()
main.show()
app.exec()