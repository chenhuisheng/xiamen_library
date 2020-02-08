#!/bin/bash

# cd to the project
cd /project || exit

# make sure everything is installed for the project.
pip install --no-cache-dir -r requirement.txt -i https://pypi.doubanio.com/simple/

echo "APP MODE:"
echo "$APP_MODE"

python ./runserver.py $APP_MODE