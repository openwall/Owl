# $Id: Owl/packages/coreutils/coreutils.spec,v 1.6 2005/05/28 19:50:21 galaxy Exp $

Summary: The GNU versions of common management utilities.
Name: coreutils
Version: 5.3.1
Release: owl0.5
License: GPL
Group: System Environment/Base
URL: http://www.gnu.org/software/%name/
# ftp://ftp.gnu.org/gnu/%name/
# cvs -d anoncvs@savannah.gnu.org:/cvsroot/coreutils export -Dnow coreutils
# Fix base source when we're off CVS snapshot
%define snapshot 200504240446
%define srcname %name-%snapshot
Source0: %srcname.tar.bz2

# Additional sources
# true and false asm source and man-pages
Source1: exit.S
Source2: true.1
Source3: false.1

# shell profile settings for colorized ls output
Source10: colorls.sh
Source11: colorls.csh

# usleep source and manpage
Source20: usleep.c
Source21: usleep.1

# ALT patches, candidates for upstream version and CVS backports
Patch0: coreutils-5.3.1-alt-hostname.diff

# ALT specific
Patch10: coreutils-5.3.1-alt-dircolors.diff
Patch11: coreutils-5.3.0-alt-without-su-uptime.diff
Patch12: coreutils-5.3.1-alt-ls-dir-vdir.diff
Patch13: coreutils-5.3.0-alt-posix2_version.diff

# other
Patch20: coreutils-5.3.0-rh-owl-ls-default-time-style.diff
Patch21: coreutils-5.2.0-rh-install-strip.diff
Patch22: coreutils-5.3.1-rh-owl-alt-ls-dumbterm.diff
Patch23: coreutils-4.5.3-rh-langinfo.diff

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
# due to sed -i
BuildRequires: sed >= 4.1.1, bison >= 2.0, automake >= 1.9.5

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
%setup -q -n %srcname

# ALT patches, candidates for upstream version and CVS backports
%patch0 -p1

# ALT specific
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1

# other
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1

find -type f -name '*.orig' -delete -print

# 2nd part of the posix2_version patch
find src -type f -print0 |
	xargs -r0 grep -FZl 'posix2_version () < 200112' -- |
	xargs -r0 sed -i 's/posix2_version () < 200112/posix2_version_lt_200112 ()/' --
find src -type f -print0 |
	xargs -r0 grep -FZl '200112 <= posix2_version ()' -- |
	xargs -r0 sed -i 's/200112 <= posix2_version ()/posix2_version_ge_200112 ()/' --

# Get rid of su and uptime
rm {src,man}/{su,uptime}.*

# "dist_" is redundant, as sources are distributed by default
sed -i 's/dist_man_MANS/man_MANS/g' man/Makefile.am

# rm -f for easy CVS vs release builds
rm -f doc/*.info* man/*.1

# Docs should say /var/run/[uw]tmp, not /etc/[uw]tmp
sed -i 's,/etc/utmp,/var/run/utmp,g;s,/etc/wtmp,/var/run/wtmp,g' \
	doc/*.texi man/*

%build
# disable uptime build
export gnulib_cv_have_boot_time=no

%configure --exec-prefix=/
%__make

%{?!_without_check:%{?!_disable_check:%__make -k check}}

# Build assembler version of true and false
gcc -nostartfiles -nodefaultlibs -nostdlib -DSTATUS=0 \
	%_sourcedir/exit.S -o true
gcc -nostartfiles -nodefaultlibs -nostdlib -DSTATUS=1 \
	%_sourcedir/exit.S -o false

# build usleep
gcc %optflags %_sourcedir/usleep.c -o usleep

# Compress (some) docs to save space
bzip2 -9fk ChangeLog NEWS THANKS

%install
rm -rf %buildroot
%makeinstall

# color-ls profile settings
mkdir -p %buildroot/etc/profile.d
install -pm644 src/dircolors.hin %buildroot/etc/DIR_COLORS
install -pm755 %_sourcedir/colorls.{,c}sh %buildroot/etc/profile.d/

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

# Remove unpackaged files if any
rm -f %buildroot%_infodir/dir

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
* Sat May 28 2005 (GalaxyMaster) <galaxy@owl.openwall.com> 5.3.1-owl0.5
- Added bison >= 2.0 and automake >= 1.9.5 dependencies to BuildRequires.

* Sun May 08 2005 Solar Designer <solar@owl.openwall.com> 5.3.1-owl0.4
- Miscellaneous corrections to usleep.c, usleep.1, true.1, and false.1.

* Sat May 07 2005 Dmitry V. Levin <ldv@owl.openwall.com> 5.3.1-owl0.3
- Enabled "make check" during build by default.
- Corrected %%post/%%preun scripts.
- Linked /bin/ls with /lib/libtermcap.so.2 instead of
/usr/lib/libtinfo.so.5.
- Fixed errors handling in colorls.sh script.
- Cleaned up spec file a bit according with conventions.

* Thu May 5 2005 Andreas Ericsson <exon@owl.openwall.com> 5.3.1-owl0.2
- Removed sources for unpackaged files (runas, runbg et al).
- Removed explicit Provides-tags for files.
- Removed Conflicts-tags for man-pages et al.
- Removed the install-C patch.
- Fairly major cleanups.
- Removed unmanagable pushd/popd sections.
- Made install-info conditional to $1 in %%post and %%preun.
- Removed %%clean.
- Updated to snapshot 200504240446, which is used in 5.3.1-alt0.4).

* Tue Apr 19 2005 Andreas Ericsson <exon@owl.openwall.com> 5.3.1-owl0.1
- Imported to Owl from coreutils-5.3.1-alt0.3, with Owl's conventions.
