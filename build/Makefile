# $Id: Owl/build/Makefile,v 1.4 2000/12/03 23:01:25 solar Exp $

default: buildworld

checkout:
	cd checkout && cvs co Owl

symlinks:
	test -d checkout/Owl/build || $(MAKE) checkout
	ln -sf checkout/Owl/build/{*.sh,.rpm*} .
	ln -s checkout/Owl/build/*.conf . 2> /dev/null || :

buildworld: symlinks
	./buildworld.sh

installworld: symlinks
	./installworld.sh

clean:
	test -d SRPMS && rm -f SRPMS/* || :
	test -d RPMS && rm -f RPMS/* || :

.PHONY: default checkout symlinks buildworld installworld clean
