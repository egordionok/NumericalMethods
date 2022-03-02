import tkinter as tk
import tkinter.font as tkFont
import numpy as np

# A = [
#     [-1, -7, -3, -2],
#     [-8, 1, -9, 0],
#     [8, 2, -5, -3],
#     [-5, 3, 5, -9]
# ]
#
# b = [-12, -60, -91, -43]

"""
-1 -7 -2 -2
-8 1 -9 0
8 2 -5 -3
-5 3 5 -9

-12
-60
-91
-43
"""

# A = [
#     [-4, -9, 4, 3],
#     [2, 7, 9, 8],
#     [4, -4, 0, -2],
#     [-8, 5, 2, 9]
#     ]
# b = [-51, 76, 26, -73]

"""
-4 -9 4 3
2 7 9 8
4 -4 0 -2
-8 5 2 9

-51
76
26
-73
"""


def lu_dec(A):
    """
    Функция LU разложения матрицы
    :param A: Матрица, которую нужно разложить
    :return L, U: Мтарицы L, U
    """
    n = len(A)
    L = [[1 if i == j else 0 for i in range(n)] for j in range(n)]
    U = [[0 for i in range(n)] for j in range(n)]

    for i in range(n):
        for j in range(n):
            if i <= j:
                U[i][j] = A[i][j] - sum([L[i][k] * U[k][j] for k in range(i)])
            else:
                L[i][j] = (A[i][j] - sum([L[i][k] * U[k][j] for k in range(j)])) / U[j][j]

    print(np.array(L))
    print(np.array(U))
    return L, U


def decision(A, b):
    """
    Решение СЛАУ методом LU разложения
    :param A:
    :param b:
    :return x:
    """
    n = len(A)
    L, U = lu_dec(A)

    # L * y  = b
    y = [0 for i in range(n)]
    for i in range(n):
        y[i] = (b[i] - sum([L[i][k] * y[k] for k in range(i)]))

    x = [0 for i in range(n)]

    for i in range(n - 1, -1, -1):
        x[i] = round((y[i] - sum([U[i][k] * x[k] for k in range(i + 1, n)])) / U[i][i], 4)

    print(x)
    print(np.linalg.solve(A, b))

    return x


def Calculate():
    a = [list(map(float, i.split())) for i in table_coefs.get('1.0', tk.END).split('\n') if len(i)]
    b = [float(i) for i in table_b.get('1.0', tk.END).split('\n') if i != '']

    ans = ''
    for i in decision(a, b):
        ans += str(round(i, 4)) + ' '

    entry_roots.delete(0, tk.END)
    entry_roots.insert(0, ans)


def Clean():
    table_coefs.delete('1.0', tk.END)
    entry_roots.delete(0, tk.END)


window = tk.Tk()
window.title('Решение СЛАУ с помощью LU разложения')

font_arial = tkFont.Font(family="Arial", size=14)

tk.Label(text="A =", font=font_arial).grid(row=0, column=0, sticky='e', pady=10, padx=10)
table_coefs = tk.Text(width=21, height=10, font=font_arial)
table_coefs.grid(row=0, column=1, columnspan=3, sticky='w', padx=10)

tk.Label(text="b =", font=font_arial).grid(row=0, column=4, sticky='e', pady=10, padx=10)
table_b = tk.Text(width=3, height=10, font=font_arial)
table_b.grid(row=0, column=5, sticky='w', padx=10)

tk.Label(text="x\U00002081, x\U00002082, ... :", font=font_arial).grid(row=2, column=0, columnspan=2, sticky='e', padx=10, pady=10)
entry_roots = tk.Entry(font=font_arial)
entry_roots.grid(row=2, column=2, columnspan=3, sticky='w', padx=10)

tk.Button(text="Вычислить", command=Calculate, font=font_arial).grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky='w')
tk.Button(text="Очистить", command=Clean, font=font_arial).grid(row=4, column=3, padx=10, sticky='e')


tk.mainloop()