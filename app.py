import os
import subprocess
from flask import Flask, render_template, jsonify, request
from settings import settings, version
from MotorClass import Motor
from logmanager import logger

logger.info('Starting Tombola web app version %s' % version)
app = Flask(__name__)
tom = Motor()


@app.route('/', methods=['GET', 'POST'])  # Default website
def index():
    if request.method == 'POST':
        logger.info('Web Post recieved')
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
        #  print(request.headers)
        if 'Api-Key' in request.headers.keys():  # check api key exists
            if request.headers['api-key'] == settings['api-key']:  # check for correct API key
                print('API valid request: %s' % request.json)
                status = tom.parse_control_message(request.json)
                return jsonify(status), 201
            else:
                logger.warning('API: access attempt using an incorrect token %s' % request.remote_addr)
                return 'access token(s) unuthorised', 401
        else:
            logger.warning('API: access attempt without a token %s' % request.remote_addr)
            return 'access token(s) incorrect', 401
    except KeyError:
        return "badly formed json message", 400


@app.route('/pylog')  # display the application log
def showplogs():
    with open(settings['logfilepath'], 'r') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='Tombola log', version=version)


@app.route('/guaccesslog')   # display the gunicorn access log
def showgalogs():
    with open(settings['gunicornpath'] + 'gunicorn-access.log', 'r') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='gunicorn access log', version=version)


@app.route('/guerrorlog')  # display the gunicorn error log
def showgelogs():
    with open(settings['gunicornpath'] + 'gunicorn-error.log', 'r') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='gunicorn error log', version=version)


@app.route('/syslog')  # display the raspberry pi system log
def showslogs():
    log = subprocess.Popen('journalctl -n 200 -r', shell=True,
                           stdout=subprocess.PIPE).stdout.read().decode(encoding='utf-8')
    logs = log.split('\n')
    return render_template('logs.html', rows=logs, log='system log', version=version)


def reboot():
    logger.warn('System is restarting now')
    os.system('sudo reboot')


if __name__ == '__main__':
    app.run()
