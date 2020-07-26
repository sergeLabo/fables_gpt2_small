#!python3

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator

file_name = "./loss.txt"
with open(file_name) as f:
    data = f.read()
f.close()

lines = data.splitlines()

x = []
loss = []
average = []

for line in lines:
    d_l = line.split(" ")
    x.append(int(d_l[0]))
    loss.append(float(d_l[2]))
    average.append(float(d_l[5]))

fig, ax = plt.subplots(1, 1, figsize=(8,8), facecolor='#cccccc')

ax.set_facecolor('#eafff5')
ax.set_title('Fables avec tf_gpt2="124M" et VOCAB_SIZE = 50257', size=18, color='magenta')

ax.set_ylim(0, 12)

ax.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)

ax.set_xlabel('Steps (number)', color='coral', size=20)
ax.set_ylabel('Loss', color='coral', size=20)

l = ax.plot(x, loss,
            linestyle=(0, (3, 5, 1, 5)),
            linewidth=1.5,
            color='red',
            label="Loss")

a = ax.plot(x, average,
            linestyle=(0, (5, 5)),
            linewidth=1.5,
            color='green',
            label="Average")

ax.axhline(y=0.1, xmin=0.0, xmax=1, color='r')

ax.text(0, 0.2, "Objectif = 0.1", weight='bold', color='blue')

ax.legend(loc="upper right", title="Efficiency")

fig.savefig("loss.png")
plt.show()
