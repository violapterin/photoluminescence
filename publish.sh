#! /usr/bin/env bash

compile() {
   SUFFIX_IN=".jpg"
   SUFFIX_OUT=".pdf"
   TITLE="phonoluminescence-full"
   many_option="\
      -units pixelsperinch\
      -density 300\
      -page b5\
      -auto-orient\
      "
   path_out=$2/${TITLE}${SUFFIX_OUT}
   set -x
   rm -f "${path_out}"
   convert $1/*${SUFFIX_IN} ${many_option} ${path_out}
   { set +x; } 2>/dev/null
}

tune() {
   SUFFIX_IN=".jpg"
   SUFFIX_OUT=".jpg"
   for path_leaf in $1/*
   do
      if [ ! -f "${path_leaf}" ]
      then
         continue
      fi
      name="$(basename ${path_leaf})"
      extension="${name##*.}"
      bare="${name%.*}"
      if [ "${extension}" != "jpg" ]
      then
         continue
      fi
      echo "tuning image ${path_leaf} ..."
      # brightness-contrast: percentage x percentage
      # adaptive-sharpen: radius x level
      many_option="\
         -brightness-contrast 8x18\
         -adaptive-sharpen 1x3\
         "
      path_out=$2/${bare}${SUFFIX_OUT}
      set -x
      convert ${path_leaf} ${many_option} ${path_out}
      { set +x; } 2>/dev/null
   done
}

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

if [ ! command -v convert &> /dev/null ]
then
    echo "Please install ImageMagick."
    exit
fi

THIS="$(dirname $0)"
SUFFIX_IN=".jpg"
SUFFIX_OUT=".pdf"
book="${THIS}/book"
leaf="${book}/leaf"
tuned="${book}/tuned"
if [ ! -d "${book}" ]
then
  echo "${book} does not exist."
fi
if [ ! -d "${leaf}" ]
then
  echo "${leaf} does not exist."
fi
if [ ! -d "${tuned}" ]
then
  echo "${tuned} does not exist."
fi

tune ${leaf} ${tuned}
compile ${tuned} ${book}