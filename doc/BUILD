This is the guide on using the Owl build environment.  It is assumed
that you've read the CONCEPTS; if not, please do so before you proceed
with this document.


	/usr/src/world setup.

The build environment is pre-configured for the use of /usr/src/world
(the HOME= setting in buildworld.conf and installworld.conf).  It is
recommended that you leave this default setting and either actually
place the files in /usr/src/world or use a symlink if /usr/src is not
on a suitable device.  You need to have at least about 500 MB free on
the device for use during the builds.

When building natively (that is, on Owl), the directory is already
there.  Otherwise, you need to create the directory, add pseudo-user
"build", preferably with UID 151 and GID 150 ("sources"), and make it
the owner of the directory.

Place the CVS tree into /usr/src/world.  Currently, this is done by
extracting checkout.tar.gz available via the FTP sites.  You will get
the "checkout" directory, and a Makefile symlink.

For actually building from source, place the "sources" directory in
/usr/src/world as well.

If you are not on an Owl system, yet, and want to install binary
packages, create /usr/src/world/RPMS and place the packages for your
architecture in there.  Note that you need the CVS tree even for
installing binary packages.


	Native (re-)builds.

It is sufficient to type "make clean && make buildworld".  With the
default buildworld.conf, packages will be built for oldest flavor of
the build host's architecture (see ARCHITECTURES) and the build will
attempt to use up to two processors.

buildworld.conf (as well as other *.conf's) may be edited by copying
it from checkout/Owl/build into /usr/src/world.  You need to remove
the symlink first, if one has previously been created for you.


	Installing binary packages.

"make installworld" will install packages found in /usr/src/world/RPMS
onto the current system, or in a new root directory of your choice (as
specified by the ROOT= setting in installworld.conf).  By default, the
packages will be installed into /owl.

Currently, it is possible to convert an existing Red Hat Linux 6.x
installation into Owl with "make installworld" and some manual help.


	Re-building individual packages.

To re-build an Owl package: remove the SRPM in /usr/src/world/SRPMS,
remove all the binary packages produced from this source package in
/usr/src/world/RPMS, type "make buildworld".

We do consider the building of SRPM's and the lack of automatic build
dependency handling for re-builds to be bugs in the build environment.
We will eventually fix these.

$Id: Owl/doc/BUILD,v 1.1 2000/12/24 07:46:14 solar Exp $
