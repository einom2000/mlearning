import matplotlib.pyplot as plt
import numpy as np

x = np.random.normal(170, 10, 250)

plt.hist(x)
plt.show()


y = np.array([35, 25, 25, 15])
mylabels = ["Apples", "Bananas", "Cherries", "Dates"]
mycolors = ["black", "hotpink", "b", "#4CAF50"]
myexplode = [0.2, 0, 0, 0]
plt.pie(y, labels=mylabels, startangle=90, explode=myexplode,
        shadow=True, colors=mycolors)
plt.legend(title = "Four Fruits:")
plt.show()