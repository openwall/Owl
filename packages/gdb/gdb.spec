# $Id: Owl/packages/gdb/gdb.spec,v 1.6 2001/07/12 03:08:04 solar Exp $

Summary: A GNU source-level debugger for C, C++ and Fortran.
Name: gdb
Version: 5.0
Release: 8owl
License: GPL
Group: Development/Debuggers
Source0: ftp://sourceware.cygnus.com/pub/gdb/releases/gdb-%{version}.tar.bz2
Patch0: gdb-5.0-pld-procfs.diff
Patch1: gdb-5.0-pld-info.diff
Patch2: gdb-5.0-pld-gettext.diff
Patch3: gdb-5.0-pld-ncurses.diff
Patch4: gdb-5.0-pld-readline.diff
Patch5: gdb-5.0-rh-symchanges.diff
Patch6: gdb-5.0-rh-alpha.diff
Patch7: gdb-5.0-owl-warnings.diff
Buildroot: /var/rpm-buildroot/%{name}-root
BuildRequires: ncurses-devel >= 5.0
BuildRequires: readline-devel >= 4.1
Prereq: /sbin/install-info

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

%build

pushd gdb
aclocal
autoconf
popd

export ac_cv_func_vfork_works=no \
%configure \
	--enable-nls \
	--without-included-gettext \
	--enable-gdbmi \
	--with-cpu=%{_target_cpu} \
%ifnarch alpha
	--with-mmalloc \
%endif
	--with-mmap

make
make info

%install
rm -rf $RPM_BUILD_ROOT

make install install-info \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
        includedir=$RPM_BUILD_ROOT%{_includedir} \
        libdir=$RPM_BUILD_ROOT%{_libdir} \
	infodir=$RPM_BUILD_ROOT%{_infodir} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_infodir}/dir $RPM_BUILD_ROOT%{_infodir}/dir.info*

# These are part of binutils
rm -f $RPM_BUILD_ROOT%{_infodir}/bfd*
rm -f $RPM_BUILD_ROOT%{_infodir}/standard*
rm -rf $RPM_BUILD_ROOT/usr/include/
rm -rf $RPM_BUILD_ROOT/usr/lib/lib{bfd*,opcodes*}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/gdb.info %{_infodir}/dir
/sbin/install-info %{_infodir}/gdbint.info.gz %{_infodir}/dir
/sbin/install-info %{_infodir}/mmalloc.info.gz %{_infodir}/dir
/sbin/install-info %{_infodir}/stabs.info.gz %{_infodir}/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/gdb.info.gz %{_infodir}/dir
	/sbin/install-info --delete %{_infodir}/gdbint.info.gz %{_infodir}/dir
	/sbin/install-info --delete %{_infodir}/mmalloc.info.gz %{_infodir}/dir
	/sbin/install-info --delete %{_infodir}/stabs.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
%doc COPYING COPYING.LIB README gdb/NEWS
/usr/bin/*
%{_mandir}/*/*
%{_infodir}/gdb.info*
%{_infodir}/gdbint.info*
%{_infodir}/stabs.info*
%{_infodir}/mmalloc.info*

%changelog
* Thu Jul 12 2001 Solar Designer <solar@owl.openwall.com>
- Corrected the package description.
- Disabled the (incorrect) use of vfork.
- Fixed some harmless compiler warnings.

* Wed Jul 11 2001 Michail Litvak <mci@owl.openwall.com>
- spec imported from RH with additions from PLD and SuSE
- patches from PLD and RH
