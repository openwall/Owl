#!/bin/sh
#
# To use this filter with less, define LESSOPEN:
# export LESSOPEN="|/usr/local/bin/lesspipe.sh %s"

lesspipe() {
  case "$1" in
  *.tar) tar tvvf "$1" 2>/dev/null ;; # View contents of .tar and .tgz files
  *.tgz) tar tzvvf "$1" 2>/dev/null ;;
  *.tar.gz) tar tzvvf "$1" 2>/dev/null ;;
  *.tar.bz2) bzip2 -dc "$1" | tar tvvf - 2>/dev/null ;;
  *.tar.Z) tar tzvvf "$1" 2>/dev/null ;;
  *.tar.z) tar tzvvf "$1" 2>/dev/null ;;
  *.Z) gzip -dc "$1" 2>/dev/null ;; # View compressed files correctly
  *.z) gzip -dc "$1" 2>/dev/null ;;
  *.zip) unzip -l "$1" 2>/dev/null ;;
  *.rpm) rpm -qpivl "$1" 2>/dev/null ;; # view contents of .rpm files
  *.1|*.2|*.3|*.4|*.5|*.6|*.7|*.8|*.9|*.n|*.man)
    FILE="`file -L - < "$1" | grep "^standard input: *troff"`" ; # groff src
    if [ -n "$FILE" ]; then
      cat "$1" | (cd / && groff -s -p -t -e -Tascii -mandoc -)
    fi ;;
  *.1.gz|*.2.gz|*.3.gz|*.4.gz|*.5.gz|*.6.gz|*.7.gz|*.8.gz|*.9.gz|*.n.gz|*.man.gz)
    if gzip -dc "$1" | file - | grep troff &>/dev/null; then
      gzip -dc "$1" | (cd / && groff -s -p -t -e -Tascii -mandoc -)
    else
      gzip -dc "$1" 2>/dev/null
    fi ;;
  *.1.bz2|*.2.bz2|*.3.bz2|*.4.bz2|*.5.bz2|*.6.bz2|*.7.bz2|*.8.bz2|*.9.bz2|*.n.bz2|*.man.bz2)
    if bzip2 -dc "$1" | file - | grep troff &>/dev/null; then
      bzip2 -dc "$1" | (cd / && groff -s -p -t -e -Tascii -mandoc -)
    else
      bzip2 -dc "$1" 2>/dev/null
    fi ;;
  *.gz) gzip -dc "$1" 2>/dev/null ;;
  *.bz2) bzip2 -dc "$1" 2>/dev/null ;;
  esac
}

if [ -n "`echo "$1" | grep "^-"`" ]; then
	lesspipe "./$1"
else
	lesspipe "$1"
fi
