import json
import datetime

version = '0.0.1'


def friendlydirname(sourcename):
    sourcename = sourcename.replace('/', '-')
    sourcename = sourcename.replace('\\', '-')
    sourcename = sourcename.replace(':', '-')
    sourcename = sourcename.replace('*', '-')
    sourcename = sourcename.replace('?', 'Q')
    sourcename = sourcename.replace('<', '-')
    sourcename = sourcename.replace('>', '-')
    sourcename = sourcename.replace('"', '-')
    sourcename = sourcename.replace('&', '-')
    sourcename = sourcename.replace('%', '-')
    sourcename = sourcename.replace('#', '-')
    sourcename = sourcename.replace('$', '-')
    sourcename = sourcename.replace("'", '-')
    sourcename = sourcename.replace(',', '.')
    sourcename = sourcename.replace('--', '-')
    sourcename = sourcename.replace('--', '-')
    sourcename = sourcename.replace('--', '-')
    return sourcename


def writesettings():
    settings['LastSave'] = datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')
    with open('settings.json', 'w') as outfile:
        json.dump(settings, outfile, indent=4, sort_keys=True)


def initialise():
    isettings = {}
    isettings['LastSave'] = '01/01/2000 00:00:01'
    isettings['port'] = '/dev/ttyUSB0'
    isettings['baud'] = 9600
    isettings['bytesize'] = 8
    isettings['stopbits'] = 1
    isettings['timeout'] = 0.5
    isettings['station'] = 10
    isettings['clear_buffers_before_call'] = True
    isettings['clear_buffers_after_call'] = True
    isettings['control_offset'] = 40005
    isettings['reading_offset'] = 40009
    isettings['read_length'] = 8
    return isettings
    # writesettings()


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
            # print('settings[%s] = %s' % (item, settings[item]))
        except KeyError:
            print('settings[%s] Not found in json file using default' % item)


settings = initialise()
loadsettings()
