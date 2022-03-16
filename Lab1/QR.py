import tkinter as tk
import tkinter.font as tkFont
import numpy as np
import math

a = [
    [-4, -6, -3],
    [-1, 5, -5],
    [6, 2, 5]
]

# a = [
#     [1, 3, 1],
#     [1, 1, 4],
#     [4, 3, 1]
# ]


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


a = np.array(a)
n = len(a)
i = 0
while math.sqrt(sum([a[i][j]*a[i][j] for i in range(n) for j in range(n) if i > j])) > 0.001 and i < 1000:
    q, r = Householder(a)
    # print('Q:', q, 'R:', r, sep='\n')
    a = np.dot(r, q)
    # print('A:', a)
    print(i)
    i += 1

print(a)