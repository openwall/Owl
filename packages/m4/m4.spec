# $Id: Owl/packages/m4/m4.spec,v 1.3 2001/02/06 11:41:54 mci Exp $

Summary: The GNU macro processor.
Name: 		m4
Version: 	1.4
Release: 	15owl
Copyright: 	GPL
Group:		Applications/Text
Source: 	ftp://ftp.gnu.org/gnu/m4/m4-%{version}.tar.gz
Patch0:		m4-1.4-rh-glibc.diff
Patch1:         m4-1.4-owl-format.diff
Buildroot: 	/var/rpm-buildroot/%{name}-root
Prereq: 	/sbin/install-info
Prefix: 	/usr

%description
A GNU implementation of the traditional UNIX macro processor.  M4 is
useful for writing text files which can be logically parsed, and is used
by many programs as part of their build process.  M4 has built-in
functions for including files, running shell commands, doing arithmetic,
etc.  The autoconf program needs m4 for generating configure scripts, but
not for running configure scripts.

Install m4 if you need a macro processor.

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
%makeinstall INSTALL_DATA="install -c -m644"
strip -R .comment $RPM_BUILD_ROOT/usr/bin/m4
gzip -9fn $RPM_BUILD_ROOT/%{_infodir}/*

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
* Tue Feb 06 2001 Michail Litvak <mci@owl.openwall.com>
- Fixed format bug in error
- added __attribute__ ((format(...))) for error

* Sat Jan 06 2001 Solar Designer <solar@owl.openwall.com>
- Enable mkstemp explicitly, not rely on configure.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
