"""
This is the main flask application - called by Gunicorn
Author: Gary Twinn
"""

import subprocess
from flask import Flask, render_template, jsonify, request
from settings import settings, VERSION
from motor_class import MotorClass
from logmanager import logger


logger.info('Starting Tombola web app version %s', VERSION)
app = Flask(__name__)
tom = MotorClass()

logger.info('Api-Key = %s', settings['api-key'])


@app.route('/', methods=['GET', 'POST'])
def index():
    """Main web page handler, shows status page via the index.html template"""
    if request.method == 'POST':
        # print(request.form)
        if len(request.form) == 0:
            logger.warning('Index page: Invalid Web Post Recieved - returning 405 to %s',
                           request.headers['X-Forwarded-For'])
            return '<!doctype html><html lang=en><title>405 Method Not Allowed</title>' \
                   '<h1>Method Not Allowed</h1>' \
                   '<p>The method is not allowed for the requested URL.</p>', 405
        logger.debug('Index page: Web Post recieved')
        tom.parse_control_message(request.form)
    return render_template('index.html', rpm_max=settings['rpm_max'], version=VERSION,
                           rpm=tom.requested_rpm, stoptimer=tom.get_stop_time())


@app.route('/statusdata', methods=['GET'])
def statusdata():
    """Status data read by javascript on default website"""
    ctrldata = tom.controller_query()  # Query the motor controller for current data
    with open(settings['cputemp'], 'r', encoding='UTF-8') as f:  # Get CPU temperature
        log = f.readline()
    f.close()
    cputemperature = round(float(log) / 1000, 1)
    ctrldata['cpu'] = cputemperature
    return jsonify(ctrldata), 201


@app.route('/api', methods=['POST'])
def api():
    """API Endpoint for programatic access - needs request data to be posted in a json file"""
    try:
        if 'Api-Key' in request.headers.keys():  # check api key exists
            if request.headers['Api-Key'] == settings['api-key']:  # check for correct API key
                status = tom.parse_control_message(request.json)
                return jsonify(status), 201
            logger.warning('API: access attempt using an ivalid token from %s', request.headers['X-Forwarded-For'])
            return 'access token(s) unuthorised', 401
        logger.warning('API: access attempt without a token from %s', request.headers['X-Forwarded-For'])
        return 'access token(s) incorrect', 401
    except KeyError:
        logger.warning('API: bad json message from %s', request.headers['X-Forwarded-For'])
        return "badly formed json message", 400


@app.route('/pylog')  # display the application log
def showplogs():
    """Displays the application log file via the logs.html template"""
    with open(settings['logfilepath'], 'r', encoding='UTF-8') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='Tombola log', version=VERSION)


@app.route('/guaccesslog')  # display the gunicorn access log
def showgalogs():
    """Displays the gunicorn access log file via the logs.html template"""
    with open(settings['gunicornpath'] + 'gunicorn-access.log', 'r', encoding='UTF-8') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='gunicorn access log', version=VERSION)


@app.route('/guerrorlog')  # display the gunicorn error log
def showgelogs():
    """Displays the gunicorn error log file via the logs.html template"""
    with open(settings['gunicornpath'] + 'gunicorn-error.log', 'r', encoding='UTF-8') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='gunicorn error log', version=VERSION)


@app.route('/syslog')  # display the raspberry pi system log
def showslogs():
    """Displays the last 200 lines if the system log file via the logs.html template"""
    log = subprocess.Popen('journalctl --system --system -n 1000', shell=True,
                           stdout=subprocess.PIPE).stdout.read().decode(encoding='utf-8')
    logs = log.split('\n')
    logs.reverse()
    return render_template('logs.html', rows=logs, log='system log', version=VERSION)


if __name__ == '__main__':
    app.run()
