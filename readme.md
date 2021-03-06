# source_template_map
In order to give all Source Engineers easy access to information on templated sources, a simple script creates a mapping table and projects it to this google sheet: https://docs.google.com/spreadsheets/d/1fnLuniqzygD_zW1CGRmU9XGaBnm14wRmc6vUHWy-PbQ/edit?usp=sharing

## requirements
Script requires python3.6 or newer, access to magenta db and google creds that have write permission for the google sheet.

### setting up virtual environment and installing packages

After cloning this repo on a machine in Basefarm, make sure there is an up-to-date version of pip installed:
``pip3 install --upgrade --user pip``


1. make sure virtualenv is installed for your current user:
``$ pip3 install --user virtualenv``
2. create virtual environment:
``$ virtualenv venv``
3. activate virtual environment:
``$ source venv/bin/activate``
4. installing required packages:
``$ pip3 install -r requirements.txt``

To exit virtual environment simply use ``$ deactivate``
(see official documentation and installation/user guide for virtualenv here: https://virtualenv.pypa.io/en/latest/)

### setting up mysql databases
in order to connect to magenta, specify user, password, host and server in ``mysql_client/config.ini``

### setting up google api
in order to authenticate with google a secret is required, which can be gotten from the google developer console (https://console.developers.google.com/). It is currently set up using a support service account, please reach out to moritz.lorey@meltwater.com or dave.parker@meltwater.com for details.

## execution
Script can be executed with ``python3 source_template_map.py``
