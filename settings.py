import json
from datetime import datetime


version = '1.4.5'


def writesettings():
    settings['LastSave'] = datetime.now().strftime('%d/%m/%y %H:%M:%S')
    with open('settings.json', 'w') as outfile:
        json.dump(settings, outfile, indent=4, sort_keys=True)


def initialise():  # These are the default values written to the settings.json file the first time the app is run
    isettings = {'LastSave': '01/01/2000 00:00:01',
                 'STW_forward': 1142,
                 'STW_register': 99,
                 'STW_stop': 0,
                 'api-key': '57vZPotsJ1VvRlnRKLG4',
                 'autoshutdown': True,
                 'baud': 9600,
                 'bytesize': 8,
                 'cameraBrightness': 10,
                 'cameraContrast': 10,
                 'cameraFPS': 30,
                 'cameraHeight': 240,
                 'cameraID': 0,
                 'cameraWidth': 320,
                 'clear_buffers_after_call': True,
                 'clear_buffers_before_call': True,
                 'control_start_register': 2,
                 'cputemp': '/sys/class/thermal/thermal_zone0/temp',
                 'database_path': './database/',
                 'gunicornpath': './logs/',
                 'logappname': 'Tombola-Py',
                 'logfilepath': './logs/tombola.log',
                 'port': '/dev/ttyUSB0',
                 'read_length': 16,
                 'reading_start_register': 23,
                 'rpm_active_LED': 17,
                 'rpm_frequency': 11.91,
                 'rpm_magnets': 48,
                 'rpm_sensor_GPIO': 27,
                 'rpm_timeout_seconds': 2,
                 'shutdowntime': '08:00:00',
                 'station': 1,
                 'stopbits': 1,
                 'syslog': '/var/log/syslog',
                 'timeout': 1}
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
    settingschanged = 0
    fsettings = readsettings()
    for item in settings.keys():
        try:
            settings[item] = fsettings[item]
        except KeyError:
            print('settings[%s] Not found in json file using default' % item)
            settingschanged = 1
    if settingschanged == 1:
        writesettings()


settings = initialise()
loadsettings()
