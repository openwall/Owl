# $Id: Owl/packages/libtool/libtool.spec,v 1.4 2002/02/05 19:50:16 mci Exp $

Summary: The GNU libtool, which simplifies the use of shared libraries.
Name: libtool
Version: 1.3.5
Release: owl9
License: GPL
Group: Development/Tools
Source: ftp://ftp.gnu.org/gnu/libtool/libtool-%{version}.tar.gz
Patch1: libtool-1.2f-rh-cache.diff
Patch2: libtool-1.3.5-rh-mktemp.diff
Patch3: libtool-1.3.5-rh-nonneg.diff
PreReq: /sbin/install-info, autoconf, automake, m4, perl
Prefix: %{_prefix}
Requires: libtool-libs = %{version}-%{release}, mktemp
Buildroot: /override/%{name}-%{version}

%description
The libtool package contains the GNU libtool, a set of shell scripts
which automatically configure UNIX and UNIX-like architectures to
generically build shared libraries.  libtool provides a consistent,
portable interface which simplifies the process of using shared
libraries.

%package libs
Summary: Runtime libraries for GNU libtool.
Group: System Environment/Libraries

%description libs
The libtool-libs package contains the runtime libraries from GNU
libtool.  GNU libtool uses these libraries to provide portible dynamic
loading of shared libraries.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
# define libtoolize to true, in case configure calls it
%define __libtoolize /bin/true
%configure

make -k -C doc
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}

%makeinstall

cp install-sh missing mkinstalldirs demo

chmod -R u=rwX,go=rX demo

cd $RPM_BUILD_ROOT
# XXX remove zero length file
rm -f .%{_datadir}/libtool/libltdl/stamp-h.in
# XXX forcibly break hardlinks
mv .%{_datadir}/libtool/libltdl .%{_datadir}/libtool/libltdl-X
mkdir .%{_prefix}/share/libtool/libltdl
cp .%{_datadir}/libtool/libltdl-X/* .%{_datadir}/libtool/libltdl
rm -rf .%{_prefix}/share/libtool/libltdl-X

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/libtool.info.gz %{_infodir}/dir
# XXX hack alert
cd %{_defaultdocdir}/libtool-%{version}/demo || \
cd %{_prefix}/doc/libtool-%{version}/demo || exit 0
umask 022
libtoolize --copy --force
aclocal
autoheader
automake
autoconf

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/libtool.info.gz %{_infodir}/dir
# XXX hack alert
	cd %{_defaultdocdir}/libtool-%{version}/demo || \
	cd %{_prefix}/doc/libtool-%{version}/demo || exit 0
	rm -f config.{guess,h.in,sub} lt{config,main.sh}
fi

%files
%defattr(-,root,root)
%doc AUTHORS COPYING INSTALL NEWS README
%doc THANKS TODO ChangeLog demo
%{_bindir}/*
%{_infodir}/libtool.info*
%{_includedir}/ltdl.h
%{_datadir}/libtool
%{_libdir}/libltdl.so
%{_libdir}/libltdl.*a
%{_datadir}/aclocal/libtool.m4

%files libs
%defattr(-,root,root)
%{_libdir}/libltdl.so.*

%changelog
* Tue Feb 05 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions

* Sun May 06 2001 Solar Designer <solar@owl.openwall.com>
- Ensure proper permissions on demo (installed as documentation).

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
