# $Id: Owl/packages/gdb/gdb.spec,v 1.17 2004/11/23 22:40:45 mci Exp $

Summary: A GNU source-level debugger for C, C++ and Fortran.
Name: gdb
Version: 6.1.1
Release: owl1
License: GPL
Group: Development/Debuggers
URL: http://www.gnu.org/software/gdb/
Source: ftp://ftp.gnu.org/pub/gnu/gdb/gdb-%version.tar.bz2
Patch0: gdb-6.1.1-deb-owl-readline.diff
Patch1: gdb-6.1.1-owl-info.diff
PreReq: /sbin/install-info
BuildRequires: ncurses-devel >= 5.0
BuildRequires: readline-devel >= 4.3
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

%build
rm gdb/doc/{gdb,stabs,gdbint}.info
rm mmalloc/mmalloc.info

export ac_cv_func_vfork_works=no
./configure \
	--prefix=%_prefix \
	--sysconfdir=%_sysconfdir \
	--mandir=%_mandir \
	--infodir=%_infodir \
	--enable-nls \
	--without-included-gettext \
	--enable-gdbmi \
	%_target_platform

make
make info

%install
rm -rf %buildroot

make install install-info \
	prefix=%_prefix \
	bindir=%_bindir \
	includedir=%_includedir \
	libdir=%_libdir \
	infodir=%_infodir \
	mandir=%_mandir \
	DESTDIR=%buildroot

# These are part of binutils
rm %buildroot%_infodir/bfd*
rm %buildroot%_infodir/standard*
rm -r %buildroot/usr/include/
rm -r %buildroot/usr/lib/lib{bfd*,opcodes*}

# XXX: (GM): Remove unpackaged files (check later)
rm %buildroot%_libdir/libiberty.a
rm %buildroot%_libdir/libmmalloc.a
rm %buildroot%_infodir/annotate.info*
rm %buildroot%_infodir/configure.info*
rm %buildroot%_infodir/dir
rm %buildroot%_datadir/locale/da/LC_MESSAGES/bfd.mo
rm %buildroot%_datadir/locale/da/LC_MESSAGES/opcodes.mo
rm %buildroot%_datadir/locale/de/LC_MESSAGES/opcodes.mo
rm %buildroot%_datadir/locale/es/LC_MESSAGES/bfd.mo
rm %buildroot%_datadir/locale/es/LC_MESSAGES/opcodes.mo
rm %buildroot%_datadir/locale/fr/LC_MESSAGES/bfd.mo
rm %buildroot%_datadir/locale/fr/LC_MESSAGES/opcodes.mo
rm %buildroot%_datadir/locale/id/LC_MESSAGES/opcodes.mo
rm %buildroot%_datadir/locale/ja/LC_MESSAGES/bfd.mo
rm %buildroot%_datadir/locale/nl/LC_MESSAGES/opcodes.mo
rm %buildroot%_datadir/locale/pt_BR/LC_MESSAGES/opcodes.mo
rm %buildroot%_datadir/locale/ro/LC_MESSAGES/bfd.mo
rm %buildroot%_datadir/locale/ro/LC_MESSAGES/opcodes.mo
rm %buildroot%_datadir/locale/sv/LC_MESSAGES/bfd.mo
rm %buildroot%_datadir/locale/sv/LC_MESSAGES/opcodes.mo
rm %buildroot%_datadir/locale/tr/LC_MESSAGES/bfd.mo
rm %buildroot%_datadir/locale/tr/LC_MESSAGES/opcodes.mo
rm %buildroot%_datadir/locale/zh_CN/LC_MESSAGES/bfd.mo

%post
/sbin/install-info %_infodir/gdb.info %_infodir/dir
/sbin/install-info %_infodir/gdbint.info.gz %_infodir/dir
/sbin/install-info %_infodir/mmalloc.info.gz %_infodir/dir
/sbin/install-info %_infodir/stabs.info.gz %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/gdb.info.gz %_infodir/dir
	/sbin/install-info --delete %_infodir/gdbint.info.gz %_infodir/dir
	/sbin/install-info --delete %_infodir/mmalloc.info.gz %_infodir/dir
	/sbin/install-info --delete %_infodir/stabs.info.gz %_infodir/dir
fi

%files
%defattr(-,root,root)
%doc COPYING COPYING.LIB README gdb/NEWS
%_bindir/*
%_mandir/*/*
%_infodir/gdb.info*
%_infodir/gdbint.info*
%_infodir/stabs.info*
%_infodir/mmalloc.info*

%changelog
* Thu Jul 08 2004 Michail Litvak <mci@owl.openwall.com> 6.1.1-owl1
- 6.1.1

* Tue Mar 09 2004 Michail Litvak <mci@owl.openwall.com> 6.0-owl0.1
- 6.0

* Thu Feb 26 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 5.0-owl10.1
- Disabled autoconf and other regeneration programs due to conflict
with new autotools.

* Fri Feb 20 2004 Michail Litvak <mci@owl.openwall.com> 5.0-owl10
- Fixed building with new readline 4.3.

* Mon Aug 19 2002 Michail Litvak <mci@owl.openwall.com> 5.0-owl9
- Deal with info dir entries such that the menu looks pretty.

* Fri Feb 01 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions.

* Thu Jul 12 2001 Solar Designer <solar@owl.openwall.com>
- Corrected the package description.
- Corrected Alpha builds.
- Disabled the (incorrect) uses of vfork.
- Fixed some harmless compiler warnings.

* Wed Jul 11 2001 Michail Litvak <mci@owl.openwall.com>
- spec imported from RH with additions from PLD and SuSE
- patches from PLD and RH
