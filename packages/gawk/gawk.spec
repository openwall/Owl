# $Id: Owl/packages/gawk/gawk.spec,v 1.3 2002/02/01 10:45:17 mci Exp $

Summary: The GNU version of the awk text processing utility.
Name: gawk
Version: 3.0.6
Release: owl2
License: GPL
Group: Applications/Text
Source0: ftp://ftp.gnu.org/gnu/gawk/gawk-%{version}.tar.gz
Source1: ftp://ftp.gnu.org/gnu/gawk/gawk-%{version}-ps.tar.gz
# The "unaligned" patch should be obsolete with glibc 2.1+
Patch0: gawk-3.0-rh-unaligned.diff
Patch1: gawk-3.0.6-jh-owl-igawk-tmp.diff
PreReq: /sbin/install-info
Requires: mktemp
BuildRequires: texinfo
BuildRoot: /override/%{name}-%{version}

%description
The gawk packages contains the GNU version of awk, a text processing
utility.  Awk interprets a special-purpose programming language to do
quick and easy text pattern matching and reformatting jobs.

%prep
%setup -q -b 1
%patch0 -p1
%patch1 -p1

%build
rm -f doc/gawk.info awklib/eg/prog/igawk.sh
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall bindir=$RPM_BUILD_ROOT/bin \
	mandir=${RPM_BUILD_ROOT}%{_mandir}/man1 \
	libexecdir=${RPM_BUILD_ROOT}%{_libexecdir}/awk \
	datadir=${RPM_BUILD_ROOT}%{_datadir}/awk

cd $RPM_BUILD_ROOT
rm -f .%{_infodir}/dir
mkdir -p .%{_prefix}/bin
ln -sf gawk.1.gz .%{_mandir}/man1/awk.1.gz
cd bin
ln -sf ../../bin/gawk ../usr/bin/awk
ln -sf ../../bin/gawk ../usr/bin/gawk

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/gawk.info.gz %{_infodir}/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/gawk.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root,-)
%doc README COPYING ACKNOWLEDGMENT FUTURES INSTALL LIMITATIONS NEWS PORTS
%doc README_d POSIX.STD doc/gawk.ps doc/awkcard.ps
/bin/*
/usr/bin/*
%{_mandir}/man1/*
%{_infodir}/gawk.info*
%{_libexecdir}/awk
%{_datadir}/awk

%changelog
* Fri Feb 01 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions.

* Sun May 27 2001 Solar Designer <solar@owl.openwall.com>
- Patched unsafe temporary file handling in igawk, based on report and
patch from Jarno Huuskonen.
- Make sure gawk.info and igawk.sh are re-generated from gawk.texi on
package builds.

* Sun Oct  1 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import spec from RH
