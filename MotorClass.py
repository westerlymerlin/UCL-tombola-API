import minimalmodbus
import serial.serialutil
from datetime import datetime
from threading import Timer
from settings import settings, writesettings
from RPMClass import RPM


class Motor:
    def __init__(self):
        self.command_start_register = settings['control_offset'] - 40001
        self.query_start_register = settings['reading_offset'] - 40001
        try:
            self.controller = minimalmodbus.Instrument(settings['port'], settings['station'],
                                                       minimalmodbus.MODE_RTU)
            self.controller.serial.parity = minimalmodbus.serial.PARITY_EVEN
            self.controller.serial.baudrate = settings['baud']
            self.controller.serial.bytesize = settings['bytesize']
            self.controller.serial.stopbits = settings['stopbits']
            self.controller.serial.timeout = settings['timeout']
            self.controller.clear_buffers_before_each_transaction = settings['clear_buffers_before_call']
            self.controller.close_port_after_each_call = settings['clear_buffers_after_call']
        except serial.serialutil.SerialException:
            print('MotorClass: Error - no controller connected, please check RS485 port address is correct')
        self.read_length = settings['read_length']
        self.direction = 0  # 0 = forward, 1 = reverse
        self.frequency = 0  # 0 - 100%
        self.running = 0  # O = disabled 1 = enabled
        self.autoshutdown = settings['autoshutdown']
        self.autoshutdowntime = settings['shutdowntime']
        self.rpm = RPM()
        self.auto_stop_timer()

    def forward(self, speed):
        self.direction = 0
        self.frequency = speed
        self.running = 1
        try:
            self.controller_command([self.frequency, self.running, self.direction, 1])
        except AttributeError:
            print('MotorClass: forward function error No RS483 Controller')
        except minimalmodbus.NoResponseError:
            print('MotorClass: forward function error RS485 timeout')
        print('Tombola Command: Forward %s Hz' % speed)

    def reverse(self, speed):
        self.direction = 1
        self.frequency = speed
        self.running = 1
        try:
            self.controller_command([self.frequency, self.running, self.direction, 1])
        except AttributeError:
            print('MotorClass: reverse function error No RS483 Controller')
        except minimalmodbus.NoResponseError:
            print('MotorClass: reverse function error RS485 timeout')
        print('Tombola Command: Reverse %s Hz' % speed)

    def stop(self):
        self.direction = 0
        self.frequency = 0
        self.running = 0
        try:
            self.controller_command([self.frequency, self.running, self.direction, 0])
        except AttributeError:
            print('MotorClass: stop function error No RS483 Controller')
        except minimalmodbus.NoResponseError:
            print('MotorClass: stop function error RS485 timeout')
        print('Tombola Command: STOP')

    def controller_command(self, message):
        self.controller.write_registers(self.command_start_register, message)
        self.controller.serial.close()

    def controller_query(self):
        try:
            data = self.controller.read_registers(self.query_start_register, self.read_length, 3)
            self.controller.serial.close()
            return {'running': running(self.running), 'reqdirection': direction(self.direction),
                    'reqfrequency': self.frequency, 'direction': direction(data[10]), 'frequency': data[0],
                    'voltage': data[9], 'current': data[2], 'rpm': data[1], 'tombola_speed': self.rpm.get_rpm()}
        except AttributeError:   # RS485 not plugged in
            print('Tombola Error: RS485 controller is not working or not plugged in')
            return {'running': running(self.running), 'reqdirection': direction(self.direction),
                    'reqfrequency': self.frequency, 'direction': 'No RS485 Controller',
                    'frequency': 'No RS485 Controller', 'voltage': 'No RS485 Controller',
                    'current': 'No RS485 Controller', 'rpm': 'No RS485 Controller', 'tombola_speed': self.rpm.get_rpm()}
        except minimalmodbus.NoResponseError:
            print('Tombola Error: No response from the V20 controller, check it is powered on and connected')
            return {'running': running(self.running), 'reqdirection': direction(self.direction),
                    'reqfrequency': self.frequency, 'direction': 'RS485 Timeout',
                    'frequency': 'RS485 Timeout', 'voltage': 'RS485 Timeout',
                    'current': 'RS485 Timeout', 'rpm': 'RS485 Timeout', 'tombola_speed': self.rpm.get_rpm()}

    def print_controlword(self):
        data = self.controller.read_register(99, 0, 3)
        self.controller.serial.close()
        print(data)

    def write_register(self, reg, controlword):
        self.controller.write_register(reg, controlword)
        self.controller.serial.close()

    def set_stop_time(self, autostop, stoptime):
        if time_format_check(stoptime):
            self.autoshutdown = autostop
            settings['autoshutdown'] = autostop
            self.autoshutdowntime = stoptime
            settings['shutdowntime'] = stoptime
            writesettings()

    def get_stop_time(self):
        return {'autostop': self.autoshutdown, 'stoptime': self.autoshutdowntime}

    def auto_stop_timer(self):
        timerthread = Timer(1, self.auto_stop_timer)
        timerthread.start()
        if self.autoshutdown and self.running:
            stoptime = datetime.strptime(datetime.now().strftime('%d/%m/%Y ') +
                                         self.autoshutdowntime, '%d/%m/%Y %H:%M:%S')
            # print(stoptime)
            if stoptime < datetime.now():
                self.stop()

    def parse_control_message(self, message):
        if 'stop' in message.keys():
            self.stop()
        if 'forward' in message.keys():
            self.forward(message['forward'])
        if 'reverse' in message.keys():
            self.reverse(message['reverse'])
        if 'register' in message.keys():
            self.write_register(message['register'], message['word'])
        elif 'setfreq' in message.keys():
            if int(message['setfreq']) > 0:
                self.forward(int(message['setfreq']))
        elif 'stoptime' in message.keys():
            if 'autostop' in message.keys():
                self.set_stop_time(True, message['stoptime'])
            else:
                self.set_stop_time(False, message['stoptime'])
        elif 'frequency' in message.keys():
            speed = int(message['frequency'])
            if speed == 0:
                self.stop()
            else:
                self.forward(message['frequency'])
        else:
            print('message recieved = %s' % message)  # used for debugging HTML Forms
        print('Settings updated via web application')
        return self.controller_query()


def direction(value):
    if value == 1:
        return 'Reverse'
    else:
        return 'Forward'


def running(value):
    if value == 1:
        return 'Running'
    else:
        return 'Stopped'


def time_format_check(value):
    try:
        datetime.strptime(value, '%H:%M:%S')
        return True
    except ValueError:
        return False


if __name__ == '__main__':  # used for standlone testing
    tom = Motor()
