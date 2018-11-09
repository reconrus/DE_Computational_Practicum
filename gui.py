import os
os.environ['PYQTGRAPH_QT_LIB'] = 'PyQt5'

from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
import pyqtgraph as pg
import solutions as nm


class NumericalSolutionsPlots(QtWidgets.QWidget):

    def __init__(self):
        super(NumericalSolutionsPlots, self).__init__()
        self.initUI()

    def initUI(self):

        self.init_plots()

        top_hbox = QtWidgets.QHBoxLayout()
        top_hbox.addWidget(self.solutions_plot)
        top_hbox.addWidget(self.local_errors_plot)

        bottom_hbox = QtWidgets.QHBoxLayout()
        bottom_hbox.addWidget(self.init_input_box())
        bottom_hbox.addWidget(self.global_errors_plot)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(top_hbox)
        vbox.addLayout(bottom_hbox)

        self.qt_connections()

        self.plot_graph()
        self.setLayout(vbox)

        self.resize(1366, 768)

        self.show()

    def init_plots(self):
        self.solutions_plot = pg.PlotWidget(title="Solutions")
        self.local_errors_plot = pg.PlotWidget(title="Local Errors")
        self.global_errors_plot = pg.PlotWidget(title="Global Errors")

        self.solutions_plot.setLabel('left', '<h4>y</h4>')
        self.solutions_plot.setLabel('bottom', '<h4>x</h4>')
        self.local_errors_plot.setLabel('left', '<h4>e</h4>')
        self.local_errors_plot.setLabel('bottom', '<h4>x</h4>')
        self.global_errors_plot.setLabel('left', '<h4>e</h4>')
        self.global_errors_plot.setLabel('bottom', '<h4>n</h4>')


    def init_input_box(self):
        x0_text = QtWidgets.QLabel('x0:')
        y0_text = QtWidgets.QLabel('y0:')
        X_text = QtWidgets.QLabel('X: ')
        N_text = QtWidgets.QLabel('N: ')
        max_N_text = QtWidgets.QLabel("Max N: ")
        self.x0_in = QtWidgets.QLineEdit('0')
        self.y0_in = QtWidgets.QLineEdit('2')
        self.X_in = QtWidgets.QLineEdit('6.4')
        self.N_in = QtWidgets.QLineEdit('50')
        self.max_N_in = QtWidgets.QLineEdit('100')


        x0_hbox = QtWidgets.QHBoxLayout()
        x0_hbox.addWidget(x0_text)
        x0_hbox.addWidget(self.x0_in)

        y0_hbox = QtWidgets.QHBoxLayout()
        y0_hbox.addWidget(y0_text)
        y0_hbox.addWidget(self.y0_in)

        X_hbox = QtWidgets.QHBoxLayout()
        X_hbox.addWidget(X_text)
        X_hbox.addWidget(self.X_in)

        N_hbox = QtWidgets.QHBoxLayout()
        N_hbox.addWidget(N_text)
        N_hbox.addWidget(self.N_in)

        max_N_hbox = QtWidgets.QHBoxLayout()
        max_N_hbox.addWidget(max_N_text)
        max_N_hbox.addWidget(self.max_N_in)

        self.plot_button = QtWidgets.QPushButton("Plot")

        in_vbox = QtWidgets.QVBoxLayout()
        in_vbox.setAlignment(QtCore.Qt.AlignCenter)
        in_vbox.addLayout(x0_hbox)
        in_vbox.addLayout(y0_hbox)
        in_vbox.addLayout(X_hbox)
        in_vbox.addLayout(N_hbox)
        in_vbox.addLayout(max_N_hbox)
        in_vbox.addWidget(self.plot_button)

        input_box = QtWidgets.QWidget()
        input_box.setLayout(in_vbox)

        return input_box

    def qt_connections(self):
        self.plot_button.clicked.connect(self.update_graph)

    def update_graph(self):
        self.solutions_plot.clear()
        self.local_errors_plot.clear()
        self.global_errors_plot.clear()

        self.solutions_legend.scene().removeItem(self.solutions_legend)
        self.local_errors_legend.scene().removeItem(self.local_errors_legend)
        self.global_errors_legend.scene().removeItem(self.global_errors_legend)

        self.plot_graph()

    def plot_graph(self):
        self.x0 = float(self.x0_in.text())
        self.y0 = float(self.y0_in.text())
        self.X = float(self.X_in.text())
        self.N = int(self.N_in.text())
        self.max_N = int(self.max_N_in.text())

        self.solutions_legend = self.solutions_plot.addLegend(offset=(500, 50))
        self.local_errors_legend = self.local_errors_plot.addLegend(offset=(500, 50))
        self.global_errors_legend = self.global_errors_plot.addLegend(offset=(500, 50))

        self.plot_solutions()
        self.plot_local_error()
        self.plot_global_error()

    def plot_solutions(self):
        self.exact_solution = nm.ExactSolution(self.x0, self.y0, self.N, self.X).fill_xy()
        self.euler_solution = nm.EulerMethod(self.x0, self.y0, self.N, self.X).fill_xy()
        self.improved_euler_solution = nm.ImprovedEulerMethod(self.x0, self.y0, self.N, self.X).fill_xy()
        self.runge_kutta_solution = nm.RungeKuttaMethod(self.x0, self.y0, self.N, self.X).fill_xy()

        self.solutions_plot.plot(self.exact_solution[0], self.exact_solution[1], pen=(0, 255, 0), name="Exact")
        self.solutions_plot.plot(self.euler_solution[0], self.euler_solution[1], pen=(255, 0, 0), name="Euler")
        self.solutions_plot.plot(self.improved_euler_solution[0], self.improved_euler_solution[1], pen=(0, 0, 255), name="Improved Euler")
        self.solutions_plot.plot(self.runge_kutta_solution[0], self.runge_kutta_solution[1], pen=(255, 255, 0), name="Runge Kutta")

    def plot_local_error(self):
        euler_local = nm.ErrorComputer.compute_local_error(self.exact_solution, self.euler_solution)
        improved_euler_local = nm.ErrorComputer.compute_local_error(self.exact_solution, self.improved_euler_solution)
        runge_kutta_local = nm.ErrorComputer.compute_local_error(self.exact_solution, self.runge_kutta_solution)

        self.local_errors_plot.plot(self.exact_solution[0], euler_local, pen=(255, 0, 0), name="Euler")
        self.local_errors_plot.plot(self.exact_solution[0], improved_euler_local, pen=(0, 0, 255), name="Improved Euler")
        self.local_errors_plot.plot(self.exact_solution[0], runge_kutta_local, pen=(255, 255, 0), name="Runge Kutta")

    def plot_global_error(self):
        euler_global = nm.ErrorComputer.compute_global_error(self.x0, self.y0, self.X, self.N, self.max_N, "Euler")
        improved_euler_global = nm.ErrorComputer.compute_global_error(self.x0, self.y0, self.X, self.N, self.max_N, "Improved Euler")
        runge_kutta_global = nm.ErrorComputer.compute_global_error(self.x0, self.y0, self.X, self.N, self.max_N, "Runge Kutta")

        self.global_errors_plot.plot(euler_global[0], euler_global[1], pen=(255, 0, 0), name="Euler")
        self.global_errors_plot.plot(improved_euler_global[0], improved_euler_global[1], pen=(0, 0, 255), name="Improved Euler")
        self.global_errors_plot.plot(runge_kutta_global[0], runge_kutta_global[1], pen=(255, 255, 0), name="Runge Kutta")


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('Numerical Solutions')
    ex = NumericalSolutionsPlots()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()