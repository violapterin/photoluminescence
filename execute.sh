#! /usr/bin/env bash

clear
./make-site.py
python3 -m http.server -d ./site
