import pandas as pd
from matplotlib import pyplot as plt 

df = pd.read_csv("data.csv")
for i in range(10):
    plt.plot(df[str(i)])

plt.grid()
plt.ylim(0,10)
plt.xlabel("Steps")
plt.ylabel("No of Workers")
plt.savefig("plot_of_pants_over_time.jpg")
plt.show()