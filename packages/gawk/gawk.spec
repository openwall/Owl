# $Id: Owl/packages/gawk/gawk.spec,v 1.6 2002/07/23 13:18:27 mci Exp $

%define BUILD_PROFILE 0

Summary: The GNU version of the awk text processing utility.
Name: gawk
Version: 3.1.1
Release: owl2
License: GPL
Group: Applications/Text
Source0: ftp://ftp.gnu.org/gnu/gawk/gawk-%{version}.tar.gz
Source1: ftp://ftp.gnu.org/gnu/gawk/gawk-%{version}-ps.tar.gz
Patch0: gawk-3.1.1-eggert-tmp.diff
PreReq: /sbin/install-info
BuildRequires: texinfo >= 4.2
BuildRoot: /override/%{name}-%{version}

%description
The gawk package contains the GNU version of awk, a text processing
utility.  awk interprets a special-purpose programming language to do
quick and easy text pattern matching and reformatting jobs.

%if %BUILD_PROFILE
%package profile
Summary: The GNU version of the awk text processing utility with
profiling support.
Group: Development/Libraries

%description profile
The gawk-profile package includes pgawk (profiling gawk).
pgawk is identical in every way to gawk, except that when it has
finished running, it creates a profile of your program with program
execution counts.
%endif

%prep
%setup -q -b 1
%patch0 -p1

%{expand:%%define optflags %optflags -Wall}

%build
rm doc/gawk.info awklib/stamp-eg
%configure
pushd awklib
make stamp-eg
popd
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall bindir=$RPM_BUILD_ROOT/bin \
	mandir=${RPM_BUILD_ROOT}%{_mandir} \
	libexecdir=${RPM_BUILD_ROOT}%{_libexecdir}/awk \
	datadir=${RPM_BUILD_ROOT}%{_datadir}/awk

gzip -9n doc/*.ps

cd $RPM_BUILD_ROOT
rm -f .%{_infodir}/dir
mkdir -p .%{_prefix}/bin
ln -sf gawk.1.gz .%{_mandir}/man1/awk.1.gz
cd bin
ln -sf ../../bin/gawk ../usr/bin/awk
ln -sf ../../bin/gawk ../usr/bin/gawk
mv $RPM_BUILD_ROOT/bin/pgawk $RPM_BUILD_ROOT/usr/bin/

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
%doc README COPYING FUTURES LIMITATIONS NEWS PROBLEMS
%doc POSIX.STD doc/gawk.ps* doc/awkcard.ps*

/bin/awk
/bin/gawk
/bin/igawk
/usr/bin/awk
/usr/bin/gawk
%{_mandir}/man1/*
%{_infodir}/gawk.info*
%{_libexecdir}/awk
%{_datadir}/awk

%if %BUILD_PROFILE
%files profile
%defattr(-,root,root)
/usr/bin/pgawk
%endif

%changelog
* Mon Jul 23 2002 Michail Litvak <mci@owl.openwall.com>
- Moved profiling gawk (pgawk) into separate package.
- Compress PostScript documentation.

* Mon Jul 15 2002 Michail Litvak <mci@owl.openwall.com>
- 3.1.1
- Switched to using Paul Eggert's patch to igawk which makes it
not use temporary files at all.

* Fri Feb 01 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions.

* Sun May 27 2001 Solar Designer <solar@owl.openwall.com>
- Patched unsafe temporary file handling in igawk, based on report and
patch from Jarno Huuskonen.
- Make sure gawk.info and igawk.sh are re-generated from gawk.texi on
package builds.

* Sun Oct 01 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import spec from RH
