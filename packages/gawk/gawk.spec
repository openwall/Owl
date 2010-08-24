# $Owl: Owl/packages/gawk/gawk.spec,v 1.22 2010/08/24 16:16:07 solar Exp $

%define BUILD_PROFILE 0

Summary: The GNU version of the awk text processing utility.
Name: gawk
Version: 3.1.8
Release: owl2
License: GPL
Group: Applications/Text
Source0: ftp://ftp.gnu.org/gnu/gawk/gawk-%version.tar.bz2
# ftp://ftp.gnu.org/gnu/gawk/gawk-%version-ps.tar.gz
#Source1: gawk-%version-ps.tar.bz2
Patch1: gawk-3.1.8-owl-info.diff
Patch2: gawk-3.1.8-owl-tmp.diff
Patch3: gawk-3.1.8-owl-warnings.diff
Patch4: gawk-3.1.8-owl-man.diff
PreReq: /sbin/install-info
BuildRequires: texinfo >= 4.2
BuildRoot: /override/%name-%version

%description
The gawk package contains the GNU version of awk, a text processing
utility.  awk interprets a special-purpose programming language to do
quick and easy text pattern matching and reformatting jobs.

%if %BUILD_PROFILE
%package profile
Summary: The version of gawk with profiling support.
Group: Development/Tools
Requires: %name = %version-%release

%description profile
The gawk-profile package includes pgawk (profiling gawk).  pgawk is
identical in every way to gawk, except that when it has finished running,
it creates a profile of your program with line execution counts.
%endif

%prep
#%setup -q -b 1
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%{expand:%%define optflags %optflags -Wall}

%build
rm doc/gawk.info awklib/stamp-eg
%configure
%__make

%check
%__make check

%install
rm -rf %buildroot
%makeinstall bindir=%buildroot/bin \
	mandir=%buildroot%_mandir \
	libexecdir=%buildroot%_libexecdir/awk \
	datadir=%buildroot%_datadir/awk

#gzip -9n doc/*.ps

pushd %buildroot
rm -f .%_infodir/dir
mkdir -p .%_prefix/bin
ln -sf gawk.1.gz .%_mandir/man1/awk.1.gz
cd bin
ln -sf ../../bin/gawk ../usr/bin/awk
ln -sf ../../bin/gawk ../usr/bin/gawk
mv %buildroot/bin/pgawk %buildroot/usr/bin/

# XXX: (GM): Remove unpackaged files (check later)
rm %buildroot/bin/gawk-%version
rm %buildroot/bin/pgawk-%version
rm %buildroot%_bindir/pgawk
rm %buildroot%_infodir/gawkinet.info*
popd

%find_lang %name

%post
/sbin/install-info %_infodir/gawk.info %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/gawk.info %_infodir/dir
fi

%files -f %name.lang
%defattr(-,root,root)
%doc README COPYING FUTURES LIMITATIONS NEWS PROBLEMS
%doc POSIX.STD
#%doc doc/*.ps.gz

/bin/awk
/bin/gawk
/bin/igawk
/usr/bin/awk
/usr/bin/gawk
%_mandir/man1/*
%_infodir/gawk.info*
%_libexecdir/awk
%_datadir/awk

%if %BUILD_PROFILE
%files profile
%defattr(-,root,root)
/usr/bin/pgawk
%endif

%changelog
* Tue Aug 24 2010 Solar Designer <solar-at-owl.openwall.com> 3.1.8-owl2
- Disabled packaging of PostScript documentation (it is not supplied pre-built
with recent versions of gawk anymore).

* Sat Aug 21 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 3.1.8-owl1
- Updated to 3.1.8.
- Dropped patch -eggert-tmp (fixed in upstream).
- Updated patch -owl-info.
- Patched unsafe temporary file handling in sample PostAgent.sh.
- Fixed compiler warnings.

* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.1.1-owl4
- Corrected info files installation.

* Mon Aug 19 2002 Michail Litvak <mci-at-owl.openwall.com> 3.1.1-owl3
- Deal with info dir entries such that the menu looks pretty.

* Mon Jul 23 2002 Michail Litvak <mci-at-owl.openwall.com>
- Moved profiling gawk (pgawk) into separate subpackage, not built by default.
- Compress PostScript documentation.

* Mon Jul 15 2002 Michail Litvak <mci-at-owl.openwall.com>
- 3.1.1
- Switched to using Paul Eggert's patch to igawk which makes it
not use temporary files at all.

* Fri Feb 01 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Sun May 27 2001 Solar Designer <solar-at-owl.openwall.com>
- Patched unsafe temporary file handling in igawk, based on report and
patch from Jarno Huuskonen.
- Make sure gawk.info and igawk.sh are re-generated from gawk.texi on
package builds.

* Sun Oct 01 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import spec from RH
