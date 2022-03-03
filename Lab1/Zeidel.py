import tkinter as tk
import tkinter.font as tkFont
import numpy as np


def vector_norm(x):
    m = abs(x[0])
    for i in x:
        if abs(i) > m:
            m = abs(i)
    return m


def SimpleIterations(arr):
    A = [[arr[i][j] for j in range(len(arr[i]) - 1)] for i in range(len(arr))]
    n = len(A)
    B = [arr[i][len(A[0])] for i in range(n)]

    # a_11*x1 + a_12*x2 + ... + a_1n*xn = b_1
    # .....    ......   ...   ......  ...
    # a_n1*x1 + a_n2*x2 + ... + a_nn*xn = b_n
    #
    #       ||
    #       \/
    #
    # x1(k+1) = alpha_11*x1(k) + alpha_12*x2 + ... + alpha_1n*xn = betta_1
    # .....    ......   ...   ......  ...
    # xn = alpha_n1*x1 + alpha_n2*x2 + ... + alpha_nn*xn = betta_n

    alpha = np.array([[-A[i][j] / A[i][i] for j in range(n)] for i in range(n)])
    for i in range(n):
        alpha[i][i] = 0
    betta = np.array([B[i] / A[i][i] for i in range(n)])

    x = np.copy(betta)
    eps = 1
    n = 0

    while eps >= 0.00001:
        x_last = x
        x = np.dot(alpha, x) + betta
        eps = vector_norm(x - x_last)
        n += 1

    return x, n


def Zeidel(arr):
    A = [[arr[i][j] for j in range(len(arr[i]) - 1)] for i in range(len(arr))]
    n = len(A)
    B = [arr[i][len(A[0])] for i in range(n)]

    # a_11*x1 + a_12*x2 + ... + a_1n*xn = betta_1
    # .....    ......   ...   ......  ...
    # a_n1*x1 + a_n2*x2 + ... + a_nn*xn = betta_n
    #
    #       ||
    #       \/
    #
    # x1(k+1) = alpha_11*x1(k) + alpha_12*x2(k) + ... + alpha_1n*xn(k) = betta_1
    # x2(k+1) = alpha_21*x1(k+1) + alpha_22*x2(k) + ... + alpha_2n*xn(k) = betta_2
    # x3(k+1) = alpha_31*x1(k+1) + alpha_32*x2(k+1) + ... + alpha_3n*xn(k) = betta_3
    # .....    ......   ...   ......  ...
    # xn(k+1) = alpha_n1*x1(k+1) + alpha_n2*x2(k+1) + ... + alpha_nn*xn(k+1) = betta_n

    alpha = np.array([[-A[i][j] / A[i][i] for j in range(n)] for i in range(n)])
    for i in range(n):
        alpha[i][i] = 0
    betta = np.array([B[i] / A[i][i] for i in range(n)])

    B = [[0 for j in range(n)] for i in range(n)]
    C = [[0 for j in range(n)] for i in range(n)]

    E = np.eye(n)

    for i in range(n):
        for j in range(n):
            if j < i:
                B[i][j] = alpha[i][j]  # Нижняя треугольная матрица с для коэф x_i(k+1) с 0 диагональю
            else:
                C[i][j] = alpha[i][j]  # Верхняя треугольная матрица с для коэф x_i(k)

    # alpha = B + C

    x = np.copy(betta)
    eps = 1
    n = 0

    while eps >= 0.00001:
        x_last = x

        #   (E - B) * x(k + 1) = C * x(k) + betta | : (E - B)
        #   x(k + 1) = (E - B)^-1 * C * x(k) + (E - B)^-1 * betta

        BE = np.linalg.inv(E - B)
        x = np.dot(np.dot(BE, C), x) + np.dot(BE, betta)
        eps = vector_norm(x - x_last)
        n += 1

    return x, n


def Calculate():
    arr = [list(map(float, i.split())) for i in table_coefs.get('1.0', tk.END).split('\n')]

    while (len(arr[len(arr) - 1])) == 0:
        arr.pop()

    a1, n1 = SimpleIterations(arr)
    a2, n2 = Zeidel(arr)

    ans1 = ''
    for i in a1:
        ans1 += str(round(i, 4)) + ' '

    ans2 = ''
    for i in a2:
        ans2 += str(round(i, 4)) + ' '

    entry_roots1.delete(0, tk.END)
    entry_roots1.insert(0, ans1)
    label_n1['text'] = str(n1)

    entry_roots2.delete(0, tk.END)
    entry_roots2.insert(0, ans2)
    label_n2['text'] = str(n2)


def Clean():
    table_coefs.delete('1.0', tk.END)
    entry_roots1.delete(0, tk.END)
    entry_roots2.delete(0, tk.END)
    label_n1['text'] = ''
    label_n2['text'] = ''


window = tk.Tk()
window.title('Решение СЛАУ методом простых итераций')

font_arial = tkFont.Font(family="Arial", size=14)

tk.Label(text="A|B =", font=font_arial).grid(row=0, column=0, sticky='e', pady=10, padx=10)
table_coefs = tk.Text(width=21, height=10, font=font_arial)
table_coefs.grid(row=0, column=1, columnspan=3, sticky='w', padx=10)

tk.Label(text="Метод простых итераций", font=font_arial).grid(row=1, column=0, columnspan=4, sticky='we', padx=10,
                                                              pady=10)

tk.Label(text="x\U00002081, x\U00002082, ... :", font=font_arial).grid(row=2, column=0, sticky='e', padx=10, pady=10)
entry_roots1 = tk.Entry(font=font_arial)
entry_roots1.grid(row=2, column=1, columnspan=3, sticky='w', padx=10)

tk.Label(text="Итераций:", font=font_arial).grid(row=3, column=0, sticky='e', padx=10, pady=10)
label_n1 = tk.Label(font=font_arial)
label_n1.grid(row=3, column=1, columnspan=3, sticky='w')

tk.Label(text="Метод Зейделя", font=font_arial).grid(row=4, column=0, columnspan=4, sticky='we', padx=10, pady=10)

tk.Label(text="x\U00002081, x\U00002082, ... :", font=font_arial).grid(row=5, column=0, sticky='e', padx=10, pady=10)
entry_roots2 = tk.Entry(font=font_arial)
entry_roots2.grid(row=5, column=1, columnspan=3, sticky='w', padx=10)

tk.Label(text="Итераций:", font=font_arial).grid(row=6, column=0, sticky='e', padx=10, pady=10)
label_n2 = tk.Label(font=font_arial)
label_n2.grid(row=6, column=1, columnspan=3, sticky='w')

tk.Button(text="Вычислить", command=Calculate, font=font_arial).grid(row=7, column=0, columnspan=2, pady=10, padx=10,
                                                                     sticky='w')
tk.Button(text="Очистить", command=Clean, font=font_arial).grid(row=7, column=3, padx=10, sticky='e')

tk.mainloop()
