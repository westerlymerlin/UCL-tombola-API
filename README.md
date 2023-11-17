# UCL-tombola

An application to control the UCL River Simulator.<br>
The River simulator consistes of a large (1m diameter) drum that can contain water, cement blocks simulate rocks on the riverbed.
The whole contraption is driven by a 1/4 hp 3 phase motor.

The 3 phase motor is controlled by a **Siemens V20** single phase to 3 phase invertor which is controled via an RS485 
interface using the modbus protocol<br>
**V20 Datasheet:**
https://support.industry.siemens.com/cs/attachments/109824500/V20_op_instr_0823_en-US.pdf
  
The contoller application runs on a **Raspberry Pi 3B or 4B** single board computer. It is written in Python and uses 
Flask for the Web application server. A USB RS485 controller provides connectivity to the V20 Invertor and the python 
library **Minimal Modbus** is used for the Modbus protocol.<br>
**Minimal Modbus Library Documentation** https://minimalmodbus.readthedocs.io/en/stable/

---
**Web Application**

Accessing the URL `http://[url to your server]/api` via a web browser will open that status web page. It has buttons to
allow starting the Tombola, stopping it and setting an auto-stop time if it is being left unatended.

**Direct API Calls**

If you POST a json message to the `http://[url to your server]/api` end point the flast app will process the call and
return a json message containing the V20 status values.

***API Messages***
`{"forward": n}`  Start the motor running forwardat a frequency of n where n is 0 - 10000<br>
`{"frequency": 0}`  Stop the motor<br>
`{"reverse": n}`  Start the motor running forwardat a frequency of n where n is 0 - 10000<br>
`{"rpm": True}`  Read the tombola RPM<br>
`{"rpm_data": True}`  Read the tombola timing data from 3 revolutions<br>
`{"write_register": rr, "word": ww}`  Write the word ww to the register rr<br>
`{"read_register": rr}`  Read the value from the register rr<br>
`{"frequency": 0}`  Stop the motor<br>
`{"stoptime": "HH:MM:SS", "autostop": true}` set the controller to auto shut off at HH:MM:SS<br>
`{"stoptime": "HH:MM:SS", "autostop": false}` Disable auto stop




---
**MotorClass.py Commands:**

`tom.forward( int )`                  set the 40003 (frequency setpoint) to int, 40004 (Run Enable) to 1, 40005
 (Forward/reverse command) to 0, 40006 (Start command) to 1<br>
`tom.reverse( int )`                set the 40003 (frequency setpoint) to int, 40004 (Run Enable) to 1, 40005
(Forward/reverse command) to 1, 40006 (Start command) to 1<br>
`tom.stop()`                        set the 40003 (frequency setpoint) to 0, 40004 (Run Enable) to 0, 40005
(Forward/reverse command) to 0, 40006 (Start command) to 0<br>
`tom.controller_query()`            returns the values of registers 40024 to 40039<br>
`tom.print_controlword()`            prints the value from register 99(STW)<br>
`tom.writeregister(int1, int2)`      will write the value **int2** into the register **int1**
e.g. `tom.writeregister(99, 129)` writes the value **129** into register **99**

---
**settings.json changes for com port**

Run the MortorClass.py file first, it will generate a fresh settings.json file<br>
Plug in the USB RS485 controller and find the port number (*com1* to *com7* on a PC or */dev/ttyUSB0* to
*/dev/ttyUSB9* on a mac or Raspberry Pi)  <br>
Change the value for `"port": "com5",`  to suite and run again to pick up the new port accress

