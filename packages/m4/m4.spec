# $Id: Owl/packages/m4/m4.spec,v 1.2 2001/01/06 14:42:39 solar Exp $

Summary: The GNU macro processor.
Name: 		m4
Version: 	1.4
Release: 	14owl
Copyright: 	GPL
Group:		Applications/Text
Source: 	ftp://ftp.gnu.org/gnu/m4/m4-%{version}.tar.gz
Patch: 		m4-1.4-rh-glibc.diff
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
%patch -p1

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
* Sat Jan 06 2001 Solar Designer <solar@owl.openwall.com>
- Enable mkstemp explicitly, not rely on configure.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
