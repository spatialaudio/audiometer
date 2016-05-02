"""Familiarization. """

start_level = -40  # dB
decrease_20db = 20  # dB
increase_10db = 10  # dB


def fam(ctrl, freq, earside):
    click = ctrl._process(freq, start_level, earside)
    current_level = start_level

    while not click:  # increasing tone
        current_level += increase_10db
        click = ctrl._process(freq, current_level, earside)
    while click:  # decreasing tone
        current_level -= decrease_20db
        click = ctrl._process(freq, current_level, earside)

    ctrl._save_results(current_level, freq, earside, 'Familiarization')

    return current_level