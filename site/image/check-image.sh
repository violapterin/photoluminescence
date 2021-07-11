#! /usr/bin/env bash

check() {
   # # $1: input absolute folder
   for path_in in $1/*; do
      if [ ! -f "${path_in}" ]
      then
         continue
      fi
      name=$(basename "${path_in}")
      extension="${name##*.}"
      if [ "${extension}" != "jpg" ] && [ "${extension}" != "png" ]
      then
         continue
      fi
      echo "checking image" "${path_in}" "..."
      identify "${path_in}" &> /dev/null
      state=$(echo $?)
      if [ "${state}" != "0" ]
      then
         echo "   " "Corrupted!!!"
         exit
      else
         echo "   " "Valid."
      fi
   done
}

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

if ! command -v identify &> /dev/null
then
    echo "Please install ImageMagick."
    exit
fi

THIS=`dirname "$0"`
check "$THIS"
