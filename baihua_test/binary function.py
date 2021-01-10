import matplotlib.pyplot as plt
import numpy as np
import time

# create 1000 equally spaced points between -10 and 10
x = np.linspace(-50, 50, 10000)

# calculate the y value for each element of the x vector
y = (-1/3)*x**2 + (1/4)*x + 2
y1 = np.linspace(0,0,10000)
x1 = np.linspace(0,0,10000)
fig, ax = plt.subplots()
ax.plot(x, y)
ax.plot(x, y1)
ax.plot(x1,y)

plt.show()

