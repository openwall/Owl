# $Owl: Owl/packages/coreutils/coreutils.spec,v 1.33 2014/07/12 13:49:31 galaxy Exp $

%define def_with() %{expand:%%{!?_with_%1: %%{!?_without_%1: %%global _with_%1 --with-%1%{?2:=%2}}}}
%define def_without() %{expand:%%{!?_with_%1: %%{!?_without_%1: %%global _without_%1 --without-%1}}}
%define def_enable() %{expand:%%{!?_with_%1: %%{!?_without_%1: %%global _with_%1 --enable-%1%{?2:=%2}}}}
%define def_disable() %{expand:%%{!?_with_%1: %%{!?_without_%1: %%global _without_%1 --disable-%1}}}

%def_disable	acl
%def_disable	xattr
%def_disable	libcap
%def_disable	libsmack
%def_enable	nls
%def_with	openssl
%def_without	selinux
%def_with	gmp

Summary: The GNU versions of common management utilities.
Name: coreutils
Version: 8.22
Release: owl1
License: GPL
Group: System Environment/Base
URL: http://www.gnu.org/software/%name/
Source0: ftp://ftp.gnu.org/gnu/%name/%name-%version.tar.xz

# Additional sources
# true and false source and man-pages
Source1: exit.c
Source2: true.1
Source3: false.1

# shell profile settings and configuration file for colorized ls output
Source10: colorls.sh
Source11: colorls.csh

# sources from sh-utils
Source20: usleep.c
Source21: usleep.1
Source22: getuseruid.c
Source23: runas.c
Source24: runas.1
Source25: runbg.c

Patch0: %name-8.22-owl-gnulib-test-getcwd.diff
Patch1: %name-8.22-owl-gnulib-test-getlogin.diff
Patch2: %name-8.22-owl-tests-xattr.diff

Patch3: %name-8.22-alt-chroot-tmp-env-vars.diff
Patch4: %name-8.22-alt-dircolors.diff
Patch5: %name-8.22-alt-hostname.diff
Patch6: %name-8.22-rh-owl-alt-ls-dumbterm.diff
Patch7: %name-8.22-alt-mksock.diff
Patch8: %name-8.22-alt-texinfo.diff
Patch9: %name-8.22-alt-tinfo.diff
Patch10: %name-8.22-rh-alt-langinfo.diff
Patch11: %name-8.22-owl-tests-pwd-long.diff

Provides: stat = %version, fileutils = %version
Provides: textutils = %version, sh-utils = %version
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

Requires(pre): /sbin/install-info
BuildRequires: gettext, autoconf >= 2.69, automake >= 1.14, libtool
BuildRequires: sed >= 4.1.1, bison >= 2.0, m4 >= 1.4.3
BuildRequires: perl >= 5.6.1
BuildRequires: libtermcap-devel
BuildRequires: ncurses-devel
BuildRequires: texinfo
%if 0%{?_with_acl:1}
BuildRequires: libacl-devel
%endif
%if 0%{?_with_xattr:1}
BuildRequires: libattr-devel
%endif
%if 0%{?_with_libcap:1}
BuildRequires: libcap-devel >= 2.24
%endif
%if 0%{?_with_libsmack:1}
BuildRequires: libsmack-devel
%endif
%if 0%{?_with_openssl:1}
BuildRequires: openssl-devel
%endif
%if 0%{?_with_selinux:1}
BuildRequires: libselinux-devel
%endif
%if 0%{?_with_gmp:1}
BuildRequires: gmp-devel
%endif

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

%patch0 -p1 -b .gnulib-test-getcwd
%patch1 -p1 -b .gnulib-test-getlogin
%patch2 -p1 -b .owl-tests-xattr

%patch3 -p1 -b .chroot-tmp-env-vars
%patch4 -p1 -b .dircolors
%patch5 -p1 -b .hostname
%patch6 -p1 -b .ls-term
%patch7 -p1 -b .mksock

# We need to regenerate the list of programs for mksock
build-aux/gen-lists-of-programs.sh --autoconf >m4/cu-progs.m4
build-aux/gen-lists-of-programs.sh --automake >src/cu-progs.mk

%patch8 -p1 -b .texinfo
%patch9 -p1 -b .tinfo
%patch10 -p1 -b .date-format
%patch11 -p1 -b .tests-pwd-long.diff

# Generate LINGUAS file.
ls po/*.po 2>/dev/null |
	sed 's|.*/||; s|\.po$||' >po/LINGUAS

gettextize -f -q --symlink
rm lib/gettext.h
ln -s '%_datadir/gettext/gettext.h' lib/
aclocal --force -I m4
autoreconf -fis

# rm -f for easy CVS vs release builds
rm -f doc/*.info* man/*.1

# Compress (some) docs to save space
bzip2 -9k NEWS THANKS

%build
%configure \
	--disable-rpath \
	--exec-prefix=/ \
	--enable-install-program=arch,hostname \
	--enable-no-install-program=su,uptime \
	%{?_with_acl}%{?_without_acl} \
	%{?_with_xattr}%{?_without_xattr} \
	%{?_with_libcap}%{?_without_libcap} \
	%{?_with_libsmack}%{?_without_libsmack} \
	%{?_with_nls}%{?_without_nls} \
	%{?_with_openssl}%{?_without_openssl} \
	%{?_with_selinux}%{?_without_selinux} \
	%{?_with_gmp}%{?_without_gmp} \
#

%__make -C po update-po
%__make

# Build our version of true and false
%__cc %optflags -Wall -W -static -U_FORTIFY_SOURCE -fno-stack-protector \
	-nostartfiles -static -DSTATUS=0 '%_sourcedir/exit.c' -o true
%__cc %optflags -Wall -W -static -U_FORTIFY_SOURCE -fno-stack-protector \
	-nostartfiles -static -DSTATUS=1 '%_sourcedir/exit.c' -o false

# Build additional utilities.
for n in getuseruid runas runbg usleep; do
	%__cc %optflags "%_sourcedir/$n.c" -o "$n"
done

%install
[ '%buildroot' != '/' -a -d '%buildroot' ] && rm -rf -- '%buildroot'
%makeinstall

# color-ls shell profile settings and configuration file
mkdir -p '%buildroot/etc/profile.d'
install -pm755 '%_sourcedir'/colorls.{,c}sh '%buildroot/etc/profile.d/'
install -pm644 src/dircolors.hin '%buildroot/etc/DIR_COLORS'

# %_bindir -> /bin path relocations
mkdir -p '%buildroot/bin'
for n in \
	basename cat chgrp chmod chown cp cut date dd df echo \
	env false hostname kill link ln ls mkdir mknod mv nice \
	pwd readlink rm rmdir sleep sort stat stty sync touch \
	true uname unlink arch mktemp \
; do
	mv "%buildroot%_bindir/$n" '%buildroot/bin/'
done

# dir and vdir symlinks to ls
ln -sf ../../bin/ls '%buildroot%_bindir/dir'
ln -sf ../../bin/ls '%buildroot%_bindir/vdir'

# /bin/*domainname symlinks to hostname - same man-page for all
for n in dnsdomainname domainname nisdomainname ypdomainname; do
	ln -s hostname "%buildroot/bin/$n"
	echo '.so man1/hostname.1' >"%buildroot%_mandir/man1/$n.1"
done

# test
ln -sf test '%buildroot%_bindir/['

# chroot goes in %_sbindir
mkdir -p '%buildroot%_sbindir'
mv '%buildroot%_bindir/chroot' '%buildroot%_sbindir/'

# Install assembler versions of true and false and their man-pages
install -pm755 true false '%buildroot/bin/'
install -pm644 '%_sourcedir'/{true,false}.1 '%buildroot%_mandir/man1/'

# Install additional utilities and their manpages
install -pm755 getuseruid runas runbg usleep '%buildroot/bin/'
install -pm644 '%_sourcedir'/{runas,usleep}.1 '%buildroot%_mandir/man1/'

# Backwards compatible symlinks
for n in env cut; do
	ln -s "../../bin/$n" "%buildroot%_bindir/$n"
done

%find_lang %name || :
touch '%name.lang'

# Remove unpackaged files
rm %buildroot%_infodir/dir

### Remove utilities and manpages which are still packaged within
### other packages.
# /bin/hostname and symlinks to it are still in net-tools
rm %buildroot{/bin,%_mandir/man1}/hostname*
rm %buildroot{/bin,%_mandir/man1}/*domainname*

# /bin/kill is also still in util-linux
rm %buildroot{/bin,%_mandir/man1}/kill*
# /bin/arch is also still in util-linux
rm %buildroot{/bin,%_mandir/man1}/arch*

# /bin/mktemp is also still in mktemp
rm %buildroot{/bin,%_mandir/man1}/mktemp*

# /bin/usleep is also still in owl-startup
rm %buildroot{/bin,%_mandir/man1}/usleep*
###

%check
%__make check

./true
! ./false

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

%files -f %name.lang
%doc AUTHORS NEWS.bz2 README THANKS.bz2 TODO
%defattr(0644,root,root,0755)
%config(noreplace) %_sysconfdir/DIR_COLORS
%config(noreplace) %attr(0755,root,root) %_sysconfdir/profile.d/colorls.*sh
%attr(0755,root,root) /bin/*
%attr(0755,root,root) %_bindir/*
%attr(0755,root,root) %_sbindir/*
%_libexecdir/%name/
%_mandir/man1/*.1*
%_infodir/*.info*

%changelog
* Sun Jun 22 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 8.22-owl1
- Updated to 8.22.

* Sun Jul 22 2012 Vasiliy Kulikov <segoon-at-owl.openwall.com> 5.97-owl6
- Fixed build failure with headers of Linux 2.6.32.

* Wed Sep 22 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 5.97-owl5
- Added .lzma, .txz and .xz suffixes to DIR_COLORS.

* Mon Mar 22 2010 Solar Designer <solar-at-owl.openwall.com> 5.97-owl4
- In exit.c, invoke the syscall via the _syscall1() macro rather than via the
glibc wrapper when we're compiling for 32-bit x86, because our current glibc
(after the switch to NPTL) produces large static binaries for exit.c on this
architecture.

* Sun Nov 22 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 5.97-owl3
- Fixed tests/touch/not-owner on read-only root file system.

* Mon Oct 08 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 5.97-owl2
- Updated to stable b5_9x snapshot 20060628.
- Fixed cut(1) double-free bug (Jim Meyering, RH#220312).
- Fixed mv(1) error reporting (Jim Meyering, DEB#376749).
- Added cifs to df(1) remote filesystems list (Tim Waugh, RH#183703).
- Fixed rm(1) potential crash bug (David Shaw, RH#235401).
- Fixed getcwd() to make pwd(1) and readlink(1) work also when run
with an unreadable parent dir on systems with openat(2) support
(Jim Meyering, RH#227168).
- Backported new hashes: base64, sha224sum, sha256sum, sha384sum,
sha512sum.
- Updated russian translation.

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
