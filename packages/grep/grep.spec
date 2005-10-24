# $Id: Owl/packages/grep/grep.spec,v 1.12 2005/10/24 03:06:24 solar Exp $

Summary: The GNU versions of grep pattern matching utilities.
Name: grep
Version: 2.4.2
Release: owl2
Epoch: 1
License: GPL
Group: Applications/Text
Source: ftp://ftp.gnu.org/gnu/grep/grep-%version.tar.gz
Patch: grep-2.4.2-owl-info.diff
PreReq: /sbin/install-info
Prefix: %_prefix
BuildRequires: texinfo, gettext
BuildRoot: /override/%name-%version

%description
The GNU versions of commonly used grep utilities.  grep searches
through textual input for lines which contain a match to a specified
pattern and then prints the matching lines.  GNU's grep utilities
include grep, egrep and fgrep.

%prep
%setup -q
%patch -p1

%build
rm doc/grep.info
unset LINGUAS || :
%configure
make

%install
rm -rf %buildroot
%makeinstall \
	LDFLAGS=-s \
	prefix=%buildroot%_prefix exec_prefix=%buildroot
mkdir -p %buildroot/bin
mv %buildroot%_prefix/bin/* %buildroot/bin/
rm -rf %buildroot%_prefix/bin

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
* Mon Aug 19 2002 Michail Litvak <mci-at-owl.openwall.com> 1:2.4.2-owl2
- Deal with info dir entries such that the menu looks pretty.

* Sun Feb 03 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions

* Sun Jul 30 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- imported from RH
- locales fix
