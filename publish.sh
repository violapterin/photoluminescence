#! /usr/bin/env bash

compile() {
   SUFFIX_IN="png"
   many_option=" \
      -auto-orient \
      -units pixelsperinch \
      -density 300 \
      -page b5 \
      "
   set -x
   rm -f $2
   convert $1/*.${SUFFIX_IN} ${many_option} $2
   { set +x; } 2>/dev/null
}

tune() {
   SUFFIX_IN="png"
   SUFFIX_OUT="png"
   for path_in in $1/*; do
      if [ ! -f "${path_in}" ]; then
         continue
      fi
      name="$(basename ${path_in})"
      bare="${name%.*}"
      suffix="${name##*.}"
      if [ "${suffix}" != "${SUFFIX_IN}" ]; then
         continue
      fi
      path_out="$2/${bare}.${SUFFIX_OUT}"
      # # Compare time stamps:
      if [ "${path_out}" -nt "${path_in}" ]; then
         continue
      fi
      echo "tuning image ${path_in} ..."
      # brightness-contrast: percentage x percentage
      # adaptive-sharpen: radius x level
      many_option=" \
         -brightness-contrast 4x12 \
         -adaptive-sharpen 1x3 \
         -density 300 \
         -page b5 \
         "
      set -x
      convert ${path_in} ${many_option} ${path_out}
      { set +x; } 2>/dev/null
   done
}

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

if [ ! command -v convert &> /dev/null ]; then
    echo "Please install ImageMagick."
    exit
fi

if [ ! command -v gs &> /dev/null ]; then
    echo "Please install Ghostscript."
    exit
fi

THIS="$(dirname $0)"
SUFFIX_OUT="pdf"
book="${THIS}/book"
leaf="${book}/leaf"
tuned="${book}/tuned"
full="${book}/photoluminescence-full.${SUFFIX_OUT}"
if [ ! -d "${book}" ]; then
  mkdir "${book}"
fi
if [ ! -d "${leaf}" ]; then
  mkdir "${leaf}"
fi
if [ ! -d "${tuned}" ]; then
  mkdir "${tuned}"
fi

echo "    ! ! ! Tuning ${leaf} to ${tuned} ! ! !"
tune ${leaf} ${tuned}
echo "    ! ! ! Compiling ${tuned} to ${full} ! ! !"
compile ${tuned} ${full}
