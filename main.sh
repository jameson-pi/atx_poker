
#!/bin/sh
if  [[ $1 = "-i" ]]; then
    pip install -r requirements.txt
else
    if [[ $1 = "-n" ]]; then
        true
    else
        pip 
    fi
    cd src   
    if  [[ $1 = "-p" ]]; then
        python3 print_data.py
    else
        export FLASK_APP=main.py
        python3 -m flask run
    fi 
cd ..
fi