# UCL-tombola

**Minimal Modbus Library Documentation** https://minimalmodbus.readthedocs.io/en/stable/

**Uses V20 power controller**
**Datasheet:**  https://support.industry.siemens.com/cs/attachments/109824500/V20_op_instr_0823_en-US.pdf
  
**USB RS484 Controller**

**Raspberry Pi 4B**


---
**MotorClass.py Commands:**

`tom.forward( int )`                  set the 40003 (frequency setpoint) to int, 40004 (Run Enable) to 1, 40005 (Forward/reverse command) to 0, 40006 (Start command) to 1

`tom.reverse( int )`                set the 40003 (frequency setpoint) to int, 40004 (Run Enable) to 1, 40005 (Forward/reverse command) to 1, 40006 (Start command) to 1

`tom.stop()`                        set the 40003 (frequency setpoint) to 0, 40004 (Run Enable) to 0, 40005 (Forward/reverse command) to 0, 40006 (Start command) to 0

`tom.controller_query()`            returns the values of registers 40024 to 40039

`tom.print_controlword()`            prints the value from register 99(STW)

`tom.writeregister(int1, int2)`      will write the value **int2** into the register **int1**	e.g. `tom.writeregister(99, 129)` writes the value **129** into register **99**

---
**settings.json changes for com port**

Run the MortorClass.py file first, it will generate a fresh settings.json file

Plug in the USB RS485 controller and find the port number (*com1* to *com7* on a PC or */dev/ttyUSB0* to */dev/ttyUSB9* on a mac or Raspberry Pi)  
 
Change the value for `"port": "com5",`  to suite and run again to pick up the new port accress

