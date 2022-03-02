import tkinter as tk
import tkinter.font as tkFont
from copy import copy


def Progonka(arr):
    A = [[arr[i][j] for j in range(len(arr[i]))] for i in range(len(arr))]
    n = len(A)

    #   Формирование массивов чисел a, b, c, d _____________
    #   a = [a0, a1, a2, ..., a_n]

    a, b, c, d = [], [], [], []
    a.append(0)
    b.append(A[0][0])
    c.append(A[0][1])
    d.append(A[0][n])

    for i in range(1, n - 1):
        a.append(A[i][i - 1])
        b.append(A[i][i])
        c.append(A[i][i + 1])
        d.append(A[i][len(A[i]) - 1])

    a.append(A[n - 1][n - 2])
    b.append(A[n - 1][n - 1])
    c.append(0)
    d.append(A[n - 1][n])

    #   Формирование массивов P, Q (Расчет значений) __________

    P, Q = [-c[0] / b[0]], [d[0] / b[0]]

    for i in range(1, n):
        P.append(-c[i] / (b[i] + a[i] * P[i - 1]))
        Q.append((d[i] - a[i] * Q[i - 1]) / (b[i] + a[i] * P[i - 1]))

    #   Вычисление решения системы ___________
    x = [Q[n - 1]]
    for i in range(1, n):
        x.append(P[n - 1 - i] * x[i - 1] + Q[n - 1 - i])

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

    if not CheckArr(arr):
        entry_roots.delete(0, tk.END)
        entry_roots.insert(0, "Матрица не трехдиагональная")
        return 0

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
table_coefs = tk.Text(width=21, height=10, font=font_arial)
table_coefs.grid(row=0, column=1, columnspan=3, sticky='w', padx=10)

tk.Label(text="x\U00002081, x\U00002082, ... :", font=font_arial).grid(row=2, column=0, sticky='e', padx=10, pady=10)
entry_roots = tk.Entry(font=font_arial)
entry_roots.grid(row=2, column=1, columnspan=3, sticky='w', padx=10)

tk.Button(text="Вычислить", command=Calculate, font=font_arial).grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky='w')
tk.Button(text="Очистить", command=Clean, font=font_arial).grid(row=4, column=3, padx=10, sticky='e')


tk.mainloop()