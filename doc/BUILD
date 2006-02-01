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

Place the CVS tree into /usr/src/world.  The easiest way to do it is
by extracting native.tar.gz available via the FTP mirrors.  You will
get the "native" directory, and a Makefile symlink.

For actually building from source, place the "sources" directory in
/usr/src/world as well.

If you are not on an Owl system, yet, and want to install binary
packages, create /usr/src/world/RPMS and place the packages for your
architecture in there.  Note that you need the CVS tree even for
installing binary packages.


	Requirements.

To (re-)build Owl from source, you'll need:

at least 1 GB free disk space under /usr/src/world for use during the
builds;

at least 64 MB of physical memory (it is possible to build on less
with sufficient swap space, but you'd better not);

at least 200 MB of virtual memory;

a few hours of CPU time, on a modern system.

And, of course, you should be running the build on Owl.  Building on
another GNU/*/Linux system is possible, but tricky and requires that
you actually convert the system into Owl with multiple iterations of
"make buildworld" and "make installworld".

Here are some build times (hours:minutes) for Owl-current, so that you
know what to expect:

Dual Pentium 4 Xeon, HT (4-way MP), 2.8 GHz, 2 GB		0:50
Dual Pentium III, 600 MHz, 512 MB				3:35
UltraSparc IIi, 400 MHz, 256 MB					10:00
Alpha 21164PC (164SX-1MB), 533 MHz, 128 MB			14:00

(Yes, gcc is this hungry and slow on Alpha.)

The build times will increase as we add more packages and update to
new versions of software already in Owl.


	Native (re-)builds.

You need to have a configured Linux 2.4.x kernel in /usr/src/linux.
As user "build", change directory to /usr/src/world and type:

	make clean && make buildworld

With the default buildworld.conf, packages will be built for oldest
flavor of the build host's architecture (see ARCHITECTURES) and the
build will attempt to use all system processors.

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


	(Re-)building individual packages.

Individual packages may be built or re-built with "make PACKAGE=name",
where "name" is the name of the source package.  For foreign packages
(SRPMs) built with the Owl build environment you also need to include
the version number part in "name".

$Owl: Owl/doc/BUILD,v 1.34 2006/02/01 17:53:09 solar Exp $
