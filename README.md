# UCL-tombola

**An application to control the UCL River Simulator.**
<br>
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

Full documentation can be found in the file https://github.com/westerlymerlin/UCL-tombola/blob/master/docs/Tombola%20Functional%20Description.docx

---
**Web Application**
<br>
Accessing the URL `http://[url to your server]` via a web browser will open that status web page. It has buttons to
allow starting the Tombola, stopping it and setting an auto-stop time if it is being left unatended.

**Direct API Calls**
<br>
If you POST a json message to the `http://[url to your server]/api` end point the flast app will process the call and
return a json message containing the V20 status values.

**API Messages**
<br>
`{"setrpm": n.n}`  Start the tombola running and hold it at n.n rpm (0.1 - 74.9 rpm)<br>
`{"setrpm": 0}`  Stop the tombola<br>
`{"rpm": True}`  Read the tombola RPM<br>
`{"rpm_data": True}`  Read the tombola abs sensor timing data from 3 revolutions<br>
`{"write_register": rr, "word": ww}`  Write the word ww to the register rr<br>
`{"read_register": rr}`  Read the value from the register rr<br>
`{"stoptime": "HH:MM:SS", "autostop": true}` set the controller to auto shut off at HH:MM:SS<br>
`{"stoptime": "HH:MM:SS", "autostop": false}` Disable auto stop

---

**Shell Commands**
<br>
These can be run from a the console (via ssh or direct on the raspberry pi) to upgrade to the latest version of the
python code:<br>
`deploy-from-git.sh`  Check github for a newer version of the code and if there is download, deply and restart the 
python web app<br>
<br>
Less often used comamnds used for troubelshooting:<br>
`stopservices.sh` Stop the gunicorn and nginx services<br>
`startservices.sh` Start the gunicorn and nginx services<br>
`restartservices.sh` Stop, then start the gunicorn and nginx services<br>
`status.sh` Show the status of the gunicorn and nginx services<br>
<br>

---

**settings.json changes for com port**
<br>
Run the MortorClass.py file first, it will generate a fresh settings.json file<br>
Plug in the USB RS485 controller and find the port number (*com1* to *com7* on a PC or */dev/ttyUSB0* to
*/dev/ttyUSB9* on a mac or Raspberry Pi)  <br>
Change the value for `"port": "com5",`  to suite and run again to pick up the new port accress

