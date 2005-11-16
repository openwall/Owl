# $Owl: Owl/packages/grep/grep.spec,v 1.17 2005/11/16 13:09:47 solar Exp $

Summary: The GNU versions of grep pattern matching utilities.
Name: grep
Version: 2.5.1a
Release: owl1
Epoch: 1
License: GPL
Group: Applications/Text
Source: ftp://ftp.gnu.org/gnu/grep/grep-%version.tar.bz2
Patch10: grep-2.5.1a-rh-fgrep.diff
Patch11: grep-2.5.1a-rh-owl-i18n.diff
Patch12: grep-2.5.1a-rh-oi.diff
Patch20: grep-2.5.1a-deb-case-fold-charclass.diff
Patch21: grep-2.5.1a-deb-case-fold.diff
Patch22: grep-2.5.1a-deb-case-fold-range.diff
Patch23: grep-2.5.1a-deb-owl-charclass-bracket.diff
Patch24: grep-2.5.1a-deb-owl-man.diff
Patch30: grep-2.5.1a-owl-info.diff
Patch31: grep-2.5.1a-owl-fixes.diff
PreReq: /sbin/install-info
Prefix: %_prefix
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
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch30 -p1
%patch31 -p1

%{expand:%%define optflags %optflags -Wall}

%build
%configure --without-included-regex
%__make
%__make check

%install
rm -rf %buildroot
%makeinstall \
	LDFLAGS=-s \
	prefix=%buildroot%_prefix exec_prefix=%buildroot
mkdir -p %buildroot/bin
mv %buildroot%_prefix/bin/* %buildroot/bin/
rm -rf %buildroot%_prefix/bin

# Use symlinks for egrep and fgrep
ln -sf grep %buildroot/bin/egrep
ln -sf grep %buildroot/bin/fgrep

# Remove unpackaged files
rm %buildroot%_infodir/dir

%post
/sbin/install-info %_infodir/grep.info.gz %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/grep.info.gz %_infodir/dir
fi

%files
%defattr(-,root,root)
%doc ABOUT-NLS AUTHORS THANKS TODO NEWS README ChangeLog
/bin/*
%_infodir/*.info*
%_mandir/*/*
%_prefix/share/locale/*/*/grep.*

%changelog
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
