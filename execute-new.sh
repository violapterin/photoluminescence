#! /usr/bin/env bash

THIS=$(dirname "$0")
clear
$(dirname "$0")/make-new.py
python3 -m http.server -d ${THIS}/site
