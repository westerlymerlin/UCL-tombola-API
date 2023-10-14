# UCL-tombola

#### Minimal Modbus Library Documentation `https://minimalmodbus.readthedocs.io/en/stable/`

#### Uses V20 power controller
Datasheet: ` https://support.industry.siemens.com/cs/attachments/109824500/V20_op_instr_0823_en-US.pdf`
 
 
#### USB RS484 Controller

#### Rsapberry Pi 4B




#### MotorClass.py Commands

`tom.forward( int )`                  set the 40003 (frequency setpoint) to int, 40004 (Run Enable) to 1, 40005 (Forward/reverse command) to 0, 40006 (Start command) to 1

`tom.reverse( int )`                set the 40003 (frequency setpoint) to int, 40004 (Run Enable) to 1, 40005 (Forward/reverse command) to 1, 40006 (Start command) to 1

`tom.stop()`                        set the 40003 (frequency setpoint) to 0, 40004 (Run Enable) to 0, 40005 (Forward/reverse command) to 0, 40006 (Start command) to 0

`tom.controller_query()`            returns the values of registers 40024 to 40039

