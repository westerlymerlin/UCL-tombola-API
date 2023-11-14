import os
import subprocess
from flask import Flask, render_template, jsonify, request
from settings import settings, version
from MotorClass import Motor
import logmanager  # writes all print output to a logfile

print('Starting Tombola web app version %s' % version)
app = Flask(__name__)
tom = Motor()

@app.route('/', methods=['GET', 'POST'])  # Default website
def index():
    if request.method == 'POST':
        tom.parse_control_message(request.form)
    return render_template('index.html', version=version, frequency=tom.frequency, stoptimer=tom.get_stop_time())


@app.route('/statusdata', methods=['GET'])  # Status data read by javascript on default website
def statusdata():
    ctrldata = tom.controller_query()  # Query the motor controller for current data
    with open(settings['cputemp'], 'r') as f:  # Get CPU temperature
        log = f.readline()
    f.close()
    cputemperature = round(float(log) / 1000, 1)
    ctrldata['cpu'] = cputemperature
    return jsonify(ctrldata), 201


@app.route('/api', methods=['POST'])  # API endpoint - requires data to be sent in a json message
def api():
    try:
        print('API request: %s' % request.json)
        status = tom.parse_control_message(request.json)
        return jsonify(status), 201
    except KeyError:
        return "badly formed json message", 201


@app.route('/pylog')  # display the application log
def showplogs():
    with open(settings['cputemp'], 'r') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    with open(settings['logfilepath'], 'r') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='Tombola log', cputemperature=cputemperature, version=version)


@app.route('/guaccesslog')   # display the gunicorn access log
def showgalogs():
    with open(settings['cputemp'], 'r') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    with open(settings['gunicornpath'] + 'gunicorn-access.log', 'r') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='gunicorn access log',
                           cputemperature=cputemperature, version=version)


@app.route('/guerrorlog')  # display the gunicorn error log
def showgelogs():
    with open(settings['cputemp'], 'r') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    with open(settings['gunicornpath'] + 'gunicorn-error.log', 'r') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='gunicorn error log',
                           cputemperature=cputemperature, version=version)


@app.route('/syslog')  # display the raspberry pi system log
def showslogs():
    with open(settings['cputemp'], 'r') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    log = subprocess.Popen('journalctl -n 200 -r', shell=True,
                           stdout=subprocess.PIPE).stdout.read().decode(encoding='utf-8')
    logs = log.split('\n')
    return render_template('logs.html', rows=logs, log='system log', cputemperature=cputemperature)


@app.route('/uscHALT')  # remote shutdown of the pi
def shutdown_the_server():
    os.system('sudo halt')
    return 'The server is now shutting down, please give it a minute before pulling the power. \nCheers G'


def reboot():
    print('System is restarting now')
    os.system('sudo reboot')


if __name__ == '__main__':
    app.run()
