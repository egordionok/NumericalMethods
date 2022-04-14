from math import *
import tkinter as tk
from tkinter.filedialog import askopenfilename
import tkinter.font as tkFont
import numpy as np
import matplotlib.pyplot as plt

#   Сделаем в диф-уре ddy = f(x, y, dy) замену
#   dy/dx = z
#   dz/dx = f(x, y, z)
#   и будем решать два уравнения
#   dy/dx = g(x, y, z) = z
#   dz/dx = f(x, y, z)


# Метод Эйлера
def Euler(ddy, dy0, y0, x, h):
    y = [0 for i in range(len(x))]
    z = [0 for i in range(len(x))]
    y[0] = y0
    z[0] = dy0

    for i in range(1, len(x)):
        y[i] = y[i - 1] + h * z[i - 1]
        z[i] = z[i - 1] + h * ddy(x[i - 1], y[i - 1], z[i - 1])
    return y

# Метод Эйлера с пересчетом
def EulerModificated(ddy, dy0, y0, x, h):
    y = [0 for i in range(len(x))]
    z = [0 for i in range(len(x))]
    y[0] = y0
    z[0] = dy0

    for i in range(1, len(x)):
        yk = y[i - 1] + h * z[i - 1]
        zk = z[i - 1] + h * ddy(x[i - 1], y[i - 1], z[i - 1])
        y[i] = y[i - 1] + h * (zk + z[i - 1]) / 2
        z[i] = z[i - 1] + h * (ddy(x[i - 1], yk, zk) + ddy(x[i], y[i - 1], z[i - 1]) )/ 2

    return y


def RungeKutta(ddy, dy0, y0, x, h):
    y = [0 for i in range(len(x))]
    z = [0 for i in range(len(x))]
    y[0] = y0
    z[0] = dy0

    for i in range(1, len(x)):
        #   коэфиценты для dy/dx = z
        ky1 = z[i - 1]
        ky2 = z[i - 1] + h * ky1 / 2
        ky3 = z[i - 1] + h * ky2 / 2
        ky4 = z[i - 1] + h * ky3

        #   коэфиценты для dz/dx = f(x, y, z)
        kz1 = ddy(x[i - 1], y[i - 1], z[i - 1])
        kz2 = ddy(x[i - 1] + h / 2, y[i - 1] + h * kz1 / 2, z[i - 1] + h * kz1 / 2)
        kz3 = ddy(x[i - 1] + h / 2, y[i - 1] + h * kz2 / 2, z[i - 1] + h * kz2 / 2)
        kz4 = ddy(x[i - 1] + h, y[i - 1] + h * kz3, z[i - 1] + h * kz3)

        z[i] = z[i - 1] + h * (kz1 + 2 * kz2 + 2 * kz3 + kz4) / 6
        y[i] = y[i - 1] + h * (ky1 + 2 * ky2 + 2 * ky3 + ky4) / 6

    return y


def Adams(ddy, dy0, y0, x, h):
    y = [0 for i in range(len(x))]
    z = [0 for i in range(len(x))]
    y[0] = y0
    z[0] = dy0

    #   Находим первые 4 значения в сетке методом Рунге-Кутта 4-го порядка для dy и y
    for i in range(1, 4):
        #   коэфиценты для z = dy
        ky1 = z[i - 1]
        ky2 = z[i - 1] + h * ky1 / 2
        ky3 = z[i - 1] + h * ky2 / 2
        ky4 = z[i - 1] + h * ky3

        #   коэфиценты для dz = f(x, y, z)
        kz1 = ddy(x[i - 1], y[i - 1], z[i - 1])
        kz2 = ddy(x[i - 1] + h / 2, y[i - 1] + h * kz1 / 2, z[i - 1] + h * kz1 / 2)
        kz3 = ddy(x[i - 1] + h / 2, y[i - 1] + h * kz2 / 2, z[i - 1] + h * kz2 / 2)
        kz4 = ddy(x[i - 1] + h, y[i - 1] + h * kz3, z[i - 1] + h * kz3)

        z[i] = z[i - 1] + h * (kz1 + 2 * kz2 + 2 * kz3 + kz4) / 6
        y[i] = y[i - 1] + h * (ky1 + 2 * ky2 + 2 * ky3 + ky4) / 6

    #   Используем метод Адамся для нахождения след значений
    for i in range(4, len(x)):
        k1 = ddy(x[i - 1], y[i - 1], z[i - 1])
        k2 = ddy(x[i - 2], y[i - 2], z[i - 2])
        k3 = ddy(x[i - 3], y[i - 3], z[i - 3])
        k4 = ddy(x[i - 4], y[i - 4], z[i - 4])

        z[i] = z[i - 1] + h / 24 * (55 * k1 - 59 * k2 + 37 * k3 - 9 * k4)
        y[i] = y[i - 1] + h / 24 * (55 * z[i - 1] - 59 * z[i - 2] + 37 * z[i - 3] - 9 * z[i - 4])

    return y



def clear():
    entry_diff_function.delete(0, tk.END)
    entry_function.delete(0, tk.END)
    entry_interval.delete(0, tk.END)
    entry_step.delete(0, tk.END)
    entry_dy0.delete(0, tk.END)
    entry_y0.delete(0, tk.END)


def readFile():
    clear()
    file = open(askopenfilename(), 'r')
    file_text = file.read().split('\n')
    entry_diff_function.insert(0, file_text[0])
    zeros = file_text[1].split()
    entry_y0.insert(0, zeros[0])
    entry_dy0.insert(0, zeros[1])
    entry_interval.insert(0, file_text[2])
    entry_step.insert(0, file_text[3])
    if len(file_text) > 4:
        entry_function.insert(0, file_text[4])


def functionParce():
    function = lambda x, y, dy: eval(entry_diff_function.get().strip(' '))
    interval = [float(a) for a in entry_interval.get().strip('[ ]').split(';')]
    step = float(entry_step.get())
    y0 = float(entry_y0.get())
    dy0 = float(entry_dy0.get())
    return function, interval, step, y0, dy0


def count():
    function, interval, step, y0, dy0 = functionParce()
    x_list = list(np.arange(interval[0], interval[1] + step / 2, step))
    euler = Euler(function, dy0, y0, x_list, step)
    euler_modif = EulerModificated(function, dy0, y0, x_list, step)
    runge_kutt = RungeKutta(function, dy0, y0, x_list, step)
    adams = Adams(function, dy0, y0, x_list, step)

    if entry_function.get().strip(' ') != '':
        y_lambda = lambda x: eval(entry_function.get().strip(' '))
        y = [y_lambda(x) for x in x_list]
        plt.plot(x_list, y, label="y(x)")
    if varE.get() == 1:
        plt.plot(x_list, euler, label="Euler")
    if varEM.get() == 1:
        plt.plot(x_list, euler_modif, label="EulerModificated")
    if varRK.get() == 1:
        plt.plot(x_list, runge_kutt, label="Runge-Kutta")
    if varA.get() == 1:
        plt.plot(x_list, adams, label="Adams")

    plt.legend(loc=2)
    plt.grid(True)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

    return 0


window = tk.Tk()

window.title('Решение задачи Коши различными методами')
font_arial = tkFont.Font(family="Arial", size=14)

tk.Label(text="y'' =", font=font_arial).grid(row=0, column=0, sticky='e', pady=10, padx=10)
entry_diff_function = tk.Entry(font=font_arial)
entry_diff_function.grid(row=0, column=1, columnspan=3, sticky='we', padx=10)

tk.Label(text="y =", font=font_arial).grid(row=1, column=0, sticky='e', pady=10, padx=10)
entry_function = tk.Entry(font=font_arial)
entry_function.grid(row=1, column=1, columnspan=3, sticky='we', padx=10)

tk.Label(text="dy\U00002080 =", font=font_arial).grid(row=2, column=0, sticky='e', pady=10, padx=10)
entry_dy0 = tk.entry_interval = tk.Entry(font=font_arial, width=10)
entry_dy0.grid(row=2, column=1, sticky='w', padx=10)

tk.Label(text="y\U00002080 =", font=font_arial).grid(row=2, column=2, sticky='e', pady=10, padx=10)
entry_y0 = tk.entry_interval = tk.Entry(font=font_arial, width=10)
entry_y0.grid(row=2, column=3, sticky='w', padx=10)

tk.Label(text="Интервал:", font=font_arial).grid(row=3, column=0, sticky='w', pady=10, padx=10)
entry_interval = tk.Entry(font=font_arial, width=10)
entry_interval.grid(row=3, column=1, sticky='we', padx=10)

tk.Label(text="Шаг:", font=font_arial).grid(row=3, column=2, sticky='e', pady=10, padx=10)
entry_step = tk.Entry(font=font_arial, width=10)
entry_step.grid(row=3, column=3, sticky='we', padx=10)

varE = tk.IntVar()
varEM = tk.IntVar()
varRK = tk.IntVar()
varA = tk.IntVar()
varE.set(1)
varEM.set(1)
varRK.set(1)
varA.set(1)

check_box_euler = tk.Checkbutton(window, text='Euler', variable=varE, onvalue=1, offvalue=0)
check_box_euler.grid(row=4, column=0, pady=10, padx=10)
check_box_eulerM = tk.Checkbutton(window, text='EulerModificated', variable=varEM, onvalue=1, offvalue=0)
check_box_eulerM.grid(row=4, column=1, pady=10, padx=10)
check_box_rk = tk.Checkbutton(window, text='Runge-Kutta', variable=varRK, onvalue=1, offvalue=0)
check_box_rk.grid(row=4, column=2, pady=10, padx=10)
check_box_adams = tk.Checkbutton(window, text='Adams', variable=varA, onvalue=1, offvalue=0)
check_box_adams.grid(row=4, column=3, pady=10, padx=10)

tk.Button(text="Выбрать файл", command=readFile, font=font_arial). \
    grid(row=5, column=0, columnspan=2, pady=10, padx=10, sticky='w')
tk.Button(text="Расчет", command=count, font=font_arial). \
    grid(row=5, column=3, pady=10, padx=10, sticky='e')


window.mainloop()
