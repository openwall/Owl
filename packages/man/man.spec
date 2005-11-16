# $Owl: Owl/packages/man/man.spec,v 1.21 2005/11/16 13:16:56 solar Exp $

Summary: A set of documentation tools: man, apropos and whatis.
Name: man
Version: 1.5l
Release: owl6
License: GPL
Group: System Environment/Base
Source: ftp://ftp.win.tue.nl/pub/linux-local/utils/man/man-%version.tar.gz
Patch0: man-1.5l-owl-makewhatis.diff
Patch1: man-1.5l-owl-latin1.diff
Patch2: man-1.5l-owl-bound.diff
Requires: groff, less, gzip, bzip2, coreutils
# makewhatis
Requires: gawk, sed, mktemp >= 1:1.3.1
# makewhatis and %%preun
Requires: findutils >= 1:4.1.5-owl4
BuildRequires: sed
# These need to be detected when this package is built
BuildRequires: groff, less, gzip, bzip2
# The proper full path to awk is patched into makewhatis
BuildRequires: gawk
BuildRoot: /override/%name-%version

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
%patch1 -p1
%patch2 -p1

%build
./configure -default +fhs -fsstnd -confdir /etc
make CC="gcc %optflags -D_GNU_SOURCE"

%install
rm -rf %buildroot
mkdir -p %buildroot/usr/{bin,sbin}
make install PREFIX=%buildroot

cd %buildroot

mkdir -p var/cache/man/{X11R6,local}
for i in 1 2 3 4 5 6 7 8 9 n; do
	mkdir var/cache/man/{cat$i,X11R6/cat$i,local/cat$i}
done

# symlinks for manpath
ln -s man .%_bindir/manpath
ln -s man.1 .%_mandir/man1/manpath.1

# Clean up accumulated cat litter.
%preun
find /var/cache/man/{,X11R6/,local/}cat[123456789n] -type f -delete

%files
%defattr(-,root,root)
%attr(0755,root,man) %_bindir/man
%_bindir/manpath
%_bindir/apropos
%_bindir/whatis
%_bindir/man2html
%_bindir/man2dvi
%attr(0700,root,root) %_sbindir/makewhatis
%config /etc/man.conf
%_mandir/man1/whatis.1*
%_mandir/man1/man.1*
%_mandir/man1/manpath.1*
%_mandir/man1/apropos.1*
%_mandir/man1/man2html.1*
%_mandir/man5/man.conf.5*
%_mandir/man8/makewhatis.8*

%attr(0755,root,man) %dir /var/cache/man
%attr(0775,root,man) %dir /var/cache/man/cat[123456789n]
%attr(0755,root,man) %dir /var/cache/man/X11R6
%attr(0775,root,man) %dir /var/cache/man/X11R6/cat[123456789n]
%attr(0755,root,man) %dir /var/cache/man/local
%attr(0775,root,man) %dir /var/cache/man/local/cat[123456789n]

%changelog
* Mon Oct 24 2005 Solar Designer <solar-at-owl.openwall.com> 1.5l-owl6
- Added build and runtime dependencies.
- Updated the makewhatis patch per our new conventions (mktemp first, set
the trap later to not trigger in-shell races).

* Thu Nov 11 2004 Michail Litvak <mci-at-owl.openwall.com> 1.5l-owl5
- Spec file cleanups.
- Include man2dvi.

* Mon Nov 08 2004 Michail Litvak <mci-at-owl.openwall.com> 1.5l-owl4
- FHS 2.2 compatibility.

* Wed Jul 21 2004 Michail Litvak <mci-at-owl.openwall.com> 1.5l-owl3
- Use sed -i.

* Fri Sep 05 2003 Solar Designer <solar-at-owl.openwall.com> 1.5l-owl2
- Fixed the buffer overflow with MANPL discovered by KF from SNOSoft.

* Sun Mar 16 2003 Solar Designer <solar-at-owl.openwall.com> 1.5l-owl1
- Updated to 1.5l.

* Fri Sep 20 2002 Solar Designer <solar-at-owl.openwall.com>
- Use groff -Tlatin1 such that 8-bit characters may be seen (for example,
when viewing rpm(8) with LANG=ru_RU.KOI8_R).
- Use the new mktemp -t in makewhatis.

* Sat Mar 30 2002 Solar Designer <solar-at-owl.openwall.com>
- No longer have the /var/catman/{,X11R6/,local/} directories themselves
(as opposed to their subdirectories) writable to group man.
- Clean up the subdirectories on package removal or upgrade safely (this
assumes that group man could have been compromised, even though we don't
really use it on Owl).

* Wed Feb 06 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Tue Jun 12 2001 Solar Designer <solar-at-owl.openwall.com>
- Updated to 1.5i2.

* Fri May 18 2001 Solar Designer <solar-at-owl.openwall.com>
- Updated to 1.5i.
- Corrected the Source URL.

* Thu Aug 10 2000 Solar Designer <solar-at-owl.openwall.com>
- Imported this spec file from RH, simplified it.
- Non-SGID installation as there's still no good solution for the man page
spoofing problem.
- Added a patch to makewhatis to use mktemp.
- Removed the cron scripts for now (should allocate a pseudo-user and fix
permissions first).
