# $Id: Owl/packages/binutils/binutils.spec,v 1.12 2004/05/08 00:25:12 galaxy Exp $

%define BUILD_HJL 1

# Define coff_target as coff if you want to add i386-coff instead of i386-pe.
%define coff_target pe
%{?_with_coff: %{expand: %%define coff_target coff}}

Summary: A GNU collection of binary utilities.
Name: binutils
Version: 2.15.90.0.3
Release: owl0.1
License: GPL
Group: Development/Tools
URL: http://sources.redhat.com/binutils/
%if %BUILD_HJL
Source: ftp://ftp.kernel.org/pub/linux/devel/binutils/binutils-%version.tar.bz2
%else
Source: ftp://ftp.gnu.org/gnu/binutils/binutils-%version.tar.gz
%endif
Patch0: binutils-2.14.90.0.8-owl-info.diff
Patch1: binutils-2.14.90.0.8-owl-searchpath.diff
Patch10: binutils-2.15.90.0.3-rh-eh-frame-ro.diff
Patch11: binutils-2.15.90.0.3-rh-place-orphan.diff
Patch12: binutils-2.15.90.0.3-rh-relro.diff
Patch13: binutils-2.15.90.0.3-rh-tbss.diff
%ifarch sparc
Patch14: binutils-2.15.90.0.3-rh-sparc1.diff
Patch15: binutils-2.15.90.0.3-rh-sparc2.diff
%endif
PreReq: /sbin/ldconfig, /sbin/install-info
ExcludeArch: ia64
BuildRoot: /override/%name-%version

# Undefine _gnu macro - peeped from RH9 spec :)
# This affects _target_platform macro used by configure macro
%define _gnu %nil

%description
binutils is a collection of binary utilities, including ar (for creating,
modifying and extracting from archives), nm (for listing symbols from
object files), objcopy (for copying and translating object files),
objdump (for displaying information from object files), ranlib (for
generating an index for the contents of an archive), size (for listing
the section sizes of an object or archive file), strings (for listing
printable strings from files), strip (for discarding symbols), c++filt
(a filter for demangling encoded C++ symbols), addr2line (for converting
addresses to file and line).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch10 -p0
%patch11 -p0
%patch12 -p0
%patch13 -p0
%ifarch sparc
%patch14 -p0
%patch15 -p0
%endif

# Apply additional Linux patches.
%_buildshell patches/README

%build
mkdir build-%_target_platform
cd build-%_target_platform
# There're currently no pre-compiled versions of these texinfo files
# included, should uncomment if that changes.
#rm bfd/doc/bfd.info binutils/binutils.info etc/standards.info
#rm gas/doc/as.info gprof/gprof.info
#rm ld/{ld,ldint}.info
ADDITIONAL_TARGETS=""
%ifos linux
%ifarch %ix86
ADDITIONAL_TARGETS="--enable-targets=i386-linuxaout,i386-%coff_target"
%endif
%ifarch sparc sparcv9
ADDITIONAL_TARGETS="--enable-targets=sparc64-linux --enable-64-bit-bfd"
%endif
%ifarch sparcv9
%define _target_platform sparc-%_vendor-%_target_os
%endif
%endif
%if %BUILD_HJL
%define __libtoolize echo --
%endif
export AR=%__ar
export CC=%__cc
export LD=%__ld
export NM=%__nm
export RANLIB=%__ranlib
CFLAGS="%optflags" ../configure \
	%_target_platform \
	--prefix=%_prefix \
	--exec-prefix=%_exec_prefix \
	--bindir=%_bindir \
	--sbindir=%_sbindir \
	--sysconfdir=%_sysconfdir \
	--datadir=%_datadir \
	--includedir=%_includedir \
	--libdir=%_libdir \
	--libexecdir=%_libexecdir \
	--localstatedir=%_localstatedir \
	--sharedstatedir=%_sharedstatedir \
	--mandir=%_mandir \
	--infodir=%_infodir \
	--enable-shared \
	$ADDITIONAL_TARGETS
%__make tooldir=%_prefix all info

%install
rm -rf %buildroot

mkdir -p %buildroot%_prefix
cd build-%_target_platform
%makeinstall tooldir=%buildroot%_prefix
%__make prefix=%buildroot%_prefix infodir=%buildroot%_infodir \
	install-info
rm %buildroot%_mandir/man1/{dlltool,nlmconv,windres}*

install -m 644 ../include/libiberty.h %buildroot%_includedir/

chmod +x %buildroot%_libdir/lib*.so*

# Remove unpackaged files
[ -f %buildroot%_infodir/dir ] && rm %buildroot%_infodir/dir

cd ..

%post
/sbin/ldconfig
/sbin/install-info --info-dir=%_infodir %_infodir/as.info.gz
/sbin/install-info --info-dir=%_infodir %_infodir/bfd.info.gz
/sbin/install-info --info-dir=%_infodir %_infodir/binutils.info.gz
/sbin/install-info --info-dir=%_infodir %_infodir/gprof.info.gz
/sbin/install-info --info-dir=%_infodir %_infodir/ld.info.gz
/sbin/install-info --info-dir=%_infodir %_infodir/standards.info.gz

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete --info-dir=%_infodir %_infodir/as.info.gz
	/sbin/install-info --delete --info-dir=%_infodir %_infodir/bfd.info.gz
	/sbin/install-info --delete --info-dir=%_infodir %_infodir/binutils.info.gz
	/sbin/install-info --delete --info-dir=%_infodir %_infodir/gprof.info.gz
	/sbin/install-info --delete --info-dir=%_infodir %_infodir/ld.info.gz
	/sbin/install-info --delete --info-dir=%_infodir %_infodir/standards.info.gz
fi

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README
%_prefix/bin/*
%_mandir/man1/*
%_prefix/include/*
%_prefix/%_lib/ldscripts
%_prefix/%_lib/lib*
%_infodir/*.info*
%_datadir/locale/*/LC_MESSAGES/*.mo

%changelog
* Fri May 07 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 2.15.90.0.3-owl0.1
- Updated to the 2.15.90.0.3

* Mon Mar 15 2004 Solar Designer <solar@owl.openwall.com> 2.14.90.0.8-owl0.5
- Further spec file cleanups.

* Fri Mar 05 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 2.14.90.0.8-owl0.4
- Cleaned up spec a bit

* Mon Feb 23 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 2.14.90.0.8-owl0.3
- Removed unpackaged %_infodir/dir to make RPM4 happy

* Wed Jan 28 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 2.14.90.0.8-owl0.2
- Cleaned up the spec file from unneeded macros

* Sun Jan 25 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 2.14.90.0.8-owl0.1
- Included relro Red Hat patch
- Patched search logic of ldfile.c to allow more robust search of the object
to link with
- Fix a typo in spec file, causing incorrect tooldir to be used

* Wed Jan 21 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 2.14.90.0.8-owl0
- Updated to the version 2.14.90.0.8
- Corrections to this spec file according to the bundled binutils spec
- Regenerated owl-info patch
- Adopted eh-frame-ro Red Hat patch to Owl
- Made more strict checking in make_tempname() in bucomm.c
- Included Red Hat patch place-orphan (see description in the patch file).

* Mon Aug 19 2002 Michail Litvak <mci@owl.openwall.com> 2.10.1.0.4-owl2
- Deal with info dir entries such that the menu looks pretty.

* Thu Jan 24 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Thu Jan 18 2001 Solar Designer <solar@owl.openwall.com>
- 2.10.1.0.4 (due to the temporary file handling fix in objdump that is
not in the 2.10.1 release).

* Fri Nov 17 2000 Solar Designer <solar@owl.openwall.com>
- --enable-targets=sparc64-linux for sparcv9 as well as plain sparc.
- Pass plain sparc- target to configure when building for sparcv9, to
allow for the use of sparcv9 optflags while not confusing configure.

* Sat Jul 29 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- 2.10

* Tue Jul 18 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- 2.9.5.0.46
- import from spec from RH
