# $Id: Owl/build/Makefile,v 1.6 2000/12/28 17:19:39 solar Exp $

default: buildworld

checkout:
	mkdir -p checkout
	cd checkout && cvs co Owl

symlinks:
	test -d checkout/Owl/build || $(MAKE) checkout
	ln -sf checkout/Owl/build/.rpm* .
	ln -s checkout/Owl/build/*.conf . 2> /dev/null || :

buildworld: symlinks
	checkout/Owl/build/buildworld.sh

installworld: symlinks
	checkout/Owl/build/installworld.sh

setup: symlinks
	checkout/Owl/build/setup.sh

clean:
	test -d SRPMS && rm -f SRPMS/* || :
	test -d RPMS && rm -f RPMS/* || :

.PHONY: default checkout symlinks buildworld installworld setup clean
