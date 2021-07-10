#! /usr/bin/env bash

THIS=$(dirname "$0")
clear
${THIS}/make-post-new.py
python3 -m http.server -d ${THIS}/site
