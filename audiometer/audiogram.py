"""Audiogram."""

import numpy as np
import csv
import matplotlib.pyplot as plt


def set_audiogram_parameters(dBHL, freqs, conduction, masking, earside,
                             ax=None, **kwargs):
    """Set measuring points.

    Parameters
    ----------
    dBHL : array_like
          dB(HearingLevel)
    freqs : array_like
          Frequency Vector in Hz
    ax: plt.Ax, optional
          Matplotlib Ax to plot on
    earside: str, default='left'
          'left' or 'right' ear
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
    xticks = np.arange(len(freqs))
    ax.set_xlabel("f / Hz")
    ax.set_ylabel('Sound Intensity / dBHL')
    ax.set_xlim([-0.5, xticks[-1] + 0.5])
    ax.set_ylim([-20, 120])
    plt.setp(ax, xticks=xticks, xticklabels=sorted(freqs))
    major_ticks = np.arange(-20, 120, 10)
    minor_ticks = np.arange(-20, 120, 5)
    ax.set_yticks(major_ticks)
    ax.set_yticks(minor_ticks, minor=True)
    ax.grid(which='both')
    ax.invert_yaxis()
    ax.tick_params(axis='x', labelsize=6.5)
    ax.tick_params(axis='y', labelsize=6.5)
    #  one octave on the frequency axis shall correspond
    #  to 20 dB on the hearing level axis (ISO 8253-1 (2011) ch. 10)
    ax.set_aspect(0.9 / ax.get_data_ratio())
    ax.set_title('Hearing Level - {} ear'.format(earside))
    if earside == 'left':
        color = 'b'
        if conduction == 'air' and masking == 'off':
            marker = 'x'
        elif conduction == 'air' and masking == 'on':
                marker = 's'
        elif conduction == 'bone' and masking == 'off':
                marker = '4'
        elif conduction == 'bone' and masking == 'on':
                marker = '*'
        else:
            raise NameError("Conduction has to be 'air' or 'bone'")
    elif earside == 'right':
        color = 'r'
        if conduction == 'air' and masking == 'off':
            marker = 'o'
        elif conduction == 'air' and masking == 'on':
            marker = '^'
        elif conduction == 'bone' and masking == 'off':
            marker = '3'
        elif conduction == 'bone' and masking == 'on':
            marker = '8'
        else:
            raise NameError("Conduction has to be 'air' or 'bone'")
    elif not earside == 'right' or not earside == 'left':
        raise NameError("'left' or 'right'?")
    lines = ax.plot(dBHL, color=color, marker=marker, markersize=5,
                    markeredgewidth=1, fillstyle='none')
    gridlines = ax.get_xgridlines() + ax.get_ygridlines()
    for line in gridlines:
        line.set_linestyle('-')
    return lines


def make_audiogram(filename, results_path=None):

        if results_path is None:
            results_path = 'audiometer/results'
        data = _read_audiogram(filename)
        conduction = [option for cond, option, none in data
                      if cond == 'Conduction'][0]
        masking = [option for mask, option, none in data
                   if mask == 'Masking'][0]

        if 'right' in [side for freq, level, side in data] and (
           'left' in [side for freq, level, side in data]):
            f, (ax1, ax2) = plt.subplots(ncols=2)
        else:
            ax1, ax2 = None, None
            f = plt.figure()

        if 'right' in [side for freq, level, side in data]:
            dBHL, freqs = _extract_parameters(data, 'right')
            set_audiogram_parameters(dBHL, freqs, conduction, masking,
                                     earside='right', ax=ax1)

        if 'left' in [side for freq, level, side in data]:
            dBHL, freqs = _extract_parameters(data, 'left')
            set_audiogram_parameters(dBHL, freqs, conduction, masking,
                                     earside='left', ax=ax2)

        f.savefig('{}{}.pdf'.format(results_path, filename))


def _read_audiogram(filename):
    with open('audiometer/results/{}'.format(filename), 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = [data for data in reader]
    return data


def _extract_parameters(data, earside):
    parameters = sorted((float(freq), float(level)) for level, freq, side
                        in data if side == earside)
    dBHL = [level for freq, level in parameters]
    freqs = [int(freq) for freq, level in parameters]
    return dBHL, freqs
