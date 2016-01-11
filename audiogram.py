"""Audiogram."""

import numpy as np
import matplotlib.pyplot as plt


def set_points(dBHL_values, freqs=None, ax=None, title=None, masking=False,
               conduction='air', **kwargs):
    """Set measuring points.

    Parameters
    ----------
    dBHL_values : array_like
          dBHL-Values Vector
    freqs : array_like, optional
          Frequency Vector in Hz
    ax: plt.Ax, optional
          Matplotlib Ax to plot on
    title: str, optional
          Audiogram Title
    masking: bool, default=False
          Masked or unmasked hearing test
    conduction: str, default='air'
          Air conduction is 'air' and bone conduction is 'bone'
    Returns
    -------
    plt.Axis
        Matplotlib axis containing the plot.

    """
    if ax is None:
        ax = plt.gca()
    if freqs is None:
        # standard test frequencies DIN EN IEC 60645-1 ch. 6.1.1.1 Tab.2
        freqs = [125, 250, 500, 1000, 2000, 4000, 8000]
    if len(dBHL_values) != len(freqs):
        raise ValueError("dBHL_values and freqs must have the same length")
    xticks = np.arange(len(freqs))
    ax.set_xlabel("f / Hz")
    ax.set_ylabel('Sound Intensity / dBHL')
    ax.set_xlim([-0.5, xticks[-1] + 0.5])
    ax.set_ylim([-10, 120])
    plt.setp(ax, xticks=xticks,
             xticklabels=freqs,
             yticks=[-10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
                     110, 120])
    ax.invert_yaxis()
    if title is not None:
        ax.set_title(title)
        if title == 'Left Ear':
            color = 'b'
            if conduction == 'air' and masking is False:
                marker = 'x'
            elif conduction == 'air' and masking is True:
                marker = 's'
            elif conduction == 'bone' and masking is False:
                marker = '4'
            elif conduction == 'bone' and masking is True:
                marker = '*'
            else:
                raise NameError("Conduction has to be 'air' or 'bone'")
        elif title == 'Right Ear':
            color = 'r'
            if conduction == 'air' and masking is False:
                marker = 'o'
            elif conduction == 'air' and masking is True:
                marker = '^'
            elif conduction == 'bone' and masking is False:
                marker = '3'
            elif conduction == 'bone' and masking is True:
                marker = '8'
            else:
                raise NameError("Conduction has to be 'air' or 'bone'")
        else:
            raise NameError("'Left Ear' or 'Right Ear'?")
    else:
        color = 'k'
        marker = 'p'
    ax.plot(dBHL_values, color=color, marker=marker, markersize=11,
            markeredgewidth=1, fillstyle='none')
    ax.grid(True)
    gridlines = ax.get_xgridlines() + ax.get_ygridlines()
    for line in gridlines:
        line.set_linestyle('-')
    return ax


# A short script to test the audiogram

dBHL_values = [30, 50, 80, 75, 84, 50, 40]
set_points(dBHL_values, title='Right Ear')
plt.show()
