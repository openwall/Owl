# $Id: Owl/packages/gdb/gdb.spec,v 1.2 2001/07/11 08:39:57 mci Exp $

Summary: A GNU source-level debugger for C, C++ and Fortran.
Name: gdb
Version: 5.0
Release: 8
Copyright: GPL
Group: Development/Debuggers
Source0: ftp://sourceware.cygnus.com/pub/gdb/releases/gdb-%{version}.tar.bz2
Patch0: gdb-5.0-pld-procfs.diff
Patch1: gdb-5.0-pld-info.diff
Patch2: gdb-5.0-pld-gettext.diff
Patch3: gdb-5.0-pld-ncurses.diff
Patch4: gdb-5.0-pld-readline.diff
Patch5: gdb-5.0-rh-symchanges.diff
Patch6: gdb-5.0-rh-alpha.diff
Buildroot: /var/rpm-buildroot/%{name}-root
BuildRequires: ncurses-devel >= 5.0
BuildRequires: readline-devel >= 4.1
Prereq: /sbin/install-info

%description
Gdb is a full featured, command driven debugger. Gdb allows you to
trace the execution of programs and examine their internal state at
any time.  Gdb works for C and C++ compiled with the GNU C compiler
gcc.

If you are going to develop C and/or C++ programs and use the GNU gcc
compiler, you may want to install gdb to help you debug your
programs.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build

pushd gdb
aclocal
autoconf
popd

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
        includedir=$RPM_BUILD_ROOT%{_includedir} \
        libdir=$RPM_BUILD_ROOT%{_libdir} \
	infodir=$RPM_BUILD_ROOT%{_infodir} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_infodir}/dir $RPM_BUILD_ROOT%{_infodir}/dir.info*

#These are part of binutils

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

# don't include the files in include, they are part of binutils

%changelog
* Wed Jul 11 2001 Michail Litvak <mci@owl.openwall.com>
- spec imported from RH with additions from PLD and SuSe
- patches from PLD and RH
