import matplotlib.pyplot as plt
import numpy as np

# Create some data
data = [np.random.rand(10, 10) for _ in range(4)]

# Create the figure and subplots
fig, axes = plt.subplots(nrows=2, ncols=2)

# Create the heatmaps and color bars for each subplot
for ax, d in zip(axes.flat, data):
    heatmap = ax.imshow(d, cmap='coolwarm')
    colorbar = plt.colorbar(heatmap, ax=ax)

    # Set the x and y ticks
    ax.set_xticks(np.arange(len(d[0])))
    ax.set_yticks(np.arange(len(d)))
    ax.set_xticklabels(np.arange(len(d[0])))
    ax.set_yticklabels(np.arange(len(d)))

    # Add annotations
    for i in range(len(d)):
        for j in range(len(d[0])):
            ax.text(j, i, f'{d[i, j]:.2f}', ha='center', va='center', color='w')

# Show the plot
plt.show()