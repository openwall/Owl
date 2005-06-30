#!/bin/awk

# change all services (except: local,pipe,proxymap,virtual)
# to run chrooted.

BEGIN			{ OFS="\t"; }
/^#([^a-z0-9]|$)/	{ print; next; }
/^[[:space:]]/			{ print; next; }
$8 ~ /(local|pipe|proxymap|virtual)/	{ print; next; }
			{ $5="-"; print; }
