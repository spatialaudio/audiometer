"""Audiogram."""

import numpy as np
import matplotlib.pyplot as plt


def set_points(dBHL_values, ax=None, title=None, **kwargs):
    if ax is None:
        ax = plt.gca()
    ax.set_xlabel("f / Hz")
    ax.set_ylabel('Sound Intensity (dBHL)')
    ax.set_xlim([-0.5, 6.5])
    ax.set_ylim([-10, 120])
    plt.setp(ax, xticks=[0, 1, 2, 3, 4, 5, 6],
             xticklabels=[125, 250, 500, 1000, 2000, 4000, 8000],
             yticks=[-10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
             110, 120])
    ax.invert_yaxis()
    color = 'k'
    if title is not None:
        ax.set_title(title)
        if title == 'Left Ear':
            color = 'b'
        elif title == 'Right Ear':
            color = 'r'
        else:
            raise NameError("'Left Ear' or 'Right Ear'?")
    ax.plot(dBHL_values, color=color, marker='x', markersize=11,
            markeredgewidth=1)
    ax.grid(True)
    return ax


# A short script to test the audiogram

dBHL_values = [30, 50, 80, 75, 84, 50, 40]

set_points(dBHL_values, title='Left Ear')
plt.show()
