# $Owl: Owl/packages/mkisofs/Attic/mkisofs.spec,v 1.1 2007/01/05 18:24:36 ldv Exp $

Summary: Creates an hybrid ISO9660/JOLIET/HFS filesystem image with optional Rock Ridge attributes.
Name: mkisofs
Version: 2.01.01a23
Release: owl1
Epoch: 9
License: GPL/CDDL/BSD
Group: Applications/Archiving
URL: http://cdrecord.berlios.de/old/private/cdrecord.html
Source: ftp://ftp.berlios.de/pub/cdrecord/alpha/cdrtools-%version.tar.bz2
Patch0: mkisofs-2.01-rh-bound.diff
Patch1: mkisofs-2.01.01-owl-debug.diff
Patch2: mkisofs-2.01.01-owl-rcfile.diff
Patch3: mkisofs-2.01.01-owl-man.diff
BuildRoot: /override/%name-%version

%description
The mkisofs program is used to generate an ISO9660/JOLIET/HFS
filesystem image.  It takes a snapshot of a given trusted directory
tree and generates a binary image of the tree which will correspond
to an ISO9660/JOLIET/HFS filesystem when written to a block device.

Note that mkisofs is not designed to handle untrusted directories.

%prep
%setup -q -n cdrtools-2.01.01
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# Fix GNU make support
sed -i 's/^include/-&/' RULES/*
sed -i '/^__gmake_warn/d' RULES/mk-gmake.id

# Disable build of profiled libraries
grep -lZ 'lib[a-z]\+_p\.mk' lib*/Makefile |
	xargs -r0 sed -i 's/lib[a-z]\+_p\.mk//' --

cd mkisofs
# mkisofs does not require librscg
sed -i 's/-lrscg //' Makefile

# Disable libfind
sed -i 's/-DUSE_FIND//;s/-lfind //' Makefile

# Disable libdeflt and libscg
sed -i 's/\(defaults\|cd_misc\|scsi\|scsi_cdr\|modes\)\.c//g' Makefile
sed -i 's/-DUSE_SCG//;s/-l\(deflt\|scg\) //g' Makefile
sed -i 's/^#ifdef.*USE_SCG/#if 1/' scsi.h

# Move manpage to proper section
sed -i 's/MKISOFS 8/MKISOFS 1/' mkisofs.8

# Disable build of unneeded cdrecord stuff
libs="$(sed -n '/^LIBS=/ s/[^-]*-l\([a-z]\+\)[^-]*/\1\\|/pg' Makefile)\$"
cd ../TARGETS
ls 5* |sed -n '/^55mkisofs$/!p' |
	xargs -r rm -fv -- [6-9]*
ls 4* |sed -n "/^4[0-9]lib\\($libs\\)/!p" |
	xargs -r rm -fv --

%build
%__make CC=%__cc COPTOPT="%optflags" CONFFLAGS="--prefix=%prefix" \
	LDCC=%__cc LDPATH=

%install
rm -rf %buildroot
install -pDm755 mkisofs/OBJ/*/mkisofs %buildroot%_bindir/mkisofs
install -pDm644 mkisofs/mkisofs.8 %buildroot%_mandir/man1/mkisofs.1

%files
%defattr(-,root,root)
%_bindir/*
%_mandir/man?/*
%doc COPYING CDDL*

%changelog
* Fri Jan 05 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.01.01a23-owl1
- Initial build for Openwall GNU/*/Linux.
