"""Familiarization. """


def fam(ctrl, freq, large_level_increment, large_level_decrement, start_level_familiar,
        earside):
    click = ctrl.process(freq, start_level_familiar, earside)
    current_level = start_level_familiar

    while not click:
        current_level += large_level_increment
        click = ctrl.process(freq, current_level, earside)
    while click:
        current_level -= large_level_decrement
        click = ctrl.process(freq, current_level, earside)

    return current_level