import json
import datetime


version = '1.0.2'


def writesettings():
    settings['LastSave'] = datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')
    with open('settings.json', 'w') as outfile:
        json.dump(settings, outfile, indent=4, sort_keys=True)


def initialise():
    isettings = {'LastSave': '01/01/2000 00:00:01', 'port': '/dev/ttyUSB0', 'baud': 9600, 'bytesize': 8, 'stopbits': 1,
                 'timeout': 1, 'station': 1, 'clear_buffers_before_call': True, 'clear_buffers_after_call': True,
                 'control_offset': 40003, 'reading_offset': 40024, 'read_length': 16,
                 'logfilepath': './logs/tombola.log', 'logappname': 'Tombola-Py', 'gunicornpath': './logs/',
                 'cputemp': '/sys/class/thermal/thermal_zone0/temp', 'syslog': '/var/log/syslog',
                 'shutdowntime': '23:59:59', 'autoshutdown': True}
    return isettings


def readsettings():
    try:
        with open('settings.json') as json_file:
            jsettings = json.load(json_file)
            return jsettings
    except FileNotFoundError:
        print('File not found')
        return {}


def loadsettings():
    global settings
    fsettings = readsettings()
    for item in settings.keys():
        try:
            settings[item] = fsettings[item]
        except KeyError:
            print('settings[%s] Not found in json file using default' % item)
            writesettings()


settings = initialise()
loadsettings()
