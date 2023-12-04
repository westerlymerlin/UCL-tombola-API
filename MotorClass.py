import minimalmodbus
import serial.serialutil
from datetime import datetime
from threading import Timer
from settings import settings, writesettings
from RPMClass import RPM
from logmanager import logger


class Motor:
    def __init__(self):
        self.register_offset = settings['register_offset']
        self.command_start_register = settings['control_offset'] - self.register_offset
        self.stw_control_register = settings['STW_register'] - self.register_offset
        self.query_start_register = settings['reading_offset'] - self.register_offset
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
            logger.info('MotorClass RS485 controller setup with modbus')
        except serial.serialutil.SerialException:
            logger.error('MotorClass: init Error - no controller connected, please check RS485 port address is correct')
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
            logger.error('MotorClass: forward function error No RS483 Controller')
        except minimalmodbus.NoResponseError:
            logger.error('MotorClass: forward function error RS485 timeout')
        logger.info('Tombola Command: Forward %s Hz' % speed)

    def reverse(self, speed):
        self.direction = 1
        self.frequency = speed
        self.running = 1
        try:
            self.controller_command([self.frequency, self.running, self.direction, 1])
        except AttributeError:
            logger.error('MotorClass: reverse function error No RS483 Controller')
        except minimalmodbus.NoResponseError:
            logger.error('MotorClass: reverse function error RS485 timeout')
        logger.info('Tombola Command: Reverse %s Hz' % speed)

    def stop(self):
        self.direction = 0
        self.frequency = 0
        self.running = 0
        try:
            self.controller_command([self.frequency, self.running, self.direction, 0])
        except AttributeError:
            logger.error('MotorClass: stop function error No RS483 Controller')
        except minimalmodbus.NoResponseError:
            logger.error('MotorClass: stop function error RS485 timeout')
        logger.info('Tombola Command: STOP')

    def controller_command(self, message):
        self.controller.write_registers(self.command_start_register, message)
        self.controller.serial.close()

    def controller_query(self):
        try:
            actual_data = self.controller.read_registers(self.query_start_register, self.read_length, 3)
            setting_data = self.controller.read_registers(self.command_start_register, 4, 3)
            self.controller.serial.close()
            return {'running': running(self.running), 'reqdirection': direction(self.direction),
                    'reqfrequency': setting_data[0] / 100, 'direction': direction(setting_data[2]),
                    'frequency': actual_data[0] / 100, 'voltage': actual_data[9], 'current': actual_data[2] / 100,
                    'rpm': actual_data[1], 'tombola_speed': self.rpm.get_rpm()}
        except AttributeError:   # RS485 not plugged in
            logger.error('Tombola Query Error: RS485 controller is not working or not plugged in')
            return {'running': running(self.running), 'reqdirection': direction(self.direction),
                    'reqfrequency': self.frequency / 100, 'direction': 'No RS485 Controller',
                    'frequency': 'No RS485 Controller', 'voltage': 'No RS485 Controller',
                    'current': 'No RS485 Controller', 'rpm': 'No RS485 Controller', 'tombola_speed': self.rpm.get_rpm()}
        except minimalmodbus.NoResponseError:
            logger.error('Tombola Query Error: No response from the V20 controller, check it is powered on and connected')
            return {'running': running(self.running), 'reqdirection': direction(self.direction),
                    'reqfrequency': self.frequency / 100, 'direction': 'RS485 Timeout',
                    'frequency': 'RS485 Timeout', 'voltage': 'RS485 Timeout',
                    'current': 'RS485 Timeout', 'rpm': 'RS485 Timeout', 'tombola_speed': self.rpm.get_rpm()}

    def print_controlword(self):
        data = self.controller.read_register(99, 0, 3)
        self.controller.serial.close()
        logger.info('Motorclass: read control word: %s' % data)

    def read_register(self, reg):
        try:
            data = self.controller.read_register(reg, 0, 3)
            self.controller.serial.close()
            logger.info('Motor Class read registry: Registry %s. Word %s' % (reg, data))
            return {'register': reg, 'word': data}
        except AttributeError:
            logger.error('MotorClass: read_register function error No RS483 Controller')
            return {'register': reg, 'word': 'No RS485 Controller'}
        except minimalmodbus.NoResponseError:
            logger.error('MotorClass: read_register function error RS485 timeout')
            return {'register': reg, 'word': 'RS485 Timeout'}

    def write_register(self, reg, controlword):
        try:
            self.controller.write_register(reg, controlword)
            self.controller.serial.close()
            logger.info('Motor Class write registry: Registry %s. Word %s' % (reg, controlword))
        except AttributeError:
            logger.error('MotorClass: write_register function error No RS483 Controller')
        except minimalmodbus.NoResponseError:
            logger.error('MotorClass: write_register function error RS485 timeout')

    def set_stop_time(self, autostop, stoptime):
        if time_format_check(stoptime):
            self.autoshutdown = autostop
            settings['autoshutdown'] = autostop
            self.autoshutdowntime = stoptime
            settings['shutdowntime'] = stoptime
            logger.info('Motor Class: Write settings')
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
        elif 'forward' in message.keys():
            self.forward(message['forward'])
        elif 'reverse' in message.keys():
            self.reverse(message['reverse'])
        elif 'reset' in message.keys():
            self.write_register(self.stw_control_register, settings['STW_forward'])
        elif 'write_register' in message.keys():
            self.write_register(message['write_register'] - self.register_offset, message['word'])
        elif 'read_register' in message.keys():
            return self.read_register(message['read_register'] - self.register_offset)
        elif 'rpm_data' in message.keys():
            return self.rpm.timequeue
        elif 'rpm' in message.keys():
            return {'rpm': self.rpm.get_rpm()}
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
            logger.info('message recieved = %s' % message)  # used for debugging HTML Forms
        logger.info('Settings updated via web application')
        return self.controller_query()


def direction(value):
    if value == 1:
        return 'Reverse'
    elif value == 0:
        return 'Forward'
    else:
        return value


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
