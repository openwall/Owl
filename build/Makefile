# $Owl: Owl/build/Makefile,v 1.25 2007/01/08 00:54:08 ldv Exp $

# The Owl branch to build and/or install, specified by its tag in the
# CVS.  This should only be set to build and/or install a non-current
# branch.
#
#TAG=Owl-2_0-stable

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
	ln -s native/$(BRANCH)/build/{*.conf,.rpm*} . 2> /dev/null || :

buildworld: symlinks
	BRANCH=$(BRANCH) PACKAGE= native/$(BRANCH)/build/buildworld.sh

installworld: symlinks
	native/$(BRANCH)/build/installworld.sh

buildkernel: symlinks
	BRANCH=$(BRANCH) native/$(BRANCH)/build/buildkernel.sh

installisotree: symlinks
	BRANCH=$(BRANCH) native/$(BRANCH)/build/installisotree.sh

iso: installisotree
	BRANCH=$(BRANCH) native/$(BRANCH)/build/makeiso.sh

setup: symlinks
	native/$(BRANCH)/build/setup.sh

clean:
	test -d RPMS && rm -f RPMS/* || :
	test -d SRPMS && rm -f SRPMS/* || :
	test -d archives && rm -f archives/* || :
	test -d kernel-work && rm -rf kernel-work || :

.PHONY: default checkout symlinks
.PHONY: buildworld installworld buildkernel installisotree iso setup clean
