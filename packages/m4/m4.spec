# $Id: Owl/packages/m4/m4.spec,v 1.4 2002/02/06 07:50:06 mci Exp $

Summary: The GNU macro processor.
Name: m4
Version: 1.4
Release: owl15
License: GPL
Group: Applications/Text
Source: ftp://ftp.gnu.org/gnu/m4/m4-%{version}.tar.gz
Patch0: m4-1.4-rh-glibc.diff
Patch1: m4-1.4-owl-format.diff
PreReq: /sbin/install-info
Prefix: %{_prefix}
BuildRoot: /override/%{name}-%{version}

%description
A GNU implementation of the traditional UNIX macro processor.  m4 is
useful for writing text files which can be logically parsed, and is used
by many programs as part of their build process.  m4 has built-in
functions for including files, running shell commands, doing arithmetic,
etc.  The autoconf program needs m4 for generating configure scripts, but
not for running configure scripts.

%prep
rm -rf $RPM_BUILD_ROOT

%setup
%patch0 -p1
%patch1 -p1

%build
autoconf
export ac_cv_func_mkstemp=yes \
%configure
make CFLAGS="$RPM_OPT_FLAGS" LDFLAGS=-s

%install
%makeinstall INSTALL_DATA="install -c -m 644"

%files
%defattr(-,root,root)
%doc NEWS README
%{_bindir}/m4
%{_infodir}/*.info*

%post
/sbin/install-info %{_infodir}/m4.info.gz %{_infodir}/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/m4.info.gz %{_infodir}/dir
fi

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Feb 06 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions

* Tue Feb 06 2001 Michail Litvak <mci@owl.openwall.com>
- Fixed format bug in error
- added __attribute__ ((format(...))) for error

* Sat Jan 06 2001 Solar Designer <solar@owl.openwall.com>
- Enable mkstemp explicitly, not rely on configure.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
