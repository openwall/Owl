# less initialization script (csh)
test -x /usr/bin/lesspipe.sh && setenv LESSOPEN "|/usr/bin/lesspipe.sh %s"
