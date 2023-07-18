import pandas as pd
from world import world
from matplotlib import pyplot as plt 
import openai
from tqdm import tqdm

openai.api_key = "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"
loaded_lists = []
for i in tqdm(range(10)):
    print(f"-------Run - {i+1}--------")
    model = world(no_workers= 10, no_days= 20, init_pants=i,manager=True,static=True)
    model.run()
    loaded_lists.append(model.pants_over_time)

df = pd.DataFrame(loaded_lists)
df = df.T
df.to_csv("data.csv")
print("===========ALL DONE============")

df = pd.read_csv("data.csv")
for i in range(10):
    plt.plot(df[str(i)])

plt.grid()
plt.ylim(0,10)
plt.xlabel("Steps")
plt.ylabel("No of Workers")
plt.savefig("plot_of_pants_over_time.jpg")
plt.show()
