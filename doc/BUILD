This is the guide on using the Owl build environment.  It is assumed
that you've read the CONCEPTS; if not, please do so before you proceed
with this document.


	/usr/src/world setup.

The build environment is pre-configured for the use of /usr/src/world
(the HOME= setting in buildworld.conf and installworld.conf).  It is
recommended that you leave this default setting and either actually
place the files in /usr/src/world or use a symlink if /usr/src is not
on a suitable device (see below for the requirements).

When building natively (that is, on Owl), the directory is already
there.  Otherwise, you need to create the directory, add pseudo-user
"build", preferably with UID 151 and GID 150 ("sources"), and make it
the owner of the directory.

Place the CVS tree into /usr/src/world.  Currently, this is done by
extracting native.tar.gz available via the FTP sites.  You will get
the "native" directory, and a Makefile symlink.

For actually building from source, place the "sources" directory in
/usr/src/world as well.

If you are not on an Owl system, yet, and want to install binary
packages, create /usr/src/world/RPMS and place the packages for your
architecture in there.  Note that you need the CVS tree even for
installing binary packages.


	Requirements.

To (re-)build Owl from source, you'll need:

at least about 500 MB free disk space under /usr/src/world for use
during the builds;

at least 64 MB of physical memory (it is possible to build on less
with sufficient swap space, but you'd better not);

at least 160 MB of virtual memory if building on and for an Alpha;

1 to 5 hours of CPU time, on a modern system (as of this writing).

And, of course, you should be running the build on Owl.  Building on
another GNU/*/Linux system is possible, but tricky and requires that
you actually convert the system into Owl with multiple iterations of
"make buildworld" and "make installworld".

Here are some build times (hours:minutes), so that you know what to
expect:

Dual Pentium III, 1 GHz, 2 GB			0:36
Dual Pentium III, 800 MHz, 512 MB		0:45
Athlon, 1 GHz, 256 MB				1:10
Dual Celeron (Mendocino), 433 MHz, 256 MB	1:20
Pentium III, 700 MHz, 192 MB			1:35
UltraSparc IIi, 400 MHz, 256 MB			3:45
Alpha 21164PC (164SX-1MB), 533 MHz, 128 MB	5:20

(Yes, gcc is this hungry and slow on Alpha.)

The build times will increase as we add more packages and update to
new versions of software already in Owl.


	Native (re-)builds.

You need to have a configured Linux 2.2 kernel in /usr/src/linux.  As
user "build", change directory to /usr/src/world and type:

	make clean && make buildworld

With the default buildworld.conf, packages will be built for oldest
flavor of the build host's architecture (see ARCHITECTURES) and the
build will attempt to use up to two processors.

buildworld.conf (as well as other *.conf's) may be edited by copying
it from native/Owl/build into /usr/src/world.  You need to remove the
symlink first, if one has previously been created for you.

All packages are built with whatever versions of libraries and build
tools are installed on the system.  Multiple iterations of buildworld
and installworld (two are sufficient most of the time) should be used
when there have been significant updates to packages used during the
builds.


	Installing binary packages.

"make installworld" will install packages found in /usr/src/world/RPMS
onto the current system, or in a new root directory of your choice (as
specified by the ROOT= setting in installworld.conf).  By default, the
packages will be installed into /owl.

"make installworld" should be run as root.

Currently, it is possible to convert an existing Red Hat Linux 6.x
installation into Owl with "make installworld" and some manual help.
Be sure to read and understand all of installorder.conf before you try
this.  In particular, your kernel should be no longer a part of an RPM
package by the time you convert the system into Owl.


	Re-building individual packages.

To re-build an Owl package: remove the SRPM in /usr/src/world/SRPMS,
remove all the binary packages produced from this source package in
/usr/src/world/RPMS, type "make buildworld".

We do consider the building of SRPM's and the lack of automatic build
dependency handling for re-builds to be bugs in the build environment.
We will eventually fix these.

$Id: Owl/doc/BUILD,v 1.14 2002/06/08 15:36:27 solar Exp $
