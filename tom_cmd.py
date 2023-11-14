# a basic command line app to allow a user connected to the raspberry pi console via TTY or SSH
# to send stop start messages to the app.

import requests


def setspeed(speed):
    message = {"frequency": speed}
    try:
        resp = requests.post('http://localhost/api', json=message, timeout=1)
        return resp.json()
    except requests.exceptions.ConnectTimeout:
        return {'setspeed': 'Timeout Error'}


if __name__ == '__main__':
    frequency = input('Enter a speed or a 0 to stop:')
    data = setspeed(frequency)
    for item in data.items():
        print(item)
