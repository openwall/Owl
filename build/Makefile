# $Id: Owl/build/Makefile,v 1.3 2000/12/03 22:18:25 solar Exp $

default: buildworld

checkout:
	cd checkout && cvs co Owl

buildworld:
	./buildworld.sh

installworld:
	./installworld.sh

clean:
	rm SRPMS/* RPMS/*

.PHONY: checkout buildworld installworld clean
