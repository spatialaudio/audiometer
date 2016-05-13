import argparse


class Config():

    def __init__(self):

        parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
        parser.add_argument("-device", help='How to select your soundcard is '
        'shown in http://python-sounddevice.readthedocs.org/en/0.3.3/'
        '#sounddevice.query_devices', type=int, default=0)
        parser.add_argument("-calibration_factor", type=int, default=1)
        parser.add_argument("-responder_device", type=str,
                            default="mouse left down")
        parser.add_argument("-attack", type=int, default=30)
        parser.add_argument("-release", type=int, default=40)
        parser.add_argument("-timeout", type=int, default=2)
        parser.add_argument("-earside", type=str, default="right")
        parser.add_argument("-small_level_increment", type=int, default=5)
        parser.add_argument("-large_level_increment", type=int, default=10)
        parser.add_argument("-small_level_decrement", type=int, default=10)
        parser.add_argument("-large_level_decrement", type=int, default=20)
        parser.add_argument("-start_level_familiar", type=int, default=-40)
        parser.add_argument("-freqs", type=str, default='1000,1500,2000,3000,'
                            '4000,6000,8000,750,500,250,125')
        try:
            args = parser.parse_args(['@config.txt'])
        except:
            print("No Config found! Using default values")
            with open('config_default.txt', 'w') as cfg:
                cfg.write('')
                args = parser.parse_args(['@config_default.txt'])

        self.device = args.device
        self.responder_device = args.responder_device
        self.attack = args.attack
        self.release = args.release
        self.timeout = args.timeout
        self.earside = args.earside
        self.small_level_increment = args.small_level_increment
        self.large_level_increment = args.large_level_increment
        self.small_level_decrement = args.small_level_decrement
        self.large_level_decrement = args.large_level_decrement
        self.start_level_familiar = args.start_level_familiar
        self.freqs = [int(i) for i in args.freqs.split(',')]