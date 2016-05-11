"""Familiarization. """


def fam(ctrl, freq, increase_10db, decrease_20db, start_level_familiar,
        earside):
    click = ctrl.process(freq, start_level_familiar, earside)
    current_level = start_level_familiar

    while not click:
        current_level += increase_10db
        click = ctrl.process(freq, current_level, earside)
    while click:
        current_level -= decrease_20db
        click = ctrl.process(freq, current_level, earside)

    return current_level