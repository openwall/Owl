# $Owl: Owl/build/Makefile,v 1.33 2014/07/10 17:45:09 solar Exp $

# The Owl branch to build and/or install, specified by its tag in the
# CVS.  This should only be set to build and/or install a non-current
# branch.
#
#TAG = Owl-3_1-stable

MODULE = Owl
BRANCH = $(if $(TAG),$(TAG),$(MODULE))

SHELL = /bin/bash

default: symlinks
	BRANCH=$(BRANCH) native/$(BRANCH)/build/buildworld.sh

checkout:
	test "`id -u`" != "0" # CVS checkout must not be done as root
	mkdir -p native
	cd native && cvs co -P $(if $(TAG),-r $(TAG) -d $(BRANCH) )$(MODULE)

symlinks:
	test -d native/$(BRANCH)/build || $(MAKE) checkout
	ln -s native/$(BRANCH)/build/{*.conf,.rpm*} . 2> /dev/null || :

buildworld: symlinks
	BRANCH=$(BRANCH) PACKAGE= native/$(BRANCH)/build/buildworld.sh

installworld: symlinks
	native/$(BRANCH)/build/installworld.sh

installisotree: symlinks
	BRANCH=$(BRANCH) native/$(BRANCH)/build/installisotree.sh

iso: installisotree
	ISO_COMPRESS= BRANCH=$(BRANCH) native/$(BRANCH)/build/makeiso.sh

iso.gz: installisotree
	ISO_COMPRESS=yes BRANCH=$(BRANCH) native/$(BRANCH)/build/makeiso.sh

installvztree: symlinks
	BRANCH=$(BRANCH) native/$(BRANCH)/build/installvztree.sh

vztemplate: installvztree
	BRANCH=$(BRANCH) native/$(BRANCH)/build/makevztemplate.sh

setup: symlinks
	native/$(BRANCH)/build/setup.sh

clean:
	test -d RPMS && rm -f RPMS/* || :
	test -d SRPMS && rm -f SRPMS/* || :
	test -d archives && rm -f archives/* || :

.PHONY: default checkout symlinks
.PHONY: buildworld installworld installisotree iso iso.gz
.PHONY: installvztree vztemplate
.PHONY: setup clean
