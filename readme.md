# source_template_map
In order to give all Source Engineers easy access to information on templated sources, a simple script creates a mapping table and projects it to this google sheet: https://docs.google.com/spreadsheets/d/1fnLuniqzygD_zW1CGRmU9XGaBnm14wRmc6vUHWy-PbQ/edit?usp=sharing

## requirements
Script requires python3.6 or newer, access to magenta db and google creds that have write permission for the google sheet.

### setting up virtual environment and installing packages

(see official documentation and installation and user guide here: https://virtualenv.pypa.io/en/latest/)
1. make sure virtualenv is installed for your current user:
``$ pip3 install --user virtualen``
2. create virtual environment:
``$ virtualenv venv``
3. activate virtual environment:
``$ source venv/bin/activate``
4. installing required packages:
``$ pip install -r requirements.txt``

To exit virtual environment simply use ``$ deactivate``

### setting up mysql databases
in order to connect to magenta, specify user, password, host and server in ``mysql_client/config.ini``

### google api
in order to authenticate with google a secret is required, please reach out to moritz.lorey@meltwater.com or dave.parker@meltwater.com
