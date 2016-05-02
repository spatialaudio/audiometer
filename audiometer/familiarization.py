"""Familiarization. """


def fam(ctrl, freq, earside):
    start_level = -40  # dB
    decreasing_tone_fam = 20  # dB
    increasing_tone_fam = 10  # dB
    click = ctrl._process(freq, start_level, earside)
    current_level = start_level

    while not click:  # increasing tone
        current_level += increasing_tone_fam
        click = ctrl._process(freq, current_level, earside)
    while click:  # decreasing tone
        current_level -= decreasing_tone_fam
        click = ctrl._process(freq, current_level, earside)

    ctrl._save_results(current_level, freq, earside, 'Familiarization')

    return current_level