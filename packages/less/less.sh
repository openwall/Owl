# less initialization script (sh)
if [ -x /usr/bin/lesspipe.sh ] ; then
  export LESSOPEN="|/usr/bin/lesspipe.sh %s"
fi
