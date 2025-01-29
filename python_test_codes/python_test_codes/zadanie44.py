import numpy as np
import sys
def eliminacja_gaussa(a):
    n = len(a)
    x = np.zeros(n)
    ratio = 0
    for i in range(n):
        if a[i][i] == 0.0:
            sys.exit("Wykryto dzielenie przez zero")
        for j in range(i+1,n):
            ratio = a[j][i]/a[i][i]
            for k in range(n+1):
                a[j][k] = a[j][k] - (ratio*a[i][k])
    x[n-1] = a[n-1][n]/a[n-1][n-1]
    for i in range(n-1,-1,-1):
        x[i] = a[i][n]
        for j in range(i+1,n):
            x[i] = x[i] - (a[i][j]*x[j])
        x[i] = x[i]/a[i][i]
    for i in range(n):
        print("x" + str(i+1) + " = " + str(x[i]))


macierz = [
    [2, -1, 1, 8],
    [-3, -2, 1, -11],
    [-2, 1, 2, -3]
]

eliminacja_gaussa(macierz)



