import os
from flask import Flask, render_template, jsonify, request
from settings import settings, version
import logmanager

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    with open(settings['cputemp'], 'r') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    if request.method == 'POST':
        print('Settings updated via web application')
    return render_template('index.html', cputemperature=cputemperature)


@app.route('/api', methods=['POST'])
def api():
    try:
        item = request.json['item']
        if item == 'gettemperature':
            return jsonify({'value': 0}), 201
        else:
            return "badly formed json message - item not found", 201
    except KeyError:
        return "badly formed json message", 201


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
