# $Id: Owl/build/Makefile,v 1.5 2000/12/03 23:07:38 solar Exp $

default: buildworld

checkout:
	mkdir -p checkout
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
