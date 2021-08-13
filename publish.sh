#! /usr/bin/env bash

if ! command -v convert &> /dev/null
then
    echo "Please install ImageMagick."
    exit
fi

THIS="$(dirname $0)"
SUFFIX_IN=".jpg"
SUFFIX_OUT=".pdf"
book="${THIS}/book"
leaf="${book}/leaf"
path_full="${book}/full${SUFFIX_OUT}"
option="\
   -units pixelsperinch\
   -density 300\
   -page a4\
   -auto-orient"
set -x
rm -f "${path_full}"
convert ${leaf}/*${SUFFIX_IN} ${option} ${path_full}
{ set +x; } 2>/dev/null
