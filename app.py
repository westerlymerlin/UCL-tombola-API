import os
from flask import Flask, render_template, jsonify, request
from settings import settings, version
from MotorClass import Motor
import logmanager

app = Flask(__name__)
tom = Motor()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print('Settings updated via web application')
    return render_template('index.html')



@app.route('/statusdata', methods=['GET', 'POST'])
def statusdata():
    # Query the motor controller for current data
    motor_data = tom.controller_query()
    if not motor_data or isinstance(motor_data, str):  # Check if we received a valid response
        return jsonify({'error': 'Unable to fetch motor data'}), 500

    # Extract motor data from the motor_data list.
    # This is an assumption based on the order in your MotorClass; you may need to adjust indices.
    ctrldata = {
        'running': tom.running,
        'direction': 'FWD' if tom.direction == 0 else 'REV',
        'frequency': tom.frequency,
        'voltage': 0,  # Placeholder, replace with real data if available
        'current': 0,  # Placeholder, replace with real data if available
        'rpm': 0,  # Placeholder, replace with real data if available
    }

    # Getting CPU temperature, as before:
    with open(settings['cputemp'], 'r') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log) / 1000, 1)
    ctrldata['cpu'] = cputemperature

    return jsonify(ctrldata), 201

@app.route('/pylog')
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
    return render_template('logs.html', rows=logs, log='X-Y log', cputemperature=cputemperature, version=version)

@app.route('/start/<int:speed>', methods=['GET'])
def start(speed):
    try:
        tom.forward(speed)
        return "Tombola started with speed: {}".format(speed)
    except Exception as e:
        return "Error: {}".format(str(e))

@app.route('/stop', methods=['GET'])
def stop():
    try:
        tom.stop()
        return "Tombola stopped"
    except Exception as e:
        return "Error: {}".format(str(e))

@app.route('/guaccesslog')
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
    return render_template('logs.html', rows=logs, log='gunicorn access log', cputemperature=cputemperature, version=version)


@app.route('/guerrorlog')
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
    return render_template('logs.html', rows=logs, log='gunicorn error log', cputemperature=cputemperature, version=version)


@app.route('/syslog')
def showslogs():
    with open(settings['cputemp'], 'r') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    with open(settings['syslog'], 'r') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='system log', cputemperature=cputemperature)

@app.route('/uscHALT')
def shutdown_the_server():
    os.system('sudo halt')
    return 'The server is now shutting down, please give it a minute before pulling the power. \nCheers G'


def reboot():
    print('System is restarting now')
    os.system('sudo reboot')


if __name__ == '__main__':
    app.run()
