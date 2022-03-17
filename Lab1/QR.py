import tkinter as tk
import tkinter.font as tkFont
import numpy as np
import math

a = [
    [-4, -6, -3],
    [-1, 5, -5],
    [6, 2, 5]
]

'''
-4 -6 -3
-1 5 -5
6 2 5
'''

# a = [
#     [1, 3, 1],
#     [1, 1, 4],
#     [4, 3, 1]
# ]

eps = 0.001


def sign(x):
    if x > 0:
        return 1
    if x == 0:
        return 0
    return -1


def norma(vector):
    return math.sqrt(sum([i*i for i in vector]))


def Householder(arr):
    A = np.array(arr)
    n = len(A)

    H = []
    for i in range(n - 1):
        v = [A[j][i] if j >= i else 0 for j in range(n)]
        v[i] = A[i][i] + sign(A[i][i])*norma(A[i:, i])

        v = np.array(v)
        # print('v:', v, sep='\n')

        vt = v.reshape(len(v), 1)
        v = v.reshape(1, len(v))

        h = np.eye(n) - 2 * np.dot(vt, v)/np.dot(v, vt)
        H.append(h)
        A = np.dot(h, A)
        # print('h:', h, 'A:', A, sep='\n')

    Q = H[0]
    for i in range(1, len(H)):
        Q = np.dot(Q, H[i])

    return Q, A


def complex_root(A, j):
    return (A[j][j] + A[j + 1][j + 1]) / 2, math.sqrt(
        math.fabs((A[j][j] + A[j + 1][j + 1]) ** 2 / 4 + A[j][j + 1] * A[j + 1][j] - A[j][j] * A[j + 1][j + 1]))


def QR(arr, eps):
    A = np.array(arr)

    n = len(A)
    i = 0
    j = 1

    while math.sqrt(sum([A[i][j]**2 for i in range(n) for j in range(0, i)])) > eps:
        q, r = Householder(A)
        # print('Q:', q, 'R:', r, sep='\n')
        re00, im00 = complex_root(A, 0)
        re01, im01 = complex_root(A, 1)

        A = np.dot(r, q)

        re10, im10 = complex_root(A, 0)
        re11, im11 = complex_root(A, 1)

        if math.sqrt((re10 - re00)**2 + (im10 - im00)**2) < eps:
            break
        if math.sqrt((re11 - re01)**2 + (im11 - im01)**2) < eps:
            break

        # print('A:', a)
        # print(i)
        i += 1

    if math.sqrt(sum([A[i][j]**2 for i in range(n) for j in range(0, i)])) < eps:
        print(A)
        print((A[k][k] for k in range(n)))
        return (A[k][k] for k in range(n)), i

    a = 0
    if math.fabs(A[1][0]) < eps * 10:
        a = A[0][0]
        j = 1
    else:
        a = A[2][2]
        j = 0

    re, im = complex_root(A, j)

    print(A)
    print(a, complex(re, im), complex(re, -im))
    a = round(a, 4)
    im = round(im, 4)
    re = round(re, 4)
    return (a, complex(re, im), complex(re, -im)), i


def Calculate():
    arr = [list(map(float, i.split())) for i in table_coefs.get('1.0', tk.END).split('\n')]
    eps = float(table_eps.get())

    while (len(arr[len(arr) - 1])) == 0:
        arr.pop()

    lamdas, n = QR(arr, eps)
    ans = ''

    for l in lamdas:
        ans += str(l) + ' '


    entry_roots.delete(0, tk.END)
    entry_roots.insert(0, ans)
    label_n['text'] = str(n)


def Clean():
    table_coefs.delete('1.0', tk.END)
    table_eps.delete(0, tk.END)
    entry_roots.delete(0, tk.END)
    label_n['text'] = ''


window = tk.Tk()
window.title('QR алгоритм для нахождения собственных значений')

font_arial = tkFont.Font(family="Arial", size=14)

tk.Label(text="A =", font=font_arial).grid(row=0, column=0, sticky='e', pady=10, padx=10)
table_coefs = tk.Text(width=35, height=10, font=font_arial)
table_coefs.grid(row=0, column=1, columnspan=3, sticky='w', padx=10)

tk.Label(text="eps =", font=font_arial).grid(row=1, column=0, sticky='e', pady=10, padx=10)
table_eps = tk.Entry(font=font_arial, width=35)
table_eps.grid(row=1, column=1, columnspan=3, sticky='w', padx=10)

tk.Label(text="λ\U00002081, λ\U00002082, ... :", font=font_arial).grid(row=5, column=0, sticky='e', padx=10, pady=10)
entry_roots = tk.Entry(font=font_arial, width=35)
entry_roots.grid(row=5, column=1, columnspan=3, sticky='w', padx=10)

tk.Label(text="Итераций:", font=font_arial).grid(row=6, column=0, sticky='e', padx=10, pady=10)
label_n = tk.Label(font=font_arial)
label_n.grid(row=6, column=1, columnspan=3, sticky='w')

tk.Button(text="Вычислить", command=Calculate, font=font_arial).grid(row=7, column=0, columnspan=2, pady=10, padx=10, sticky='w')
tk.Button(text="Очистить", command=Clean, font=font_arial).grid(row=7, column=3, padx=10, sticky='e')

tk.mainloop()
