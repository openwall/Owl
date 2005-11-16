#!/bin/sh -e
#
# $Owl: Owl/packages/postfix/postfix-oclosure.sh,v 1.2 2005/11/16 13:28:58 solar Exp $
#
# Written by Dmitry V. Levin and placed in the public domain.
#
# There's absolutely no warranty.
#

in=
out=
exit_handler()
{
	local rc=$?
	trap - EXIT
	[ -z "$in" ] || rm -f -- "$in"
	[ -z "$out" ] || rm -f -- "$out"
	exit $rc
}

trap exit_handler EXIT HUP INT QUIT PIPE TERM

in=$(mktemp -t in.XXXXXXXXXX) || exit $?
out=$(mktemp -t out.XXXXXXXXXX) || exit $?

order="$1"
shift

sort -u >"$in"
while :; do
	# find out all objects required for $in.
	join -1 1 -2 2 -o 2.1 "$in" "$order" |
		sort -u >"$out"
	# if result not changed, break.
	cmp -s "$in" "$out" && break || cp "$out" "$in"
done

sort -u "$out"
