# $Id: Owl/build/Makefile,v 1.15.2.1 2003/12/19 19:15:31 solar Exp $

# The Owl branch to build and/or install, specified by its tag in the
# CVS.  This should only be set to build and/or install a non-current
# branch.
#
TAG=Owl-1_1-release

MODULE=Owl
BRANCH=$(if $(TAG),$(TAG),$(MODULE))

default: symlinks
	BRANCH=$(BRANCH) native/$(BRANCH)/build/buildworld.sh

checkout:
	test "`id -u`" != "0" # CVS checkout must not be done as root
	mkdir -p native
	cd native && cvs co -P $(if $(TAG),-r $(TAG) -d $(BRANCH) )$(MODULE)

symlinks:
	test -d native/$(BRANCH)/build || $(MAKE) checkout
	ln -sf native/$(BRANCH)/build/.rpm* .
	ln -s native/$(BRANCH)/build/*.conf . 2> /dev/null || :

buildworld: symlinks
	BRANCH=$(BRANCH) PACKAGE= native/$(BRANCH)/build/buildworld.sh

installworld: symlinks
	native/$(BRANCH)/build/installworld.sh

setup: symlinks
	native/$(BRANCH)/build/setup.sh

clean:
	test -d RPMS && rm -f RPMS/* || :
	test -d SRPMS && rm -f SRPMS/* || :
	test -d archives && rm -f archives/* || :

.PHONY: default checkout symlinks buildworld installworld setup clean
