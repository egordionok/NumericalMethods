import tkinter as tk
import tkinter.font as tkFont
import numpy as np
import math

def sign(x):
    if x > 0:
        return 1
    if x == 0:
        return 0
    return -1

def QR(arr):
    n = len(arr)
    A = np.array(arr)
    v = np.array()
    v.append(A[0][0] + sign(A[0][0])*math.sqrt(sum([A[j][0]**2 for j in range(0, n)])))
    for i in range(1, n):
        v.append(A[i][0])

    H = np.eye(n) - 2 * np.dot(np.dot(v, v.T),np.invert(np.dot(v.T, v)))

