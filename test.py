import numpy as np
import matplotlib.pyplot as plt
import math


def shooting(ddy, y1, y2, x, h, eps=0.0001):
    n0 = y2
    n1 = 1.8
    n = [n0, n1]
    yn1 = RungeKutta(ddy, n0, y1, x, h)
    yn2 = RungeKutta(ddy, n1, y1, x, h)
    yn = [yn1, yn2]

    j = 0
    while math.fabs(yn[-1][-1] - y2) > eps and j < 100:
        print(yn[-1][-1], y2, math.fabs(yn[-1][-1] - y2))
        nk = n[j + 1] - (n[j + 1] - n[j]) / (yn[j + 1][-1] - yn[j][-1]) * yn[j + 1][-1]
        yn.append(RungeKutta(ddy, nk, y1, x, h))
        n.append(nk)
        j += 1

    return yn[-1]


def shooting(ddy, y1, y2, x, h, eps=0.0001):
    n0 = y2
    n1 = 1.8
    n = [n0, n1]
    yn1 = RungeKutta(ddy, y1, n0, x, h)
    yn2 = RungeKutta(ddy, y1, n1, x, h)
    yn = [yn1, yn2]

    j = 0
    while math.fabs(yn[-1][-1] - y2) > eps and j < 100:
        print(yn[-1][-1], y2, math.fabs(yn[-1][-1] - y2))
        nk = n[j + 1] - (n[j + 1] - n[j]) / (yn[j + 1][-1] - yn[j][-1]) * yn[j + 1][-1]
        yn.append(RungeKutta(ddy, y1, nk, x, h))
        n.append(nk)
        j += 1

    return yn[-1]

function = lambda x, y, dy: math.exp(x) + math.sin(y)
interval = [0, 1]
step = 0.1
y1 = 1
y2 = 2
# Точное решение
y_lambda = lambda x: -1 + 2/x + 2*(x + 1)/x * math.log(abs(x + 1))

x_list = list(np.arange(interval[0], interval[1] + step / 2, step))

shooting = shooting(function, y1, y2, x_list, step)