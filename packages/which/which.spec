# $Owl: Owl/packages/which/which.spec,v 1.11 2006/06/06 16:18:35 ldv Exp $

Summary: Displays where a particular program in your path is located.
Name: which
Version: 2.16
Release: owl1
License: GPL
Group: Applications/System
URL: http://www.xs4all.nl/~carlo17/which/
Source0: ftp://ftp.gnu.org/gnu/which/which-%version.tar.gz
Source1: which-2.sh
Source2: which-2.csh
Patch0: which-2.16-owl-info.diff
Patch1: which-2.16-rh-alt-fixes.diff
PreReq: /sbin/install-info
Prefix: %_prefix
BuildRoot: /override/%name-%version

%description
The which command shows the full pathname of a specified program, if
the specified program is in your PATH.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure
make

%install
rm -rf %buildroot

%makeinstall

mkdir -p %buildroot/etc/profile.d
install -pm755 %_sourcedir/which-2.{sh,csh} %buildroot/etc/profile.d/

# Remove unpackaged files
rm %buildroot%_infodir/dir

%post
/sbin/install-info %_infodir/which.info %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/which.info %_infodir/dir
fi

%files
%defattr(-,root,root)
%doc EXAMPLES NEWS
%_bindir/*
%config /etc/profile.d/which-2.*
%_infodir/*.info*
%_mandir/*/*

%changelog
* Tue Jun 06 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.16-owl1
- Updated to 2.16.
- Packaged documentation in Info format.

* Sat Feb 02 2002 Solar Designer <solar-at-owl.openwall.com> 2.12-owl2
- Enforce our new spec file conventions.

* Sun Nov 19 2000 Michail Litvak <mci-at-owl.openwall.com>
- Imported from RH.
- update to 2.12
