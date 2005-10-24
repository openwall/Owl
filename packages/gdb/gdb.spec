# $Id: Owl/packages/gdb/gdb.spec,v 1.22 2005/10/24 03:06:23 solar Exp $

Summary: A GNU source-level debugger for C, C++ and Fortran.
Name: gdb
Version: 6.3
Release: owl1
License: GPL
Group: Development/Debuggers
URL: http://www.gnu.org/software/gdb/
Source: ftp://ftp.gnu.org/gnu/gdb/gdb-%version.tar.bz2
Patch0: gdb-6.3-alt-readline.diff
Patch1: gdb-6.3-owl-info.diff
Patch2: gdb-6.3-deb-thread-db.diff
Patch3: gdb-6.3-deb-tracepoint.diff
Patch4: gdb-6.3-deb-cp_pass_by_reference.diff
Patch5: gdb-6.3-deb-tracefork.diff
Patch6: gdb-6.3-deb-bfd_close.diff
Patch7: gdb-6.3-rh-inheritance.diff
Patch8: gdb-6.3-rh-gdbtypes.diff
Patch9: gdb-6.3-cvs-20050526-bfd.diff
Patch10: gdb-6.3-gentoo-alt-gdbinit.diff
PreReq: /sbin/install-info
BuildRequires: ncurses-devel >= 5.0
BuildRequires: readline-devel >= 4.3
BuildRequires: libtool, texinfo
BuildRoot: /override/%name-%version

%description
GDB is a full featured, command driven debugger.  GDB allows you to
trace the execution of programs and examine their internal state at
any time.  The debugger is most effective when used together with a
supported compiler, such as those from the GNU Compiler Collection.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

%build
# readline texinfo files are needed to generate gdb documentation
mv readline/doc readline-doc

rm -rf readline dejagnu tcl expect
rm gdb/doc/*.info*

export ac_cv_func_vfork_works=no
%configure \
	--host=%{_target_platform} \
	--build=%{_target_platform} \
	--without-included-gettext

%__make
%__make info

%install
rm -rf %buildroot

%__make install install-info \
	prefix=%_prefix \
	bindir=%_bindir \
	includedir=%_includedir \
	libdir=%_libdir \
	infodir=%_infodir \
	mandir=%_mandir \
	DESTDIR=%buildroot

# These are part of binutils
rm -r %buildroot%_includedir
rm %buildroot%_infodir/{annotate,bfd,configure,standard}*
rm %buildroot%_libdir/lib{bfd,iberty,opcodes}*

# Remove unpackaged files if any
rm -f %buildroot%_infodir/dir
rm %buildroot%_datadir/locale/*/LC_MESSAGES/{bfd,opcodes}.mo

%pre
if [ $1 -ge 1 -a -f %_infodir/mmalloc.info.gz ]; then
	/sbin/install-info --delete %_infodir/mmalloc.info %_infodir/dir ||:
fi

%post
/sbin/install-info %_infodir/gdb.info %_infodir/dir
/sbin/install-info %_infodir/gdbint.info %_infodir/dir
/sbin/install-info %_infodir/stabs.info %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/gdb.info %_infodir/dir
	/sbin/install-info --delete %_infodir/gdbint.info %_infodir/dir
	/sbin/install-info --delete %_infodir/stabs.info %_infodir/dir
fi

%files
%defattr(-,root,root)
%doc COPYING COPYING.LIB README gdb/NEWS
%_bindir/*
%_mandir/*/*
%_infodir/gdb.info*
%_infodir/gdbint.info*
%_infodir/stabs.info*

%changelog
* Sun May 29 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 6.3-owl1
- Updated to 6.3
- Imported a bunch of patches from Debian's gdb-6.3-5 package.
- Backported patch from upstream that adds sanity checks to BFD library
(CAN-2005-1704).
- Imported patch from Gentoo that fixes .gdbinit issue (CAN-2005-1705).
- Corrected info files installation.

* Fri Jan 15 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 6.1.1-owl2
- Used %%__make macro instead of plain "make".

* Thu Jul 08 2004 Michail Litvak <mci-at-owl.openwall.com> 6.1.1-owl1
- 6.1.1

* Tue Mar 09 2004 Michail Litvak <mci-at-owl.openwall.com> 6.0-owl0.1
- 6.0

* Thu Feb 26 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 5.0-owl10.1
- Disabled autoconf and other regeneration programs due to conflict
with new autotools.

* Fri Feb 20 2004 Michail Litvak <mci-at-owl.openwall.com> 5.0-owl10
- Fixed building with new readline 4.3.

* Mon Aug 19 2002 Michail Litvak <mci-at-owl.openwall.com> 5.0-owl9
- Deal with info dir entries such that the menu looks pretty.

* Fri Feb 01 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Thu Jul 12 2001 Solar Designer <solar-at-owl.openwall.com>
- Corrected the package description.
- Corrected Alpha builds.
- Disabled the (incorrect) uses of vfork.
- Fixed some harmless compiler warnings.

* Wed Jul 11 2001 Michail Litvak <mci-at-owl.openwall.com>
- spec imported from RH with additions from PLD and SuSE
- patches from PLD and RH
