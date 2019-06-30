import os
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
time = np.linspace(0.0, 10.0, 10)
y = np.linspace(0.0, 60e3, 600)
x = np.linspace(-100, 100, 500)
X, Y = np.meshgrid(x, y)
t1 = 3.0
t2 = 6.0
A_max = 5.0
A1 = (  (time < t1) * np.zeros(time.shape)
      + (t1 <= time) * (time < t2) * (A_max / (t2-t1) * (time - t1))
      + (t2 <= time) * np.ones(time.shape) * A_max)
A2 = .2*y
sigma = 10.0
h0 = 10
x1 = -25.0
x2 = 25.0
mu = 1.0
breach = np.ones(X.shape) * h0
for i in range(len(A1)):
    breach -= A1[i] * np.exp(-X**2 / sigma**2) * (0.10 * Y)  * (x1 <= X) * (X <= x2)
    plt.clf()
    plt.figure()
    plt.pcolor(X, Y, breach, vmin=5, vmax=h0)
    plt.colorbar()
    plt.show()
fortran_file = os.path.join('c:/', 'fortranprograms', 'fortran_test.txt')
data = np.loadtxt(fortran_file)