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
            self.controller = minimalmodbus.Instrument(settings['port'], settings['station'], minimalmodbus.MODE_RTU)
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
        self.rpm_hz = settings['rpm_frequency']
        self.requested_rpm = 0
        self.rpm = RPM()
        self.auto_stop_timer()

    def set_speed(self, required_rpm):
        try:
            required_rpm = int(float(required_rpm) * 10)/10
        except ValueError:
            return
        if required_rpm < 0.1:
            self.stop()
            return
        elif required_rpm > 74.9:
            required_rpm = 74.9
        self.running = 1
        self.direction = 0
        self.requested_rpm = required_rpm
        self.rpm_controller()

    def rpm_controller(self):
        rpm = self.rpm.get_rpm()
        speedchanged = 1
        if not self.running:
            return
        if abs(rpm - self.requested_rpm) > 1:
            self.frequency = int(10 * self.requested_rpm * self.rpm_hz)
        elif rpm - self.requested_rpm > 0.1:
            logger.info('RPM slightly to high, reducing it a bit')
            self.frequency = int(self.frequency - self.rpm_hz)
        elif rpm - self.requested_rpm < -0.1:
            logger.info('RPM slightly to low, increasing it a bit')
            self.frequency = int(self.frequency + self.rpm_hz)
        else:
            speedchanged = 0
        if speedchanged:
            # print('Current f %.2f Desired %.2f' % (rpm, self.requested_rpm))
            try:
                self.controller_command([self.frequency, self.running, self.direction, 1])
            except AttributeError:
                logger.error('MotorClass: rpm controller function error No RS483 Controller')
            except minimalmodbus.NoResponseError:
                logger.error('MotorClass: rpm controller function error RS485 timeout')
            logger.info('Motorclass rpm controller: Current RPM %.2f Desired %.2f setting to frequency %s'
                        % (rpm, self.requested_rpm, self.frequency))
        rpmthread = Timer(10, self.rpm_controller)
        rpmthread.start()

    def stop(self):
        self.direction = 0
        self.frequency = 0
        self.requested_rpm = 0
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
            return {'running': running(self.running), 'reqfrequency': setting_data[0] / 100,
                    'frequency': actual_data[0] / 100, 'voltage': actual_data[9], 'current': actual_data[2] / 100,
                    'rpm': actual_data[1], 'tombola_speed': '%.2f' % self.rpm.get_rpm(),
                    'requested_speed': self.requested_rpm}
        except AttributeError:   # RS485 not plugged in
            logger.error('Tombola Query Error: RS485 controller is not working or not plugged in')
            return {'running': running(self.running), 'reqfrequency': self.frequency / 100,
                    'frequency': 'No RS485 Controller', 'voltage': 'No RS485 Controller',
                    'current': 'No RS485 Controller', 'rpm': 'No RS485 Controller',
                    'tombola_speed': '%.2f' % self.rpm.get_rpm(), 'requested_speed': self.requested_rpm}
        except minimalmodbus.NoResponseError:
            logger.error('Tombola Query Error: No response from the V20 controller, '
                         'check it is powered on and connected')
            return {'running': running(self.running), 'reqfrequency': self.frequency / 100,
                    'frequency': 'RS485 Timeout', 'voltage': 'RS485 Timeout', 'current': 'RS485 Timeout',
                    'rpm': 'RS485 Timeout', 'tombola_speed': '%.2f' % self.rpm.get_rpm(),
                    'requested_speed': self.requested_rpm}
        except:
            logger.error('Tombola Query Error: unhandled exeption')
            return {'running': running(self.running), 'reqfrequency': self.frequency / 100, 'frequency': '-',
                    'voltage': '-', 'current': '-', 'rpm': '-', 'tombola_speed': '%.2f' % self.rpm.get_rpm(),
                    'requested_speed': self.requested_rpm}

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
            logger.info('Stop request recieved web application')
            self.stop()
        elif 'websetrpm' in message.keys():
            logger.info('RPM set by web application')
            self.set_speed(message['websetrpm'])
        elif 'setrpm' in message.keys():
            self.set_speed(message['websetrpm'])
        elif 'reset' in message.keys():
            self.write_register(self.stw_control_register, settings['STW_forward'])
        elif 'write_register' in message.keys():
            self.write_register(message['write_register'] - self.register_offset, message['word'])
        elif 'read_register' in message.keys():
            return self.read_register(message['read_register'] - self.register_offset)
        elif 'rpm_data' in message.keys():
            return self.rpm.get_rpm_data()
        elif 'rpm' in message.keys():
            return {'rpm': self.rpm.get_rpm()}
        elif 'stoptime' in message.keys():
            if 'autostop' in message.keys():
                self.set_stop_time(True, message['stoptime'])
            else:
                self.set_stop_time(False, message['stoptime'])
            logger.info('Stop time updated via web application')
        else:
            logger.info('message recieved but not processed  = %s' % message)  # used for debugging HTML Forms
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
