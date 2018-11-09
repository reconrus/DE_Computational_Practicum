from numpy import exp
import numpy as np


class NumericalMethod:
    def __init__(self, x0, y0, N, X):
        self.N = N
        self.h = (X-x0)/N
        self.xy = [(x0, y0)]
        self.X = X
        self.local_error = [0]
        self.global_error = 0

    def fill_xy(self):
        while self.xy[-1][0] < self.X:
            self.xiyi()
        return np.array(self.xy).T


class ExactSolution(NumericalMethod):
    def __init__(self, x0, y0, N, X):
        super(ExactSolution, self).__init__(x0, y0, N, X)
        self.c = (y0 - 3)/(y0*exp(3*x0*x0/2))
        #self.c = (y0 - (np.sin(x0) + np.cos(x0))/2)*exp(x0) #for exact solution

    def xiyi(self):
        xi = self.xy[-1][0] + self.h
        yi = self.exact_f(xi)
        self.xy.append((xi, yi))

    def exact_f(self, x):
        return 3/(1-self.c*exp(3*x*x/2))
        #return (np.sin(x) + np.cos(x))/2 + self.c*exp(-x)


class EulerMethod(NumericalMethod):
    def xiyi(self):
        x, y = self.xy[-1]

        xi = x + self.h
        yi = y + self.h * RHS.fxy(x, y)

        self.xy.append((xi, yi))


class ImprovedEulerMethod(NumericalMethod):
    def xiyi(self):
        x, y = self.xy[-1]

        xi = x + self.h
        k1 = RHS.fxy(x, y)
        k2 = RHS.fxy(xi, y + self.h*k1)

        yi = y + self.h*(k1 + k2)/2

        self.xy.append((xi, yi))


class RungeKuttaMethod(NumericalMethod):
    def xiyi(self):
        x, y = self.xy[-1]

        xi = x + self.h
        k1 = RHS.fxy(x, y)
        k2 = RHS.fxy(x + self.h/2, y + self.h * k1/2)
        k3 = RHS.fxy(x + self.h/2, y + self.h * k2/2)
        k4 = RHS.fxy(xi, y + self.h * k3)

        yi = y + self.h * (k1 + 2*k2 + 2*k3 + k4) / 6

        self.xy.append((xi, yi))


class ErrorComputer:

    @staticmethod
    def compute_local_error(exact, numerical):
        return np.abs(exact[1] - numerical[1])

    @staticmethod
    def compute_global_error(x0, y0, X, N0, N1, method):
        global_errors = []

        for i in range(N0, N1 + 1):
            if method == "Euler":
                sol = EulerMethod(x0, y0, i, X).fill_xy()
            elif method == "Improved Euler":
                sol = ImprovedEulerMethod(x0, y0, i, X).fill_xy()
            elif method == "Runge Kutta":
                sol = RungeKuttaMethod(x0, y0, i, X).fill_xy()

            exact = ExactSolution(x0, y0, i, X).fill_xy()
            global_errors.append(max(ErrorComputer.compute_local_error(exact, sol)))

        return np.array([np.arange(N0, N1 + 1), global_errors])


class RHS:
    @staticmethod
    def fxy(x, y):
        yi = x * y * (y - 3)
        #yi = np.cos(x) - y
        # if we use improved euler method, plot goes to infinity if h is not enough small
        return yi  # if yi < 100 else 0


