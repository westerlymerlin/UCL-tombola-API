"""
Settings module, reads the settings from a settings.json file. If it does not exist or a new setting
has appeared it will creat from the defaults in the initialise function.
Author: Gary Twinn
"""

import json
from datetime import datetime


VERSION = '1.7.3'


def writesettings():
    """Write settings to json file"""
    settings['LastSave'] = datetime.now().strftime('%d/%m/%y %H:%M:%S')
    with open('settings.json', 'w', encoding='UTF-8') as outfile:
        json.dump(settings, outfile, indent=4, sort_keys=True)


def initialise():  # Default values written to the settings.json file the first time the app is run
    """Setup the settings structure with default values"""
    isettings = {'LastSave': '01/01/2000 00:00:01',
                 'STW_forward': 1142,
                 'STW_register': 99,
                 'STW_stop': 0,
                 'api-key': '<APIKEY$>',
                 'autoshutdown': True,
                 'baud': 9600,
                 'bytesize': 8,
                 'clear_buffers_after_call': True,
                 'clear_buffers_before_call': True,
                 'control_start_register': 2,
                 'cputemp': '/sys/class/thermal/thermal_zone0/temp',
                 'database_path': './database/',
                 'gunicornpath': './logs/',
                 'logappname': 'Tombola-Py',
                 'logfilepath': './logs/tombola.log',
                 'loglevel': 'INFO',
                 'port': '/dev/ttyUSB0',
                 'read_length': 16,
                 'reading_start_register': 23,
                 'rpm_active_LED': 17,
                 'rpm_frequency': 11.91,
                 'rpm_magnets': 48,
                 'rpm_max': 99.9,
                 'rpm_sensor_GPIO': 27,
                 'rpm_timeout_seconds': 2,
                 'shutdowntime': '08:00:00',
                 'station': 1,
                 'stopbits': 1,
                 'syslog': '/var/log/syslog',
                 'serialtimeout': 0.75}
    return isettings


def readsettings():
    """Read the json file"""
    try:
        with open('settings.json', encoding='UTF-8') as json_file:
            jsettings = json.load(json_file)
            return jsettings
    except FileNotFoundError:
        print('File not found')
        return {}


def loadsettings():
    """Replace the default settings with thsoe from the json files"""
    global settings
    settingschanged = 0
    fsettings = readsettings()
    for item in settings.keys():
        try:
            settings[item] = fsettings[item]
        except KeyError:
            print(f'settings[{item}] Not found in json file using default')
            settingschanged = 1
    if settingschanged == 1:
        writesettings()


settings = initialise()
loadsettings()
