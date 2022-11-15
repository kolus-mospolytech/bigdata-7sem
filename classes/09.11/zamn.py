import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("input/moons.csv")
print(df)
print(df.shape)
plt.figure()
plt.scatter(df['x1'], df['x2'], c=df['label'], cmap='rainbow')
plt.axis('equal')
plt.title("Model data")
plt.xlabel("x1")
plt.ylabel("x2")
plt.show()
