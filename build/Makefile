# $Id: Owl/build/Makefile,v 1.7 2001/05/11 08:50:25 solar Exp $

default: buildworld

checkout:
	mkdir -p native
	cd native && cvs co Owl

symlinks:
	test -d native/Owl/build || $(MAKE) checkout
	ln -sf native/Owl/build/.rpm* .
	ln -s native/Owl/build/*.conf . 2> /dev/null || :

buildworld: symlinks
	native/Owl/build/buildworld.sh

installworld: symlinks
	native/Owl/build/installworld.sh

setup: symlinks
	native/Owl/build/setup.sh

clean:
	test -d SRPMS && rm -f SRPMS/* || :
	test -d RPMS && rm -f RPMS/* || :

.PHONY: default checkout symlinks buildworld installworld setup clean
