# $Id: Owl/packages/make/make.spec,v 1.7 2004/09/10 07:25:18 galaxy Exp $

Summary: A GNU tool which simplifies the build process for users.
Name: make
Version: 3.79.1
Release: owl4
License: GPL
Group: Development/Tools
Source: ftp://ftp.gnu.org/gnu/make/make-%version.tar.gz
PreReq: /sbin/install-info
Prefix: %_prefix
BuildRoot: /override/%name-%version

%description
A GNU tool for controlling the generation of executables and other
non-source files of a program from the program's source files.  The
make utility automatically determines which pieces of a large
program need to be recompiled, and issues commands to recompile them.

%prep
%setup -q

%build
export ac_cv_func_mkstemp=yes \
%configure
make

%install
rm -f $RPM_BUILD_ROOT
%makeinstall
ln -sf make $RPM_BUILD_ROOT%_bindir/gmake

# XXX: (GM): Remove unpackaged files (check later)
rm %buildroot%_infodir/dir
rm %buildroot%_datadir/locale/de/LC_MESSAGES/make.mo
rm %buildroot%_datadir/locale/es/LC_MESSAGES/make.mo
rm %buildroot%_datadir/locale/fr/LC_MESSAGES/make.mo
rm %buildroot%_datadir/locale/ja/LC_MESSAGES/make.mo
rm %buildroot%_datadir/locale/ko/LC_MESSAGES/make.mo
rm %buildroot%_datadir/locale/nl/LC_MESSAGES/make.mo
rm %buildroot%_datadir/locale/pl/LC_MESSAGES/make.mo
rm %buildroot%_datadir/locale/pt_BR/LC_MESSAGES/make.mo
rm %buildroot%_datadir/locale/ru/LC_MESSAGES/make.mo

%post
/sbin/install-info %_infodir/make.info.gz %_infodir/dir \
	--entry="* GNU make: (make).                             The GNU make utility."

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/make.info.gz %_infodir/dir \
		--entry="* GNU make: (make).                             The GNU make utility."
fi

%files
%defattr(-,root,root)
%doc NEWS README
%_bindir/*
%_mandir/man*/*
%_infodir/*.info*

%changelog
* Mon Aug 19 2002 Michail Litvak <mci@owl.openwall.com> 3.79.1-owl4
- Deal with info dir entries such that the menu looks pretty.

* Wed Feb 06 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions

* Sat Jan 06 2001 Solar Designer <solar@owl.openwall.com>
- Enable mkstemp explicitly, not rely on configure.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import spec from RH rawhide
