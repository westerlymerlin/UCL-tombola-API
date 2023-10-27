import os
import subprocess
from flask import Flask, render_template, jsonify, request
from settings import settings, version
from MotorClass import Motor
import logmanager

app = Flask(__name__)
tom = Motor()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if len(request.form) == 0:
            tom.stop()
        else:
            if int(request.form['setfreq']) > 0:
                tom.forward(int(request.form['setfreq']))
        print('Settings updated via web application')
    return render_template('index.html', version=version, frequency=tom.frequency)


@app.route('/statusdata', methods=['GET'])
def statusdata():
    # Query the motor controller for current data
    ctrldata = tom.controller_query()

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
    return render_template('logs.html', rows=logs, log='gunicorn access log',
                           cputemperature=cputemperature, version=version)


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
    return render_template('logs.html', rows=logs, log='gunicorn error log',
                           cputemperature=cputemperature, version=version)


@app.route('/syslog')
def showslogs():
    with open(settings['cputemp'], 'r') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    log = subprocess.Popen('journalctl -n 200 -r', shell=True,
                           stdout=subprocess.PIPE).stdout.read().decode(encoding='utf-8')
    logs = log.split('\n')
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
