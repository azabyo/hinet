#!/bin/bash

if [ "$(whoami)" == "azabyo" ]; then
    echo "not azabyo"
elif [ "$(whoami)" == "root" ]; then
    echo "root"
else
    echo "else"
fi