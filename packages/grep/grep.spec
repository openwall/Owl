# $Owl: Owl/packages/grep/grep.spec,v 1.24 2010/08/26 15:01:46 segoon Exp $

Summary: The GNU versions of grep pattern matching utilities.
Name: grep
Version: 2.6.3
Release: owl1
Epoch: 1
License: GPL
Group: Applications/Text
Source: ftp://ftp.gnu.org/gnu/grep/grep-%version.tar.bz2
Patch25: grep-2.6.3-deb-alt-bigfile.diff
Patch30: grep-2.6.3-owl-info.diff
Patch31: grep-2.6.3-owl-fixes.diff
#Patch32: grep-2.6.3-owl-program_name.diff
Patch33: grep-2.6.3-alt-owl-bound.diff
Patch35: grep-2.6.3-deb-man.diff
Patch36: grep-2.6.3-deb-mmap.diff
Patch37: grep-2.6.3-deb-xmalloc.diff
PreReq: /sbin/install-info
BuildRequires: pcre-devel
BuildRequires: texinfo, gettext, sed
BuildRoot: /override/%name-%version

%description
The GNU versions of commonly used grep utilities.  grep searches
through textual input for lines which contain a match to a specified
pattern and then prints the matching lines.  GNU's grep utilities
include grep, egrep, and fgrep.

%prep
%setup -q
%patch25 -p1
%patch30 -p1
%patch31 -p1
#%patch32 -p1
%patch33 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
bzip2 -9k ChangeLog

%{expand:%%define optflags %optflags -Wall}

%build
# The regex.h must be kept in sync with --without-included-regex.
install -pm644 %_includedir/regex.h lib/
# Bundled error.c is outdated.
: >lib/error.c
%configure --bindir=/bin --without-included-regex
%__make

%check
%__make check

%install
rm -rf %buildroot
%makeinstall bindir=%buildroot/bin LDFLAGS=

# Use symlinks for egrep, fgrep and pcregrep
#ln -sf grep %buildroot/bin/egrep
#ln -sf grep %buildroot/bin/fgrep
#ln -sf grep %buildroot/bin/pcregrep
ln -s grep.1.gz %buildroot%_mandir/man1/pcregrep.1.gz

# Remove unpackaged files
rm %buildroot%_infodir/dir

%post
/sbin/install-info %_infodir/grep.info %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/grep.info %_infodir/dir
fi

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog.bz2 NEWS README THANKS TODO
/bin/*
%_infodir/*.info*
%_mandir/*/*
%_prefix/share/locale/*/*/grep.*

%changelog
* Thu Aug 26 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 1:2.6.3-owl1
- Updated patches and dropped those are fixed by upstream.
- Added patches from Debian.

* Mon Apr 23 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 1:2.5.1a-owl4
- Applied "fgrep -w" fix by Pavel Kankovsky.
- Adopted Debian fix for big file handling.

* Sun Sep 24 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1:2.5.1a-owl3
- Applied upstream fix for "-D skip".
- Fixed several potential NULL dereferences and reads beyond end of buffer
due to incorrect bound checks.

* Mon Dec 05 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1:2.5.1a-owl2
- Packaged pcregrep.

* Thu Nov 10 2005 Michail Litvak <mci-at-owl.openwall.com> 1:2.5.1a-owl1
- 2.5.1a
- Added patches from Debian and Red Hat.
- Built with -Wall, fixed some warnings.
- Added make check.

* Mon Aug 19 2002 Michail Litvak <mci-at-owl.openwall.com> 1:2.4.2-owl2
- Deal with info dir entries such that the menu looks pretty.

* Sun Feb 03 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions

* Sun Jul 30 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- imported from RH
- locales fix
