# $Owl: Owl/packages/coreutils/coreutils.spec,v 1.25 2006/06/25 16:58:47 ldv Exp $

Summary: The GNU versions of common management utilities.
Name: coreutils
Version: 5.97
Release: owl1
License: GPL
Group: System Environment/Base
URL: http://www.gnu.org/software/%name/
Source0: ftp://ftp.gnu.org/gnu/%name/%name-%version.tar.bz2

# Additional sources
# true and false source and man-pages
Source1: exit.c
Source2: true.1
Source3: false.1

# shell profile settings and configuration file for colorized ls output
Source10: colorls.sh
Source11: colorls.csh

# usleep source and manpage
Source20: usleep.c
Source21: usleep.1

# CVS backports and other candidates for upstream version
Patch0: coreutils-5.91-up-ls-usage.diff
Patch1: coreutils-5.91-eggert-ls-time-style.diff
Patch2: coreutils-5.91-alt-hostname.diff

# Owl/ALT specific
Patch10: coreutils-5.92-owl-info-true-false.diff
Patch11: coreutils-5.91-alt-owl-dircolors.diff
Patch12: coreutils-5.3.0-alt-without-su-uptime.diff
Patch13: coreutils-5.3.1-alt-ls-dir-vdir.diff
Patch14: coreutils-5.91-alt-posix2_version.diff

# other
Patch20: coreutils-5.2.0-rh-install-strip.diff
Patch21: coreutils-5.3.1-rh-owl-alt-ls-dumbterm.diff
Patch22: coreutils-5.91-rh-alt-langinfo.diff

Provides: stat = %version, fileutils = %version, textutils = %version, sh-utils = %version
Obsoletes: stat, fileutils, textutils, sh-utils

# (ldv@): coreutils' version of kill and hostname are cleaner and
# should be used in favour of their counterparts in util-linux and
# net-tools, respectively
# (exon@): add version tags when we replace the utils with the ones
# in coreutils

# due to /bin/kill
#Conflicts: util-linux
# due to /bin/hostname
#Conflicts: net-tools
# due to /bin/usleep
#Conflicts: owl-startup

PreReq: /sbin/install-info
BuildRequires: sed >= 4.1.1, bison >= 2.0, automake >= 1.9.5, m4 >= 1.4.3
BuildRequires: perl >= 5.6.1
BuildRequires: libtermcap-devel

BuildRoot: /override/%name-%version

%description
These are the GNU core utilities.  This package is the union of
the GNU fileutils, sh-utils, and textutils packages.

These tools are the GNU versions of common useful and popular
file and text utilities which are used for:
+ file management
+ shell scripting
+ modifying text files

Most of these programs have significant advantages over their Unix
counterparts, such as greater speed, additional options, and fewer
arbitrary limits.

%prep
%setup -q

# ALT patches, candidates for upstream version and CVS backports
%patch0 -p0
%patch1 -p0
%patch2 -p1

# ALT specific
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1

# other
%patch20 -p1
%patch21 -p1
%patch22 -p1

find -type f -name '*.orig' -delete -print

# Get rid of su and uptime
rm {src,man}/{su,uptime}.*

# "dist_" is redundant, as sources are distributed by default
sed -i 's/dist_man_MANS/man_MANS/g' man/Makefile.am

# rm -f for easy CVS vs release builds
rm -f doc/*.info* man/*.1

# Docs should say /var/run/[uw]tmp, not /etc/[uw]tmp
sed -i 's,/etc/utmp,/var/run/utmp,g;s,/etc/wtmp,/var/run/wtmp,g' \
	doc/*.texi man/*

# Stable autoconf is sufficient to build coreutils for GNU/Linux.
grep -lZ 'AC_PREREQ(2\.59[^)]\+)' m4/*.m4 |
	xargs -r0 sed -i 's/AC_PREREQ(2\.59[^)]\+)/AC_PREREQ(2.59)/' --

%build
# disable uptime build
export gnulib_cv_have_boot_time=no

%configure --exec-prefix=/
%__make -C po update-po
%__make

%{?!_without_check:%{?!_disable_check:%__make -k check}}

# Build our version of true and false
%__cc %optflags -Wall -W -static -nostartfiles -DSTATUS=0 \
	%_sourcedir/exit.c -o true
%__cc %optflags -Wall -W -static -nostartfiles -DSTATUS=1 \
	%_sourcedir/exit.c -o false

# build usleep
%__cc %optflags %_sourcedir/usleep.c -o usleep

# Compress (some) docs to save space
bzip2 -9fk ChangeLog NEWS THANKS

%install
rm -rf %buildroot
%makeinstall

# color-ls shell profile settings and configuration file
mkdir -p %buildroot/etc/profile.d
install -pm755 %_sourcedir/colorls.{,c}sh %buildroot/etc/profile.d/
install -pm644 src/dircolors.hin %buildroot/etc/DIR_COLORS

# %_bindir -> /bin path relocations
mkdir -p %buildroot/bin
for n in \
	basename cat chgrp chmod chown cp cut date dd df echo \
	env false hostname kill link ln ls mkdir mknod mv nice \
	pwd readlink rm rmdir sleep sort stat stty sync touch \
	true uname unlink \
; do
	mv %buildroot%_bindir/$n %buildroot/bin/
done

# dir and vdir symlinks to ls
ln -sf ../../bin/ls %buildroot%_bindir/dir
ln -sf ../../bin/ls %buildroot%_bindir/vdir

# /bin/*domainname symlinks to hostname - same man-page for all
for n in dnsdomainname domainname nisdomainname ypdomainname; do
	ln -s hostname %buildroot/bin/$n
	echo '.so man1/hostname.1' >%buildroot%_mandir/man1/$n.1
done

# test
ln -sf test %buildroot%_bindir/[

# chroot goes in %_sbindir
mkdir -p %buildroot%_sbindir
mv %buildroot%_bindir/chroot %buildroot%_sbindir/

# Install assembler versions of true and false and their man-pages
install -pm755 true false %buildroot/bin/
install -pm644 %_sourcedir/{true,false}.1 %buildroot%_mandir/man1/

# Install usleep and its manpage
install -pm755 usleep %buildroot/bin/
install -pm644 %_sourcedir/usleep.1 %buildroot%_mandir/man1/

# Backwards compatible symlinks
for n in env cut; do
	ln -s ../../bin/$n %buildroot%_bindir/$n
done

# Remove unpackaged files
rm %buildroot%_infodir/dir

### Remove utilities and manpages which are still packaged within
### other packages.
# /bin/hostname and symlinks to it are still in net-tools
rm %buildroot{/bin,%_mandir/man1}/hostname*
rm %buildroot{/bin,%_mandir/man1}/*domainname*

# /bin/kill is also still in util-linux
rm %buildroot{/bin,%_mandir/man1}/kill*

# /bin/usleep is also still in owl-startup
rm %buildroot{/bin,%_mandir/man1}/usleep*
###

%pre
# Remove info dir entries for fileutils, textutils and sh-utils,
# this is necessary to register info dir entry for coreutils.
for f in %_infodir/{fileutils,textutils,sh-utils}.info*; do
	[ -f "$f" ] || continue
	/sbin/install-info --delete "$f" %_infodir/dir ||:
done

%post
/sbin/install-info %_infodir/%name.info %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/%name.info %_infodir/dir
fi

%files
%defattr(-,root,root)
%config(noreplace) /etc/DIR_COLORS
%config(noreplace) /etc/profile.d/*
/bin/*
%_bindir/*
%_sbindir/*
%_mandir/man?/*
%_infodir/*.info*
%_datadir/locale/*/LC_MESSAGES/coreutils.mo
%doc ChangeLog.bz2 NEWS.bz2 THANKS.bz2 AUTHORS README TODO

%changelog
* Sun Jun 25 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 5.97-owl1
- Updated to 5.97.

* Sat May 27 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 5.96-owl1
- Updated to 5.96.
- Rewritten assembler version of true and false in C to avoid
portability issues.

* Sun May 21 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 5.95-owl1
- Updated to 5.95.

* Mon Feb 20 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 5.94-owl1
- Updated to 5.94.

* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 5.93-owl2
- Backported fts fixes from 5_94 branch.

* Mon Nov 07 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 5.93-owl1
- Updated to 5.93.

* Thu Oct 27 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 5.92-owl4
- Applied upstream fix to md5sum and sha1sum: changed default read mode
back to text, to sync with documentation and for backwards compatibility.

* Mon Oct 24 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 5.92-owl3
- Applied upstream fix to "mkdir -p" and "install -d": when creating
final component of the file name, do not fail when it already exists.
- Applied upstream fix to dircolors.

* Sun Oct 23 2005 Solar Designer <solar-at-owl.openwall.com> 5.92-owl2
- Re-worked the texinfo documentation patch for true(1) and false(1) to make
it explicit that we're referring to non-GNU versions of these utilities.

* Sun Oct 23 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 5.92-owl1
- Updated to 5.92.
- Updated texinfo documentation for true(1) and false(1),
patch from Andreas Ericsson.

* Sun Jul 03 2005 Solar Designer <solar-at-owl.openwall.com> 5.3.1-owl0.6
- Enable color ls on ttys by default (like we did in fileutils package).

* Sat May 28 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 5.3.1-owl0.5
- Added bison >= 2.0 and automake >= 1.9.5 dependencies to BuildRequires.

* Sun May 08 2005 Solar Designer <solar-at-owl.openwall.com> 5.3.1-owl0.4
- Miscellaneous corrections to usleep.c, usleep.1, true.1, and false.1.

* Sat May 07 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 5.3.1-owl0.3
- Enabled "make check" during build by default.
- Corrected %%post/%%preun scripts.
- Linked /bin/ls with /lib/libtermcap.so.2 instead of
/usr/lib/libtinfo.so.5.
- Fixed errors handling in colorls.sh script.
- Cleaned up spec file a bit according with conventions.

* Thu May 5 2005 Andreas Ericsson <exon-at-owl.openwall.com> 5.3.1-owl0.2
- Removed sources for unpackaged files (runas, runbg et al).
- Removed explicit Provides-tags for files.
- Removed Conflicts-tags for man-pages et al.
- Removed the install-C patch.
- Fairly major cleanups.
- Removed unmanagable pushd/popd sections.
- Made install-info conditional to $1 in %%post and %%preun.
- Removed %%clean.
- Updated to snapshot 200504240446, which is used in 5.3.1-alt0.4).

* Tue Apr 19 2005 Andreas Ericsson <exon-at-owl.openwall.com> 5.3.1-owl0.1
- Imported to Owl from coreutils-5.3.1-alt0.3, with Owl's conventions.
