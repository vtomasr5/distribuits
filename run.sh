#!/bin/sh

sh set_env.sh
python main.py; cat debug.log
