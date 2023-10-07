import minimalmodbus
from settings import settings


class Motor:
    def __init__(self):
        self.command_start_register = settings['control_offset'] - 40001
        self.query_start_register = settings['read_offset'] - 40001
        self.controller = minimalmodbus.Instrument(settings['port'], settings['station'], minimalmodbus.MODE_RTU)
        self.controller.serial.parity = minimalmodbus.serial.PARITY_NONE
        self.controller.serial.baudrate = settings['baud']
        self.controller.serial.bytesize = settings['bytesize']
        self.controller.serial.stopbits = settings['stopbits']
        self.controller.serial.timeout = settings['timeout']
        self.controller.clear_buffers_before_each_transaction = settings['clear_buffers_before_call']
        self.controller.close_port_after_each_call = settings['clear_buffers_after_call']
        self.read_length = settings['read_length']
        self.direction = 0  # 0 = forward, 1 = reverse
        self.frequency = 0  # 0 - 100%
        self.running = 0  # O = disabled 1 = enabled

    def forward(self, speed):
        self.direction = 0
        self.frequency = speed
        self.running = 1
        self.controller_command([self.frequency, self.running, self.direction])

    def reverse(self, speed):
        self.direction = 1
        self.frequency = speed
        self.running = 1
        self.controller_command([self.frequency, self.running, self.direction])

    def stop(self):
        self.direction = 0
        self.frequency = 0
        self.running = 0
        self.controller_command([self.frequency, self.running, self.direction])

    def controller_command(self, message):
        self.controller.write_registers(self.command_start_register, message)
        self.controller.serial.close()

    def controller_query(self):
        data = self.controller.read_registers(self.query_start_register, self.read_length, 3)
        self.controller.serial.close()
        return data


tombola_motor = Motor()
