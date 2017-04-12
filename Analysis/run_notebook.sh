#!/bin/bash

# this script runs a Django server with iPython notebook extensions

source ../venv/bin/activate
../venv/bin/python manage.py shell_plus --notebook --no-browser
