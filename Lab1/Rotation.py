import numpy as np
import tkinter as tk
import tkinter.font as tkFont
import math


def Rotation(arr, eps=0.1):
    A = np.array(arr)
    n = len(A)
    iterator = 0
    self_vectors = np.eye(len(A))
    while iterator < 1000000:
        iterator += 1
        # print(f"_________________ it {iterator} _________________")
        max_a = max([[math.fabs(A[i][j]), i, j] for i in range(n) for j in range(n) if i != j], key=lambda x: x[0])

        my_round = lambda x: round(x, 4)
        U = np.eye(n)
        a, i, j = max_a
        phi = 0.5 * math.atan((2 * a)/(A[i][i] - A[j][j])) if A[i][i] != A[j][j] else math.pi/4
        U[i][i] = math.cos(phi)
        U[j][j] = math.cos(phi)
        U[i][j] = -math.sin(phi)
        U[j][i] = math.sin(phi)

        self_vectors = np.dot(self_vectors, U)

        A = np.dot(np.dot(U.T, A), U)
        # print(A.round(2))
        # print()
        # print(U.round(2))

        if math.sqrt(sum([A[i][j]**2 for i in range(n) for j in range(i + 1, n)])) < eps:
            break

    return A, iterator, self_vectors


def Calculate():
    arr = [list(map(float, i.split())) for i in table_coefs.get('1.0', tk.END).split('\n')]
    eps = float(table_eps.get())

    while (len(arr[len(arr) - 1])) == 0:
        arr.pop()

    arr, n, self_vectors = Rotation(arr, eps)

    print(self_vectors)
    print()
    # print(arr)
    ans = ''
    for i in range(len(arr)):
        ans += str(round(arr[i][i], 4)) + ' '

    entry_roots.delete(0, tk.END)
    entry_roots.insert(0, ans)
    label_n['text'] = str(n)


def Clean():
    table_coefs.delete('1.0', tk.END)
    table_eps.delete(0, tk.END)
    entry_roots.delete(0, tk.END)
    label_n['text'] = ''


window = tk.Tk()
window.title('Метод вращений для нахождения собственных значений')

font_arial = tkFont.Font(family="Arial", size=14)

tk.Label(text="A =", font=font_arial).grid(row=0, column=0, sticky='e', pady=10, padx=10)
table_coefs = tk.Text(width=30, height=10, font=font_arial)
table_coefs.grid(row=0, column=1, columnspan=3, sticky='w', padx=10)

tk.Label(text="eps =", font=font_arial).grid(row=1, column=0, sticky='e', pady=10, padx=10)
table_eps = tk.Entry(font=font_arial, width=30)
table_eps.grid(row=1, column=1, columnspan=3, sticky='w', padx=10)

tk.Label(text="λ\U00002081, λ\U00002082, ... :", font=font_arial).grid(row=5, column=0, sticky='e', padx=10, pady=10)
entry_roots = tk.Entry(font=font_arial, width=30)
entry_roots.grid(row=5, column=1, columnspan=3, sticky='w', padx=10)

tk.Label(text="Итераций:", font=font_arial).grid(row=6, column=0, sticky='e', padx=10, pady=10)
label_n = tk.Label(font=font_arial)
label_n.grid(row=6, column=1, columnspan=3, sticky='w')

tk.Button(text="Вычислить", command=Calculate, font=font_arial).grid(row=7, column=0, columnspan=2, pady=10, padx=10, sticky='w')
tk.Button(text="Очистить", command=Clean, font=font_arial).grid(row=7, column=3, padx=10, sticky='e')

tk.mainloop()

# A = [
#     [8, 2, -1],
#     [2, -5, -8],
#     [-1, -8, -5]
# ]


'''
8 2 -1
2 -5 -8
-1 -8 -5
'''

# A = [
#     [4, 2, 1],
#     [2, 5, 3],
#     [1, 3, 6]
# ]

'''
4 2 1
2 5 3
1 3 6
'''