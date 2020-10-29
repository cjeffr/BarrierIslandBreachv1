import numpy as np
import matplotlib.pyplot as plt


length = 24
radius = 6
mu = 0
sigma = 5
# x = np.arange(length)
# y = np.sqrt(radius**2-(x-(length/2))**2)
x = np.linspace(-10, 10, 100)
den = 1 / (sigma * np.sqrt(2*np.pi))
expo = np.exp((-1/2)*(((x - mu)/sigma)**2))
print(expo)
y =  expo/den
y = np.nan_to_num(y)
plt.plot(x, y)
plt.show()