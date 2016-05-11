from configparser import ConfigParser
import itertools


def load():

    try:
        cfg = ConfigParser()
        with open('config.ini') as f:
            # http://stackoverflow.com/a/8555776
            cfg.read_file(itertools.chain(['[Parameters]'], f))  # Fake Section

    except EnvironmentError:
        with open('config_default.ini', 'w') as f_default:
            cfg.add_section('Parameters')
            cfg.set('Parameters', 'device', '0')
            cfg.set('Parameters', 'attack', '30')
            cfg.set('Parameters', 'release', '40')
            cfg.set('Parameters', 'responder_device', 'mouse left down')
            cfg.set('Parameters', 'timeout', '2')
            cfg.set('Parameters', 'earside', 'right')
            cfg.set('Parameters', 'calibration_factor', '1')
            cfg.set('Parameters', 'freqs', ('1000\n1500\n2000\n3000\n4000\n6000'
                                            '\n8000\n750\n500\n250\n125'))
            cfg.set('Parameters', 'increase_5db', '5')
            cfg.set('Parameters', 'increase_10db', '10')
            cfg.set('Parameters', 'decrease_10db', '10')
            cfg.set('Parameters', 'decrease_20db', '20')
            cfg.set('Parameters', 'start_level_familiar', '-40')

            cfg.write(f_default)

    finally:
            device = int(cfg['Parameters']['device'])
            attack = int(cfg['Parameters']['attack'])
            release = int(cfg['Parameters']['release'])
            timeout = int(cfg['Parameters']['timeout'])
            # http://stackoverflow.com/a/30223001
            freqs = [int(i) for i in cfg.get('Parameters', 'freqs').split('\n')]
            increase_5db = int(cfg['Parameters']['increase_5db'])
            increase_10db = int(cfg['Parameters']['increase_10db'])
            decrease_10db = int(cfg['Parameters']['decrease_10db'])
            decrease_20db = int(cfg['Parameters']['decrease_20db'])
            start_level_familiar = int(cfg['Parameters']['start_level_familiar'])
            earside = cfg['Parameters']['earside']
            responder_device = cfg['Parameters']['responder_device']

            return (device, attack, release, timeout, freqs, increase_5db,
                    increase_10db, decrease_10db, decrease_20db,
                    start_level_familiar, earside, responder_device)

