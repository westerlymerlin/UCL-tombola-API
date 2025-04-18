# Contents for: app

* [app](#app)
  * [subprocess](#app.subprocess)
  * [enumerate\_threads](#app.enumerate_threads)
  * [Flask](#app.Flask)
  * [render\_template](#app.render_template)
  * [jsonify](#app.jsonify)
  * [request](#app.request)
  * [settings](#app.settings)
  * [VERSION](#app.VERSION)
  * [MotorClass](#app.MotorClass)
  * [logger](#app.logger)
  * [app](#app.app)
  * [tom](#app.tom)
  * [threadlister](#app.threadlister)
  * [index](#app.index)
  * [statusdata](#app.statusdata)
  * [api](#app.api)
  * [showplogs](#app.showplogs)
  * [showgalogs](#app.showgalogs)
  * [showgelogs](#app.showgelogs)
  * [showslogs](#app.showslogs)

<a id="app"></a>

# app

This is the main flask application - called by Gunicorn
Author: Gary Twinn

<a id="app.subprocess"></a>

## subprocess

<a id="app.enumerate_threads"></a>

## enumerate\_threads

<a id="app.Flask"></a>

## Flask

<a id="app.render_template"></a>

## render\_template

<a id="app.jsonify"></a>

## jsonify

<a id="app.request"></a>

## request

<a id="app.settings"></a>

## settings

<a id="app.VERSION"></a>

## VERSION

<a id="app.MotorClass"></a>

## MotorClass

<a id="app.logger"></a>

## logger

<a id="app.app"></a>

#### app

<a id="app.tom"></a>

#### tom

<a id="app.threadlister"></a>

#### threadlister

```python
def threadlister()
```

Lists threads currently running

<a id="app.index"></a>

#### index

```python
@app.route('/', methods=['GET', 'POST'])
def index()
```

Main web page handler, shows status page via the index.html template

<a id="app.statusdata"></a>

#### statusdata

```python
@app.route('/statusdata', methods=['GET'])
def statusdata()
```

Status data read by javascript on default website

<a id="app.api"></a>

#### api

```python
@app.route('/api', methods=['POST'])
def api()
```

API Endpoint for programatic access - needs request data to be posted in a json file

<a id="app.showplogs"></a>

#### showplogs

```python
@app.route('/pylog')
def showplogs()
```

Displays the application log file via the logs.html template

<a id="app.showgalogs"></a>

#### showgalogs

```python
@app.route('/guaccesslog')
def showgalogs()
```

Displays the gunicorn access log file via the logs.html template

<a id="app.showgelogs"></a>

#### showgelogs

```python
@app.route('/guerrorlog')
def showgelogs()
```

Displays the gunicorn error log file via the logs.html template

<a id="app.showslogs"></a>

#### showslogs

```python
@app.route('/syslog')
def showslogs()
```

Displays the last 2000 lines if the system log file via the logs.html template

