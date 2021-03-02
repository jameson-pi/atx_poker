#!/bin/sh
if  [[ $1 = "-i" ]]; then
    pip install -r requirements.txt
else
    pip install -r requirements.txt
    cd src   
    if  [[ $1 = "-p" ]]; then
        python3 print_data.py
    else
        export FLASK_APP=main.py
        python3 -m flask run
cd ..
fi
fi