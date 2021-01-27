#!/bin/bash

if [ "$(whoami)" == "azabyo" ]; then
    source /home/azabyo/azabyo_vscode/hinet_py/venv/bin/activate
    nohup python /home/azabyo/azabyo_vscode/hinet_py/hinet.py > /dev/null &
elif [ "$(whoami)" == "root" ]; then
    su - azabyo
    source /home/azabyo/azabyo_vscode/hinet_py/venv/bin/activate
    nohup python /home/azabyo/azabyo_vscode/hinet_py/hinet.py > /dev/null &
else
    echo "permission error"
fi
#python /home/azabyo/azabyo_vscode/hinet_py/hinet.py
