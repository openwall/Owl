# $Id: Owl/packages/time/time.spec,v 1.8 2005/10/24 03:06:30 solar Exp $

Summary: A GNU utility for monitoring a program's use of system resources.
Name: time
Version: 1.7
Release: owl14
License: GPL
Group: Applications/System
Source0: ftp://ftp.gnu.org/gnu/time/time-%version.tar.gz
Source1: time.1
Patch0: time-1.7-deb-make_quiet.diff
Patch1: time-1.7-mdk-info.diff
Patch2: time-1.7-deb-info_quiet.diff
Prefix: %_prefix
BuildRequires: texinfo
BuildRoot: /override/%name-%version

%description
The GNU time utility runs another program, collects information about
the resources used by that program while it is running and displays the
results.  time can help developers optimize their programs.

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p1

%build
%configure
make LDFLAGS=-s

%install
rm -rf %buildroot
%makeinstall

mkdir -p %buildroot%_mandir/man1
install -m 644 %_sourcedir/time.1 %buildroot%_mandir/man1/

%post
/sbin/install-info %_infodir/time.info.gz %_infodir/dir \
	--entry="* time: (time).                                 GNU time Utility"

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/time.info.gz %_infodir/dir \
		--entry="* time: (time).                                 GNU time Utility"
fi

%files
%defattr(-,root,root)
%doc NEWS README
%_bindir/time
%_infodir/time.info*
%_mandir/*/*

%changelog
* Mon Aug 19 2002 Michail Litvak <mci-at-owl.openwall.com> 1.7-owl14
- Deal with info dir entries such that the menu looks pretty.

* Mon Feb 04 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Sat Nov 18 2000 Michail Litvak <mci-at-owl.openwall.com>
- imported from RH, some patches from MDK, and Debian
- added --quiet options (deb)
