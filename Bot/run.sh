#!/bin/bash

# Creating virtual environment with defined libraries from requirements.txt
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

# Running the controller
python3 main.py "$1"
