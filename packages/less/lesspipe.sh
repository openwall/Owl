#!/bin/sh
#
# To use this filter with less, define LESSOPEN:
# export LESSOPEN="|/usr/local/bin/lesspipe.sh %s"

lesspipe() {
  case "$1" in
  *.tar) tar tvvf $1 2>/dev/null ;; # View contents of .tar and .tgz files
  *.tgz) tar tzvvf $1 2>/dev/null ;;
  *.tar.gz) tar tzvvf $1 2>/dev/null ;;
  *.tar.bz2) bzip2 -dc $1 | tar tvvf - 2>/dev/null ;;
  *.tar.Z) tar tzvvf $1 2>/dev/null ;;
  *.tar.z) tar tzvvf $1 2>/dev/null ;;
  *.Z) gzip -dc $1  2>/dev/null ;; # View compressed files correctly
  *.z) gzip -dc $1  2>/dev/null ;;
  *.gz) gzip -dc $1  2>/dev/null ;;
  *.bz2) bzip2 -dc $1  2>/dev/null ;;
  *.zip) unzip -l $1 2>/dev/null ;;
  *.rpm) rpm -qpivl $1 2>/dev/null ;; # view contents of .rpm files
  *.1|*.2|*.3|*.4|*.5|*.6|*.7|*.8|*.9|*.n|*.man) FILE=`file -L $1` ; # groff src
    FILE=`echo $FILE | cut -d ' ' -f 2`
    if [ "$FILE" = "troff" ]; then
      groff -s -p -t -e -Tascii -mandoc $1
    fi ;;
  esac
}

lesspipe $1

