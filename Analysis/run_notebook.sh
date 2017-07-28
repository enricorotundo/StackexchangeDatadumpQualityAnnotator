#!/bin/bash

# this script runs a Django server with iPython notebook extensions
# then you can open notebooks in Tasks/*/*.ipynb
cd ..
source venv/bin/activate
python manage.py shell_plus --notebook --no-browser
