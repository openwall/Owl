#!/bin/awk

# comment out all interfaces to non-postfix software.

BEGIN	{ found=0; }
/^# Interfaces to non-Postfix software\. /	{ found=1; }
/^#/	{ print; next; }
{
	if (found) printf ("#");
	print;
}
