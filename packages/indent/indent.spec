# $Id: Owl/packages/indent/indent.spec,v 1.1 2005/11/11 15:29:49 solar Exp $

Summary: A GNU program for formatting C code.
Name: indent
Version: 2.2.9
Release: owl1
Group: Development/Tools
License: GPL
URL: http://www.gnu.org/software/indent/
Source: ftp://ftp.gnu.org/gnu/%name/%name-%version.tar.gz
Patch0: indent-2.2.9-rh-check-label-size.diff
BuildRoot: /override/%name-%version

%description
Indent is a GNU program for formatting C code so that it is easier to
read.  Indent can also convert from one C writing style to a different one.
This can be helpful when porting code to various 'odd' platforms.  Indent
has a limited understanding of C syntax, but tries its best to handle things
properly.

%prep
%setup -q
%patch0 -p1

%build
%configure
%__make

%install
rm -rf %buildroot
%makeinstall

# Remove unpackaged files.
rm %buildroot%_infodir/dir
rm %buildroot%_prefix/doc/%name/indent.html
rm %buildroot%_bindir/texinfo2man

%post
/sbin/install-info %_infodir/%name.info %_infodir/dir

%preun
/sbin/install-info --delete %_infodir/%name.info %_infodir/dir

%files
%defattr(-,root,root)
%_bindir/*
%_datadir/locale/*/LC_MESSAGES/indent.mo
%_mandir/man1/%name.1.gz
%_infodir/%name.info.gz

%changelog
* Fri Nov 11 2005 Andreas Ericsson <exon-at-owl.openwall.com> 2.2.9-owl1
- Added patch from FC3 to mitigate potential SIGSEGVs with long labels.
- Moved to official distribution.
- Grammar and interpunctuation fixes.

* Thu Apr 21 2005 Andreas Ericsson <exon-at-owl.openwall.com> 2.2.9-owl_add1
- Added internationalization files.
- Enforced Owl's specfile conventions.
- Added %%post and %%pre for install-info purposes.
- New Release-tag for Owl addons.

* Sat Jun 19 2004 Andreas Ericsson <exon-at-owl.openwall.com> 2.2.9-owl0.1
- Initial packaging.
