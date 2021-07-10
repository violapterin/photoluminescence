#! /usr/bin/env bash

THIS=$(dirname "$0")
clear
${THIS}/make-post-all.py
python3 -m http.server -d ${THIS}/site
