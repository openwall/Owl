# $Id: Owl/packages/man/man.spec,v 1.6 2002/03/29 22:52:42 solar Exp $

Summary: A set of documentation tools: man, apropos and whatis.
Name: man
Version: 1.5i2
Release: owl2
License: GPL
Group: System Environment/Base
Source: ftp://ftp.win.tue.nl/pub/linux-local/utils/man/man-%{version}.tar.gz
Patch0: man-1.5i-owl-makewhatis.diff
Requires: groff, mktemp, findutils >= 1:4.1.5-owl4
BuildRoot: /override/%{name}-%{version}

%description
The man package includes three tools for finding information and/or
documentation about your Linux system: man, apropos and whatis.  The
man system formats and displays on-line manual pages about commands or
functions on your system.  apropos searches the whatis database
(containing short descriptions of system commands) for a string.
whatis searches its own database for a complete word.

%prep
%setup -q
%patch0 -p1

%build
./configure -default +fsstnd
mv conf_script conf_script.orig
sed 's,/usr/lib,/etc,' < conf_script.orig > conf_script
chmod u+x conf_script
make CC="gcc $RPM_OPT_FLAGS -D_GNU_SOURCE"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/{bin,man,sbin}
make install PREFIX=$RPM_BUILD_ROOT

cd $RPM_BUILD_ROOT

mkdir -p var/catman/{X11R6,local}
for i in 1 2 3 4 5 6 7 8 9 n; do
	mkdir var/catman/{cat$i,X11R6/cat$i,local/cat$i}
done

# symlinks for manpath
ln -s man usr/bin/manpath
ln -s man.1 usr/man/man1/manpath.1

%clean
rm -rf $RPM_BUILD_ROOT

# Clean up accumulated cat litter.
%preun
find /var/catman/{,X11R6/,local/}cat[123456789n] -type f -delete

%post
find /var/catman/{,X11R6/,local/}cat[123456789n] -type f -delete

%files
%defattr(-,root,root)
%attr(0755,root,man) /usr/bin/man
/usr/bin/manpath
/usr/bin/apropos
/usr/bin/whatis
%attr(0700,root,root) /usr/sbin/makewhatis
%config /etc/man.conf
/usr/man/man5/man.conf.5*
/usr/man/man1/whatis.1*
/usr/man/man1/man.1*
/usr/man/man1/manpath.1*
/usr/man/man1/apropos.1*
/usr/man/man1/man2html.1*
/usr/bin/man2html

%attr(0755,root,man) %dir /var/catman
%attr(0775,root,man) %dir /var/catman/cat[123456789n]
%attr(0755,root,man) %dir /var/catman/X11R6
%attr(0775,root,man) %dir /var/catman/X11R6/cat[123456789n]
%attr(0755,root,man) %dir /var/catman/local
%attr(0775,root,man) %dir /var/catman/local/cat[123456789n]

%changelog
* Sat Mar 30 2002 Solar Designer <solar@owl.openwall.com>
- No longer have the /var/catman/{,X11R6/,local/} directories themselves
(as opposed to their subdirectories) writable to group man.
- Clean up the subdirectories on package removal or upgrade safely (this
assumes that group man could have been compromised, even though we don't
really use it on Owl).

* Wed Feb 06 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions.

* Tue Jun 12 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 1.5i2.

* Fri May 18 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 1.5i.
- Corrected the Source URL.

* Thu Aug 10 2000 Solar Designer <solar@owl.openwall.com>
- Imported this spec file from RH, simplified it.
- Non-SGID installation as there's still no good solution for the man page
spoofing problem.
- Added a patch to makewhatis to use mktemp.
- Removed the cron scripts for now (should allocate a pseudo-user and fix
permissions first).
