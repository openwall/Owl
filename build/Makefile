# $Id: Owl/build/Makefile,v 1.9 2001/06/21 08:01:24 solar Exp $

# The Owl branch to build and/or install, specified by its tag in the
# CVS.  This should only be set to build and/or install a non-current
# branch.
#
#TAG=Owl-0_1-stable

MODULE=Owl
BRANCH=$(if $(TAG),$(TAG),$(MODULE))

default: buildworld

checkout:
	mkdir -p native
	cd native && cvs co -r $(TAG) -d $(BRANCH) $(MODULE)

symlinks:
	test -d native/$(BRANCH)/build || $(MAKE) checkout
	ln -sf native/$(BRANCH)/build/.rpm* .
	ln -s native/$(BRANCH)/build/*.conf . 2> /dev/null || :

buildworld: symlinks
	BRANCH=$(BRANCH) native/$(BRANCH)/build/buildworld.sh

installworld: symlinks
	native/$(BRANCH)/build/installworld.sh

setup: symlinks
	native/$(BRANCH)/build/setup.sh

clean:
	test -d SRPMS && rm -f SRPMS/* || :
	test -d RPMS && rm -f RPMS/* || :

.PHONY: default checkout symlinks buildworld installworld setup clean
