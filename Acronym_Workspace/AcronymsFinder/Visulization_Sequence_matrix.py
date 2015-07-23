__author__ = 'HongDing'
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

n=26

data = pd.read_csv('sequence_matrix.csv',index_col=0)

ax = plt.imshow(data, interpolation='nearest', cmap='Reds').get_axes()
ax.set_xticks(np.linspace(0, n-1, n))
ax.set_yticks(np.linspace(0, n-1, n))


ax.set_xticklabels(data.columns)
ax.set_yticklabels(data.index)

ax.grid('off')
ax.xaxis.tick_top()

plt.tick_params(
    axis='both',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    left='off',
    right='off',
    labelbottom='off') # labels along the bottom edge are off

plt.savefig('sequence_matrix_visualization.pdf')