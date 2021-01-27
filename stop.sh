#!/bin/bash
ps -ef | grep hinet | grep -v grep | awk -F " " '{print $2}' | xargs kill