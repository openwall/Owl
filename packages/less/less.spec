# $Owl: Owl/packages/less/less.spec,v 1.17 2006/04/04 01:02:00 ldv Exp $

Summary: A text file browser similar to more, but better.
Name: less
Version: 358
Release: owl7
License: GPL
Group: Applications/Text
URL: http://www.flash.net/~marknu/less/
Source0: ftp://ftp.gnu.org/gnu/less/%name-%version.tar.gz
Source1: lesspipe.sh
Source2: less.sh
Source3: less.csh
Patch0: less-358-owl-popen.diff
Patch1: less-358-owl-optimize.diff
BuildRequires: ncurses-devel
BuildRoot: /override/%name-%version

%description
The less utility is a text file browser that resembles more, but has
more capabilities.  less allows you to move backwards in the file as
well as forwards.  Since less doesn't have to read the entire input file
before it starts, less starts up more quickly than text editors (for
example, vi).

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure
make datadir=/usr/doc

%install
rm -rf %buildroot
%makeinstall
mkdir -p %buildroot/etc/profile.d
install -m 755 %_sourcedir/lesspipe.sh %buildroot/usr/bin/
install -m 755 %_sourcedir/less.{sh,csh} %buildroot/etc/profile.d/

%files
%defattr(-,root,root)
/etc/profile.d/*
/usr/bin/*
%_mandir/man1/*

%changelog
* Sun Jul 07 2002 Solar Designer <solar-at-owl.openwall.com> 358-owl7
- Use grep -q in lesspipe.sh.

* Mon Feb 04 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions

* Sat May 05 2001 Solar Designer <solar-at-owl.openwall.com>
- Use -Tlatin1 with groff such that 8-bit man pages may be viewed.

* Mon Apr 09 2001 Solar Designer <solar-at-owl.openwall.com>
- Optimized line number calculation and forward searches, now 20 to 50%%
faster (but still a lot slower than wc and grep).

* Thu Oct 19 2000 Solar Designer <solar-at-owl.openwall.com>
- lesspipe.sh: "cd /" before running groff such that it can't be attacked
when less is run with an untrusted current directory.

* Sun Sep 03 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- use popen

* Wed Aug 23 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- lesspipe fixes

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import spec from RH
- fix URL
