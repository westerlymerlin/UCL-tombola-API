# None

<a id="app_control"></a>

# app\_control

Settings Management Module

This module handles application configuration settings with JSON persistence.
It provides functionality to read, write, and initialize application settings
from a settings.json file with fallback to defaults when settings are missing.

Features:
- Automatic creation of settings.json if not present
- Default values for all settings
- Persistence of settings to JSON format
- Automatic detection and addition of new settings
- Timestamp tracking of settings modifications

Usage:
    import from app_control import settings, writesettings

<a id="app_control.json"></a>

## json

<a id="app_control.datetime"></a>

## datetime

<a id="app_control.VERSION"></a>

#### VERSION

<a id="app_control.writesettings"></a>

#### writesettings

```python
def writesettings()
```

Write settings to json file

<a id="app_control.initialise"></a>

#### initialise

```python
def initialise()
```

Setup the settings structure with default values

<a id="app_control.readsettings"></a>

#### readsettings

```python
def readsettings()
```

Read the json file

<a id="app_control.loadsettings"></a>

#### loadsettings

```python
def loadsettings()
```

Replace the default settings with thsoe from the json files

<a id="app_control.settings"></a>

#### settings

