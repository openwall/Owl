# $Id: Owl/packages/binutils/binutils.spec,v 1.11 2003/10/29 18:25:46 solar Exp $

%define BUILD_HJL 1

Summary: A GNU collection of binary utilities.
Name: binutils
Version: 2.10.1.0.4
Release: owl2
License: GPL
Group: Development/Tools
URL: http://sources.redhat.com/binutils/
%if %BUILD_HJL
Source: ftp://ftp.valinux.com/pub/support/hjl/binutils/binutils-%version.tar.gz
%else
Source: ftp://ftp.gnu.org/gnu/binutils/binutils-%version.tar.gz
%endif
Patch: binutils-2.10.1.0.4-owl-info.diff
PreReq: /sbin/ldconfig, /sbin/install-info
ExcludeArch: ia64
BuildRoot: /override/%name-%version

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
%patch -p1

%build
# There're currently no pre-compiled versions of these texinfo files
# included, should uncomment if that changes.
#rm bfd/doc/bfd.info binutils/binutils.info etc/standards.info
#rm gas/doc/{gasp,as}.info gprof/gprof.info
#rm ld/{ld,ldint}.info
ADDITIONAL_TARGETS=""
%ifos linux
%ifarch sparc sparcv9
ADDITIONAL_TARGETS="--enable-targets=sparc64-linux"
%endif
%ifarch sparcv9
%define _target_platform sparc-%_vendor-%_target_os
%endif
%endif
%if %BUILD_HJL
%define __libtoolize echo --
%endif
%configure --enable-shared $ADDITIONAL_TARGETS
make tooldir=%{_prefix}usr all info

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%_prefix
%makeinstall
make prefix=$RPM_BUILD_ROOT%_prefix infodir=$RPM_BUILD_ROOT%_infodir \
	install-info
rm $RPM_BUILD_ROOT%_mandir/man1/nlmconv.1

install -m 644 include/libiberty.h $RPM_BUILD_ROOT%_prefix/include/

chmod +x $RPM_BUILD_ROOT%_prefix/%_lib/lib*.so*

%post
/sbin/ldconfig
/sbin/install-info %_infodir/as.info.gz %_infodir/dir
/sbin/install-info %_infodir/bfd.info.gz %_infodir/dir
/sbin/install-info %_infodir/binutils.info.gz %_infodir/dir
/sbin/install-info %_infodir/gasp.info.gz %_infodir/dir
/sbin/install-info %_infodir/gprof.info.gz %_infodir/dir
/sbin/install-info %_infodir/ld.info.gz %_infodir/dir
/sbin/install-info %_infodir/standards.info.gz %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/as.info.gz %_infodir/dir
	/sbin/install-info --delete %_infodir/bfd.info.gz %_infodir/dir
	/sbin/install-info --delete %_infodir/binutils.info.gz %_infodir/dir
	/sbin/install-info --delete %_infodir/gasp.info.gz %_infodir/dir
	/sbin/install-info --delete %_infodir/gprof.info.gz %_infodir/dir
	/sbin/install-info --delete %_infodir/ld.info.gz %_infodir/dir
	/sbin/install-info --delete %_infodir/standards.info.gz %_infodir/dir
fi

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README
%_prefix/bin/*
%_mandir/man1/*
%_prefix/include/*
%_prefix/%_lib/*
%_infodir/*.info*

%changelog
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
