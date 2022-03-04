import math
import tkinter as tk
import tkinter.font as tkFont
from scipy.linalg import solve_banded
import numpy as np

'''
-14 -6 -78
-9 15 -1 -73
1 -11 10 -38
-7 12 3 77
6 -7 91

-14 -6 0 0 0 -78
-9 15 -1 0 0 -73
0 1 -11 10 0 -38
0 0 -7 12 3 77
0 0 0 6 -7 91
'''

a = [
    [-14, -6, 0, 0, 0],
    [-9, 15, -1, 0, 0],
    [0, 1, -11, 10, 0],
    [0, 0, -7, 12, 3],
    [0, 0, 0, 6, -7]
]

b = [-78, -73, -38, 77, 91]

u = 1
l = 1
n = 5
m = 5

a = np.array(a)
b = np.array(b)
ab = np.zeros((u + l + 1, m))
for j in range(m):
    for i in range(n):
        index = u + i - j
        if 0 <= index < u + l + 1:
            ab[index][j] = a[i][j]
print('Проверка через внутренние библиотеки:')
print(solve_banded((l, u), ab, b))


def Progonka(arr):
    A = [[arr[i][j] for j in range(len(arr[i]))] for i in range(len(arr))]
    n = len(A)

    #   Формирование массивов чисел a, b, c, d _____________
    #   a = [a0, a1, a2, ..., a_n]
    a, b, c, d = [0], [arr[0][0]], [arr[0][1]], [arr[0][2]]
    for i in arr[1:-1]:
        a.append(i[0])
        b.append(i[1])
        c.append(i[2])
        d.append(i[3])

    a.append(arr[-1][0])
    b.append(arr[-1][1])
    c.append(0)
    d.append(arr[-1][2])

    for i in range(n):
        if math.fabs(b[i]) < math.fabs(a[i]) + math.fabs(c[i]):
            raise Exception

    #   Формирование массивов P, Q (Расчет значений) ((Прямой ход))

    P, Q = [-c[0] / b[0]], [d[0] / b[0]]

    for i in range(1, n):
        P.append(-c[i] / (b[i] + a[i] * P[i - 1]))
        Q.append((d[i] - a[i] * Q[i - 1]) / (b[i] + a[i] * P[i - 1]))

    #   Вычисление решения системы (Обратный ход)
    x = [Q[n - 1]]
    for i in range(1, n):
        x.append(P[n - 1 - i] * x[i - 1] + Q[n - 1 - i])

    print('P:')
    print(np.array(P))
    print('Q:')
    print(np.array(Q))

    x = reversed(x)
    return x


def CheckArr(arr):
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            q = arr[i][j]
            if i != j and i - 1 != j and i + 1 != j and j != len(arr[0]) - 1 and q != 0:
                return False

    return True


def Calculate():
    arr = [list(map(float, i.split())) for i in table_coefs.get('1.0', tk.END).split('\n')]

    while (len(arr[len(arr) - 1])) == 0:
        arr.pop()

    ans = ''
    for i in Progonka(arr):
        ans += str(round(i, 4)) + ' '

    entry_roots.delete(0, tk.END)
    entry_roots.insert(0, ans)


def Clean():
    table_coefs.delete('1.0', tk.END)
    entry_roots.delete(0, tk.END)


window = tk.Tk()
window.title('Решение СЛАУ методом Прогонки')

font_arial = tkFont.Font(family="Arial", size=14)

tk.Label(text="A|B =", font=font_arial).grid(row=0, column=0, sticky='e', pady=10, padx=10)
table_coefs = tk.Text(width=40, height=10, font=font_arial)
table_coefs.grid(row=0, column=1, columnspan=3, sticky='w', padx=10)

tk.Label(text="x\U00002081, x\U00002082, ... :", font=font_arial).grid(row=2, column=0, sticky='e', padx=10, pady=10)
entry_roots = tk.Entry(font=font_arial, width=40)
entry_roots.grid(row=2, column=1, columnspan=3, sticky='w', padx=10)

tk.Button(text="Вычислить", command=Calculate, font=font_arial).grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky='w')
tk.Button(text="Очистить", command=Clean, font=font_arial).grid(row=4, column=3, padx=10, sticky='e')


tk.mainloop()