# $Id: Owl/packages/sed/sed.spec,v 1.12 2005/10/24 03:06:29 solar Exp $

Summary: A GNU stream text editor.
Name: sed
Version: 4.1.1
Release: owl1
License: GPL
Group: Applications/Text
URL: http://www.gnu.org/software/sed/
Source: ftp://ftp.gnu.org/gnu/sed/sed-%version.tar.gz
Patch0: sed-4.0.9-owl-info.diff
PreReq: /sbin/install-info
Prefix: %_prefix
BuildRequires: texinfo
BuildRoot: /override/%name-%version

%description
The sed (Stream EDitor) editor is a stream or batch (non-interactive)
editor.  sed takes text as input, performs an operation or set of
operations on the text and outputs the modified text.  The operations
that sed performs (substitutions, deletions, insertions, etc.) can be
specified in a script file or from the command line.

%prep
%setup -q
%patch -p1

%build
rm doc/sed.info
%configure
make

%install
rm -rf %buildroot

%makeinstall

cd %buildroot
mv .%_bindir bin

# Remove unpackaged files
rm %buildroot%_infodir/dir

%post
/sbin/install-info %_infodir/sed.info.gz %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/sed.info.gz %_infodir/dir
fi

%files
%defattr(-,root,root)
%doc AUTHORS BUGS NEWS README THANKS ChangeLog
/bin/sed
%_infodir/*.info*
%_datadir/locale/*/*/*
%_mandir/man*/*

%changelog
* Fri Jul 16 2004 Solar Designer <solar-at-owl.openwall.com> 4.1.1-owl1
- Updated to 4.1.1.

* Mon Jul 12 2004 Michail Litvak <mci-at-owl.openwall.com> 4.0.9-owl1
- 4.0.9

* Mon Aug 19 2002 Michail Litvak <mci-at-owl.openwall.com> 3.02-owl9
- Deal with info dir entries such that the menu looks pretty.

* Wed Feb 06 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import spec from RH rawhide
- fix URL
