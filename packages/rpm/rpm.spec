# $Owl: Owl/packages/rpm/rpm.spec,v 1.97 2014/07/12 13:58:45 galaxy Exp $

%define def_with() %{expand:%%{!?_with_%1: %%{!?_without_%1: %%global _with_%1 --with-%1%{?2:=%2}}}}
%define def_without() %{expand:%%{!?_with_%1: %%{!?_without_%1: %%global _without_%1 --without-%1}}}
%define def_enable() %{expand:%%{!?_with_%1: %%{!?_without_%1: %%global _with_%1 --enable-%1%{?2:=%2}}}}
%define def_disable() %{expand:%%{!?_with_%1: %%{!?_without_%1: %%global _without_%1 --disable-%1}}}

%def_with	rescue
%def_disable	static
%def_enable	nls
%def_disable	python
%def_enable	plugins
%def_without	selinux
# with extternal db or with the bundled one
%def_without	external
%def_without	acl
%def_without	cap
%def_without	lua

%define rpm_version 4.11.2
%define bdb_version 5.3.28
%define fcr_version 2.17.2

Summary: The RPM package management system.
Name: rpm
Version: %rpm_version
Release: owl1
License: GPLv2+
Group: System Environment/Base
URL: http://www.rpm.org/
Source0: http://rpm.org/releases/rpm-4.11.x/%name-%version.tar.bz2
# We are using a stripped down version of the db 5.3 distribution here.
# This allows us to keep the size of the sources under control. The
# original tarball was about 34MB (the NC version), our stripped down
# version is just 1.4MB.  The original distribution can be found at:
# http://download.oracle.com/berkeley-db/db-%bdb_version.NC.tar.gz
Source1: db-%bdb_version.tar.xz
# The fakechroot package is a repackaged version of the upstream one
# with an addition of the patches directory where we store our patches.
Source2: fakechroot-%fcr_version.tar.xz

Source11: rpminit
Source12: rpminit.1
Source13: gendiff
Source14: configure-presets
Source20: rpm.macros
Source21: rpm.macros.build
Source22: rpm.macros.build.arch
Source23: rpm.macros.build.collection
Source24: rpm.macros.build.conditionals
Source25: rpm.macros.build.configure
Source26: rpm.macros.build.debugpkg
Source27: rpm.macros.build.deps
Source28: rpm.macros.build.java
Source29: rpm.macros.build.perl
Source30: rpm.macros.build.python
Source31: rpm.macros.build.scriptlets
Source32: rpm.macros.build.signature
Source33: rpm.macros.build.specfile
Source34: rpm.macros.build.tools
Source35: rpm.macros.sys.filesystem
Source36: rpm.macros.sys.platform
Source37: rpm.macros.sys.scriptlets
Source38: rpm.macros.sys.signature
Source39: rpm.macros.sys.tools

# Essential fixes (to ensure that the package can be built on our system)
# [0-99]
Patch0: %name-4.11.2-owl-DT_GNU_HASH.diff

# Fedora patches (this brings our RPM closer to the well supported
# upstream version and consequently we are going to benefit from the
# documentation describing RHEL/CentOS/FC's RPMs)
# [100-199]
Patch100: %name-4.11.x-fc-siteconfig.diff
Patch101: %name-4.9.90-fc-fedora-specspo.diff
Patch102: %name-4.9.90-fc-no-man-dirs.diff
Patch103: %name-4.8.1-fc-use-gpg2.diff
Patch104: %name-4.11.2-fc-double-separator-warning.diff

# the following patches were already submitted and accepted upstream
Patch105: %name-4.11.x-fc-filter-soname-deps.diff
Patch106: %name-4.11.x-fc-do-not-filter-ld64.diff
Patch107: %name-4.11.2-fc-macro-newlines.diff
Patch108: %name-4.11.x-fc-reset-fileactions.diff
Patch109: %name-4.11.2-fc-python3-buildsign.diff
Patch110: %name-4.11.x-fc-rpmdeps-wrap.diff
Patch111: %name-4.11.2-fc-appdata-prov.diff

# the following were not yet submitted/accepted
Patch112: %name-4.6.0-fc-niagara.diff
Patch113: %name-4.7.1-fc-geode-i686.diff
Patch114: %name-4.9.1.1-fc-ld-flags.diff
Patch115: %name-4.10.0-fc-dwz-debuginfo.diff
Patch116: %name-4.10.0-fc-minidebuginfo.diff
Patch117: %name-4.11.1-fc-sepdebugcrcfix.diff
Patch118: %name-4.11.0.1-fc-setuppy-fixes.diff

Patch119: %name-4.9.90-fc-armhfp.diff
Patch120: %name-4.9.0-fc-armhfp-logic.diff

# Our patches and fixes
# [200-299]
Patch200: %name-4.11.2-owl-tmp-scripts.diff
Patch201: %name-4.11.2-owl-brp-scripts.diff
Patch202: %name-4.11.2-owl-db-umask.diff
Patch203: %name-4.11.2-owl-closeall.diff
Patch204: %name-4.11.2-owl-autodeps-symbol-versioning.diff
Patch205: %name-4.11.2-owl-autoreq.diff
Patch206: %name-4.11.2-owl-buildhost.diff
Patch207: %name-4.11.2-owl-rpmrc.diff
Patch208: %name-4.11.2-owl-chroot-ugid.diff
Patch209: %name-4.11.2-owl-compare-digest.diff
Patch210: %name-4.11.2-owl-honor-buildtime.diff
Patch211: %name-4.11.2-owl-doScriptExec-umask.diff
Patch212: %name-4.11.2-owl-grammar.diff
Patch213: %name-4.11.2-owl-remove-unsafe-perms.diff
Patch214: %name-4.11.2-owl-tests.diff
Patch215: %name-4.11.2-owl-plugindir.diff
Patch216: %name-4.11.2-owl-rpmquery-alias.diff
# the following ensures that our platform macros contain only minimal
# subset of substitution macros.
Patch217: %name-4.11.2-owl-macros-platform.diff
# fix the patch macro to bail out if the patch is a broken symlink
Patch218: %name-4.11.2-owl-macro-patch.diff
# get rid of the --disable-dependency-tracking, since it's not always
# available
Patch219: %name-4.11.2-owl-macro-configure.diff
Patch220: %name-4.11.2-owl-no-stack-protector.diff
Patch221: %name-4.11.2-owl-elfdeps-noexec.diff
Patch222: %name-4.11.2-owl-db3-configure.diff
Patch223: %name-4.11.2-owl-db-static-libtool-hack.diff
# the following patch is a band-aid to run tests through a modern fakechroot
Patch224: %name-4.11.2-owl-tests-fakechroot.diff

Requires(post,postun): /sbin/ldconfig
Requires: sh-utils, fileutils, mktemp, gawk
Requires: coreutils
BuildRequires: libtool >= 2.4.2, automake >= 1.14, autoconf >= 2.69
BuildRequires: gettext >= 0.16.1
BuildRequires: elfutils-libelf-devel >= 0:0.108-owl3
BuildRequires: bzip2-devel
BuildRequires: xz-devel
BuildRequires: libnss-devel
BuildRequires: libmagic-devel
BuildRequires: ncurses-devel
%if 0%{?_with_external:1}
BuildRequires: db4-devel >= 4.5
Requires: db4-utils >= 4.5
%endif
%if 0%{?_with_acl:1}
BuildRequires: libacl-devel
%endif
BuildRoot: /override/%name-%rpm_version

%description
The RPM Package Manager (RPM) is a powerful command line driven
package management system capable of installing, uninstalling,
verifying, querying, and updating software packages.  Each software
package consists of an archive of files along with information about
the package like its version, a description, etc.

%package devel
Summary: Development files for applications which will manipulate RPM packages.
Group: Development/Libraries
Requires: %name = %version-%release

%description devel
This package contains the RPM C library and header files.  These
development files will simplify the process of writing programs which
manipulate RPM packages and databases.  These files are intended to
simplify the process of creating graphical package managers or any
other tools that need an intimate knowledge of RPM packages in order
to function.

%package build
Summary: Scripts and executable programs used to build packages.
Group: Development/Tools
Requires: %name = %version-%release
Requires: file

%description build
This package contains scripts and executable programs that are used to
build packages using RPM.

%if 0%{?_with_python:1}
%package python
Summary: Python bindings for apps which will manipulate RPM packages.
Group: Development/Libraries
Requires: rpm = %rpm_version
Requires: python

%description python
The rpm-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by RPM Package Manager libraries.
%endif

%if 0%{?_with_rescue:1}
%package rescue
Summary: Specially compiled RPM binaries for rescue operations.
Group: System Environment/Rescue Tools

%description rescue
This package contains binaries linked in a such way that the only
dynamic dependencies are the libraries residing in /lib, therefore
these binaries can be used for rescue operations when no filesystems
except for the root filesystem are available.

Due to the nature of these binaries (they are mostly static) the
occupied space by this package is quite significant: around 10MB
on your root filesystem.

Another catch is that you need to be familiar with RPM tools since
if %_rpmlibdir is not available you will need to provide the
essential configuration options manually, e.g.:

To get a list of all packages from the database
# /bin/rpm.rescue --rcfile /dev/null --dbpath=/var/lib/rpm -qa

To rebuild the database saving the new copy in /tmp/db
# /bin/rpmdb.rescue --rcfile /dev/null --dbpath=/var/lib/rpm \
  -D '_dbpath_rebuild /tmp/db' -D '_rpmlock_path /tmp' --rebuilddb

To extract the content of a package into the current directory
# /bin/rpm2cpio.rescue package-1.2.3.%_arch.rpm | cpio -mid
%endif

%prep
%setup -q %{?_without_external:-a 1} -a 2

%patch0 -p1 -b .DT_GNU_HASH

%patch100 -p1 -b .siteconfig
# the following two are strictly Fedora-specific
#patch101 -p1 -b .fedora-specspo
#patch102 -p1 -b .no-man-dirs
%patch103 -p1 -b .use-gpg2
%patch104 -p1 -b .double-sep-warning
%patch105 -p1 -b .filter-soname-deps
# I belive that the comparison is somewhat broken in the next patch,
# but there is no risk (they compare less than intended :) ) -- (GM)
%patch106 -p1 -b .dont-filter-ld64
# we may want to enable the following fix since we don't have that
# much legacy packages and the patch addresses an annoying issue.
#patch107 -p1 -b .macro-newlines
%patch108 -p1 -b .reset-fileactions
%patch109 -p1 -b .python3-buildsign
%patch110 -p1 -b .rpmdeps-wrap
%patch111 -p1 -b .appdata-prov
%patch112 -p1 -b .niagara
%patch113 -p1 -b .geode
%patch114 -p1 -b .ldflags
# patch #117 uses glibc 2.9's types from <endian.h>, we don't need the
# functionality provided by these patches as now, so I disabled them.
# eventually, our glibc will be up to date and then we may want to
# re-enable the patches.
#patch115 -p1 -b .dwz-debuginfo
#patch116 -p1 -b .minidebuginfo
#patch117 -p1 -b .sepdebugcrcfix
%patch118 -p1 -b .setuppy-fixes

%patch119 -p1 -b .armhfp
# this patch cant be applied on softfp builds
%ifnarch armv3l armv4b armv4l armv4tl armv5tel armv5tejl armv6l armv7l
%patch120 -p1 -b .armhfp-logic
%endif

%patch200 -p1 -b .tmp-scripts
%patch201 -p1 -b .brp-scripts
%patch203 -p1 -b .closeall
%patch204 -p1 -b .autodeps-symbol-versioning
%patch205 -p1 -b .autoreq
%patch206 -p1 -b .buildhost
%patch207 -p1 -b .rpmrc
%patch208 -p1 -b .chroot-ugid
%patch209 -p1 -b .compare-digest
%patch210 -p1 -b .honor-buildtime
%patch211 -p1 -b .doScriptExec-umask
%patch212 -p1 -b .grammar
%patch213 -p1 -b .remove-unsafe-perms
%patch214 -p1 -b .tests
%patch215 -p1 -b .plugindir
%patch216 -p1 -b .rpmquery-alias
%patch217 -p1 -b .macros-platform
%patch218 -p1 -b .macro-patch
%patch219 -p1 -b .macro-configure
%patch220 -p1 -b .stack-protector
%patch221 -p1 -b .elfdeps-noexec
%patch222 -p1 -b .db3-configure
sed -i '/#set -x/s,^#,,' db3/configure

%if 0%{?_without_external:1}
ln -s $(ls -1td db-%{bdb_version}*/ | %__sed 's,/\+$,,g;q') db
%patch202 -p1 -b .db-umask.diff
%patch223 -p1 -b .db-static-libtool-hack
%endif

%patch224 -p1 -b .tests-fakechroot

cat << EOF > m4/noop.m4
AC_DEFUN([PKG_PROG_PKG_CONFIG], [])dnl
AC_DEFUN([PKG_CHECK_MODULES], [])dnl
EOF

autoreconf -fis

# Replace gendiff with our implementation
mv scripts/gendiff scripts/gendiff.orig
install -p -m 755 '%_sourcedir/gendiff' scripts/

bzip2 -9k ChangeLog

%build
%define __usr            /usr
%define __usrsrc         %__usr/src
%define __var            /var

%ifarch x86_64
%define _lib             lib64
%else
%define _lib             lib
%endif
%define __share          /share
%define __prefix         %__usr
%define __exec_prefix    %__prefix
%define __bindir         %__exec_prefix/bin
%define __sbindir        %__exec_prefix/sbin
%define __libexecdir     %__exec_prefix/%_lib
%define __datadir        %__prefix/share
%define __sysconfdir     /etc
%define __sharedstatedir %__prefix/com
%define __localstatedir  %__var
%define __libdir         %__exec_prefix/%_lib
%define __includedir     %__prefix/include
%define __oldincludedir  /usr/include
%define __infodir        %__datadir/info
%define __mandir         %__datadir/man
%define _rpmlibdir       %__prefix/lib/rpm

prepare()
{
	CC='%__cc' \
	CXX='%__cxx' \
	CPPFLAGS="$(nspr-config --cflags) $(nss-config --cflags) -D_GNU_SOURCE" \
	CFLAGS='%optflags -Wall -fPIC -fno-strict-aliasing' \
	__FAKECHROOT="$(pwd)/tests/fakechroot" \
	../configure \
		--host='%_target_platform' \
		--with-vendor=openwall \
		--prefix='%__usr' \
		--bindir='%__bindir' \
		--sbindir='%__sbindir' \
		--libexecdir='%__libexecdir' \
		--datarootdir='%__datadir' \
		--sysconfdir='%__sysconfdir' \
		--sharedstatedir='%__sharedstatedir' \
		--localstatedir='%__localstatedir' \
		--libdir='%__libdir' \
		--includedir='%__includedir' \
		--oldincludedir='%__oldincludedir' \
		--infodir='%__infodir' \
		--mandir='%__mandir' \
		--enable-largefile \
		--disable-rpath \
		"$@"
}

mkdir 'obj-%_arch.normal'
cd 'obj-%_arch.normal'
%if 0%{?_without_external:1}
ln -s ../db
%endif
prepare \
	--enable-shared \
	%{?_with_static}%{?_without_static} \
	%{?_with_nls} %{?_without_nls} \
	%{?_with_python}%{?_without_python} \
	%{?_with_plugins}%{?_without_plugins} \
	%{?_with_selinux}%{?_without_selinux} \
	%{?_with_external}%{?_without_external}-db \
	%{?_with_acl}%{?_without_acl} \
	%{?_with_cap}%{?_without_cap} \
	%{?_with_lua}%{?_without_lua} \
	--without-beecrypt \
#
ln -s ../../tests/fakechroot tests/
cd ..

cd 'obj-%_arch.normal'
%__make

# Check whether it works at all
./rpm --showrc >/dev/null

cd ..

%if 0%{?_with_rescue:1}
mkdir 'obj-%_arch.rescue'
cd 'obj-%_arch.rescue'
%if 0%{?_without_external:1}
ln -s ../db
%endif
# NOTE: we require static libraries here since we need to link (mostly)
#       static versions of /bin/rpm, rpmdb, and possibly rpm2cpio .
prepare \
	--enable-static \
	--disable-shared \
	--disable-nls \
	--disable-python \
	--disable-plugins \
	--without-beecrypt \
	--without-selinux \
	--without-cap \
	--without-acl \
	--without-lua \
	%{?_with_external}%{?_without_external}-db \
#
ln -s ../../tests/fakechroot tests/

cat << "EOF" > mostly-static.sh
#!/bin/sh
cmd='%__cc'
arg="$1"
while [ -n "$arg" ]; do
        case "$arg" in
                [./]*.so) [ -f "${arg%%.so}.a" ] && arg="${arg%%.so}.a"
                        ;;
                -ldl|-lpthread|-lnss?) ;;
                -l*)    obj=$(%__cc -print-file-name="lib${arg#-l}.a")
                        [ "$obj" = "lib${arg#-l}.a" ] || arg="$obj"
                        ;;
        esac
        cmd="$cmd $arg" ; shift ; arg="$1"
done
echo Executing: $cmd
exec $cmd
EOF
chmod +x mostly-static.sh

# We have a trick in our sleeve ... :)
%__make CCLD="$(pwd)/mostly-static.sh"

# Check whether it works at all
./rpm --showrc >/dev/null

cd ..
%endif

%install
[ '%buildroot' != '/' -a -d '%buildroot' ] && rm -rf -- '%buildroot'

cd 'obj-%_arch.normal'
%__make DESTDIR="%buildroot" install
cd ..

%if 0%{?_with_rescue:1}
# transfer our mostly static binaries for the rescue mode
cp -a 'obj-%_arch.rescue/rpm' '%buildroot/bin/rpm.rescue'
cp -a 'obj-%_arch.rescue/rpmdb' '%buildroot/bin/rpmdb.rescue'
cp -a 'obj-%_arch.rescue/rpm2cpio' '%buildroot/bin/rpm2cpio.rescue'
%endif

mkdir -p '%buildroot%__sysconfdir/rpm'
mkdir -p '%buildroot%_rpmlibdir/macros.d'
mkdir -p '%buildroot%__localstatedir/spool/repackage'
mkdir -p '%buildroot%__localstatedir/lib/rpm'
for dbi in \
    Basenames Conflictname Dirnames Group Installtid Name Obsoletename \
    Packages Providename Requirename Triggername Sha1header Sigmd5 \
    Filemd5s Pubkeys \
    __db.001 __db.002 __db.003 __db.004 __db.005 __db.006 __db.007 \
    __db.008 __db.009
do
	touch '%buildroot%__localstatedir'/lib/rpm/$dbi
done

%if 0%{?_with_external:1}
for dbutil in dump load recover stat upgrade verify
do
	# XXX: need to calculate relative path from absolute here
	ln -sv ../../bin/db_$dbutil '%buildroot%_rpmlibdir'/rpmdb_$dbutil
done
%endif

%if 0%{?_with_plugins:1}
%if %_lib == lib64
mv '%buildroot%__libdir/rpm/plugins' '%buildroot%_rpmlibdir/'
%endif
%endif

# Remove unpackaged files
#
find '%buildroot' -type f -name '*.la' -delete

# the platform directory under %%_rpmlibdir contains too many platforms.
# let's pick the ones we support and drop all the rest.  All in all, the
# platform subdirectory contains just the macros file tweaked toward the
# corresponding platform, hence can be easily recreated.
mv -- '%buildroot%_rpmlibdir/platform'{,.orig}
mkdir '%buildroot%_rpmlibdir/platform'
mv -- '%buildroot%_rpmlibdir/platform'.orig/{i?86,x86_64,pentium*,athlon,geode,noarch}-linux \
	'%buildroot%_rpmlibdir/platform/'
rm -r -- '%buildroot%_rpmlibdir/platform.orig'

# unneeded crontab, logrotate config, valgrind config
rm -- '%buildroot%_rpmlibdir'/rpm.{daily,log,supp}
# i18n man pages (let's stick to English only for now)
rm -r -- '%buildroot%__mandir'/??

install -p -m 755 '%_sourcedir/rpminit' '%buildroot%__bindir/'
install -p -m 644 '%_sourcedir/rpminit.1' '%buildroot%__mandir/man1/'
install -p -m 644 '%_sourcedir/configure-presets' '%buildroot%__bindir/'

# install macro definitions
install -p -m 644 '%_sourcedir/rpm.macros' \
	'%buildroot%_rpmlibdir/macros'
for f in '%_sourcedir/rpm.macros'.* ; do
	install -p -m 644 "$f" \
		"%buildroot%_rpmlibdir/macros.d/${f#%_sourcedir/rpm.}"
done
# update essential macros in macros.sys.platform
sed -i 's,@host@,%_host,;
	s,@host_alias@,%_host_alias,;
	s,@host_cpu@,%_host_cpu,;
	s,@host_vendor@,%_host_vendor,;
	s,@host_os@,%_host_os,' \
		'%buildroot%_rpmlibdir/macros.d/macros.sys.platform'

# it's possible that there are no language files, e.g. if the package
# was built with the --disable-nls option, hence we need to be ready
# for that.
%find_lang %name || :
touch '%name.lang'

%check
%{expand:%%{!?_with_test: %%{!?_without_test: %%global _with_test --with-test}}}
if [ -z "$(hostname -f 2>/dev/null)" ]; then
	cat << EOF
WARNING: our quick check indicates that the host name assigned to this
         environment ($(hostname 2>/dev/null)) cannot be canonicalized.
         There are more than a hundred tests in RPM's testsuite which rely
         on a properly configured host name.

         The quickest fix for this issue would be to run 'hostname',
         and add the displayed host name to /etc/hosts (the file should
         be world-readable, e.g. 'chmod 0644 /etc/hosts').
EOF
	exit 1
fi

# RPM's testsuite requires fakechroot, let's build one right here
ln -sf $(ls -1td fakechroot-*/ | %__sed 's,/\+$,,g;q') fakechroot
pushd fakechroot
for f in patches/*.diff ; do
	patch -p1 -Z < "$f"
done
# disable tests thet fail if the fake chroot directory is too deep
sed -i 's,t/socket-af_unix\.t,,' test/Makefile.am
autoreconf -fis -I m4
CFLAGS='%optflags -fPIC' \
%configure
%__make
# fakechroot's testsuite is picky about the current working directory
cd "$(pwd -P)"
%__make check
popd

cat << EOF > tests/fakechroot
#!/bin/bash
# fix paths since RPM testsuite is really broken in regard to the modern
# fakechroot that emulates almost a proper chroot environment.
args=("\$@")
for (( i=0 ; i < \${#args[@]} ; i++ )); do
        args[\$i]=\${args[i]//\$FAKECHROOT_BASE}
done
set -- "\${args[@]}"
unset args
LD_LIBRARY_PATH=\${LD_LIBRARY_PATH//\$FAKECHROOT_BASE} \
PATH=/usr/bin:/bin:/usr/bin:/usr/local/bin:/sbin:/usr/sbin:/usr/local/sbin \
PYTHONPATH=\${PYTHONPATH//\$FAKECHROOT_BASE} \
RPM_CONFIGDIR=\${RPM_CONFIGDIR//\$FAKECHROOT_BASE} \
RPM_POPTEXEC_PATH=\${RPM_POPTEXEC_PATH//\$FAKECHROOT_BASE} \
HOME=/ \
TOPDIR=/build \
LD_PRELOAD=$(pwd)/fakechroot/src/.libs/libfakechroot.so "\$@"
EOF
chmod +x tests/fakechroot

# now we are ready to test
cd 'obj-%_arch.normal'
%__make check
%if 0%{?_with_rescue:1}
cd '../obj-%_arch.rescue'
%__make check
%endif
cd ..

%post
/sbin/ldconfig

# ToDo: (GM): It is good to run "rpmd --rebuilddb" after upgrading rpm, but
# it is not so trivial. Rebuild process has to start _after_ this package is
# installed, so we will have to hack the installation process. One way to
# do this thing can be seen in ALT Linux's rpm.spec, they fire a special
# helper which waits for main RPM process exit and runs specified program.
# For now, we assume that "make installworld" (Owl installation and upgrade
# procedure) does all the dirty work for us. :)

%postun -p /sbin/ldconfig

%triggerpostun -- %name < 4.2-owl22
# Remove __db.00? files that look like they're pre-NPTL.  We may be removing
# files that are opened and/or memory-mapped by us (by the rpm process that
# installs the new rpm package), but that's OK.  The next invocation of rpm
# will recreate the files.  4.2-owl22 is when we added this trigger, and we
# were already using NPTL at the time, so there is no need to perform the
# size check and possibly remove the files when upgrading from newer versions.
RPMDBDIR=/var/lib/rpm
if [ -f $RPMDBDIR/__db.001 -a "`wc -c < $RPMDBDIR/__db.001`" -le 8192 ]; then
	rm -f $RPMDBDIR/__db.00?
fi

%files -f %name.lang
%defattr(0644,root,root,0755)
%doc ChangeLog.bz2 COPYING CREDITS
%dir %__sysconfdir/rpm
%dir %__localstatedir/lib/rpm
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %__localstatedir/lib/rpm/[A-Z]*
%ghost %attr(0600,root,root) %verify(not md5 size mtime)  %__localstatedir/lib/rpm/__db.*
%attr(0755,root,root) /bin/rpm
%attr(0755,root,root) %__bindir/rpm2cpio
%attr(0755,root,root) %__bindir/rpmdb
%attr(0755,root,root) %__bindir/rpmgraph
%attr(0755,root,root) %__bindir/rpmkeys
%attr(0755,root,root) %__bindir/rpmsign
# the following 2 are symlinks, so not %%attr() for them
%__bindir/rpmquery
%__bindir/rpmverify
%__libdir/librpm.so.*
%__libdir/librpmio.so.*
%__libdir/librpmsign.so.*
%__mandir/man8/rpm.8*
%__mandir/man8/rpm2cpio.8*
%__mandir/man8/rpmdb.8*
%__mandir/man8/rpmgraph.8*
%__mandir/man8/rpmkeys.8*
%__mandir/man8/rpmsign.8*
%if 0
%__mandir/*/man8/rpm.8*
%__mandir/*/man8/rpm2cpio.8*
%__mandir/*/man8/rpmgraph.8*
%endif
%dir %_rpmlibdir
%_rpmlibdir/rpmpopt-4.11.2
%_rpmlibdir/rpmrc
%_rpmlibdir/macros
%dir %_rpmlibdir/macros.d
%attr(0644,root,root) %_rpmlibdir/macros.d/macros.sys.*
%_rpmlibdir/platform
%dir %__localstatedir/spool/repackage

%attr(0755,root,root) %_rpmlibdir/rpmdb_dump
%attr(0755,root,root) %_rpmlibdir/rpmdb_load
%attr(0755,root,root) %_rpmlibdir/rpmdb_recover
%attr(0755,root,root) %_rpmlibdir/rpmdb_stat
%attr(0755,root,root) %_rpmlibdir/rpmdb_upgrade
%attr(0755,root,root) %_rpmlibdir/rpmdb_verify

%if 0%{?_with_plugins:1}
%dir %_rpmlibdir/plugins
%_rpmlibdir/plugins/exec.so
%else
%exclude %_rpmlibdir/plugins/exec.so
%endif

%files build
%doc doc/manual/[a-z]*
%attr(0644,root,root) %__bindir/configure-presets
%attr(0755,root,root) %__bindir/gendiff
%attr(0755,root,root) %__bindir/rpmbuild
%attr(0755,root,root) %__bindir/rpminit
%attr(0755,root,root) %__bindir/rpmspec
%__libdir/librpmbuild.so.*
%__libdir/pkgconfig/rpm.pc
%attr(0755,root,root) %_rpmlibdir/appdata.prov
%attr(0755,root,root) %_rpmlibdir/brp-compress
%attr(0755,root,root) %_rpmlibdir/brp-java-gcjcompile
%attr(0755,root,root) %_rpmlibdir/brp-python-bytecompile
%attr(0755,root,root) %_rpmlibdir/brp-python-hardlink
%attr(0755,root,root) %_rpmlibdir/brp-strip
%attr(0755,root,root) %_rpmlibdir/brp-strip-comment-note
%attr(0755,root,root) %_rpmlibdir/brp-strip-shared
%attr(0755,root,root) %_rpmlibdir/brp-strip-static-archive
%attr(0755,root,root) %_rpmlibdir/check-buildroot
%attr(0755,root,root) %_rpmlibdir/check-files
%attr(0755,root,root) %_rpmlibdir/check-prereqs
%attr(0755,root,root) %_rpmlibdir/check-rpaths
%attr(0755,root,root) %_rpmlibdir/check-rpaths-worker
%attr(0755,root,root) %_rpmlibdir/config.guess
%attr(0755,root,root) %_rpmlibdir/config.sub
%attr(0755,root,root) %_rpmlibdir/debugedit
%attr(0755,root,root) %_rpmlibdir/desktop-file.prov
%attr(0755,root,root) %_rpmlibdir/elfdeps
%attr(0755,root,root) %_rpmlibdir/find-debuginfo.sh
%attr(0755,root,root) %_rpmlibdir/find-lang.sh
%attr(0755,root,root) %_rpmlibdir/find-provides
%attr(0755,root,root) %_rpmlibdir/find-requires
%attr(0755,root,root) %_rpmlibdir/fontconfig.prov
%attr(0755,root,root) %_rpmlibdir/libtooldeps.sh
%attr(0644,root,root) %_rpmlibdir/macros.d/macros.build
%attr(0644,root,root) %_rpmlibdir/macros.d/macros.build.*
%attr(0755,root,root) %_rpmlibdir/mkinstalldirs
%attr(0755,root,root) %_rpmlibdir/mono-find-provides
%attr(0755,root,root) %_rpmlibdir/mono-find-requires
%attr(0755,root,root) %_rpmlibdir/ocaml-find-provides.sh
%attr(0755,root,root) %_rpmlibdir/ocaml-find-requires.sh
%attr(0755,root,root) %_rpmlibdir/osgideps.pl
%attr(0755,root,root) %_rpmlibdir/perl.prov
%attr(0755,root,root) %_rpmlibdir/perl.req
# the following script was supposed to be a replacement for perl.prov and
# perl.req, but it seems it failed.  RPM isn't configured to use it, yet
# including it brings a dependency on Module::ScanDeps::DataFeed .
%exclude %attr(0755,root,root) %_rpmlibdir/perldeps.pl
%attr(0755,root,root) %_rpmlibdir/pkgconfigdeps.sh
%attr(0755,root,root) %_rpmlibdir/pythondeps.sh
%attr(0755,root,root) %_rpmlibdir/rpm2cpio.sh
%attr(0755,root,root) %_rpmlibdir/rpmdb_loadcvt
%attr(0755,root,root) %_rpmlibdir/rpmdeps
%attr(0755,root,root) %_rpmlibdir/script.req
%attr(0755,root,root) %_rpmlibdir/tcl.req
%attr(0755,root,root) %_rpmlibdir/tgpg
%dir %_rpmlibdir/fileattrs
%_rpmlibdir/fileattrs/*.attr
%_rpmlibdir/macros.perl
%_rpmlibdir/macros.php
%_rpmlibdir/macros.python
%__mandir/man1/gendiff.1*
%__mandir/man1/rpminit.1*
%__mandir/man8/rpmbuild.8*
%__mandir/man8/rpmdeps.8*
%__mandir/man8/rpmspec.8*
%if 0
%__mandir/*/man8/rpmbuild.8*
%__mandir/*/man1/gendiff.1*
%__mandir/*/man8/rpmdeps.8*
%endif

%files devel
%defattr(0644,root,root,0755)
%__includedir/rpm
%__libdir/librpm.so
%__libdir/librpmbuild.so
%__libdir/librpmio.so
%__libdir/librpmsign.so
%if 0%{?_with_static:1}
%__libdir/librpm.a
%__libdir/librpmbuild.a
%__libdir/librpmio.a
%__libdir/librpmsign.a
%endif

%if 0%{?_with_rescue:1}
%files rescue
%defattr(0644,root,root,0755)
%attr(0755,root,root) /bin/rpm*.rescue
%endif

%changelog
* Thu Jun 19 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.11.2-owl1
- Updated to 4.11.2.
- Regenerated applicable patches, dropped ones which are no longer
applicable or were implemented upstream.
- Introduced a testsuite to check the resulting binaries.
- Introduced an option to build a special, rescue version of rpm, rpmdb,
and rpm2cpio.

* Tue Aug 14 2012 Vasiliy Kulikov <segoon-at-owl.openwall.com> 4.2-owl29
- Instead of using -lXXX used specific libXXX.la files from the build tree.
Old scheme wrongly used system libraries insteaf of in-tree libraries.  It
added a dependency of rpm-devel package for building rpm.

* Sun Jul 22 2012 Vasiliy Kulikov <segoon-at-owl.openwall.com> 4.2-owl28
- Added multiple -lXXX into LDFLAGS to fix build error under binutils >= 2.21.

* Mon Oct 10 2011 Solar Designer <solar-at-owl.openwall.com> 4.2-owl27
- Added a patch for CVE-2011-3378 (crash and potential arbitrary code execution
on malformed package file headers) taken from RHEL 4 update package
rpm-4.3.3-35_nonptl.el4.src.rpm.
- Build beecrypt with -Wa,--noexecstack.

* Mon Jul 25 2011 Solar Designer <solar-at-owl.openwall.com> 4.2-owl26
- Added a patch to remove unsafe file permissions (chmod'ing files to 0) on
package removal or upgrade to prevent continued access to such files via
hard-links possibly created by a user (CVE-2005-4889, CVE-2010-2059).

* Mon May 02 2011 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2-owl25
- Fixed %%patch regression introduced in previous release.
Reported by Chris Bopp (http://www.openwall.com/lists/owl-dev/2011/05/02/1).

* Mon Sep 06 2010 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2-owl24
- Backported xz/lzma support in %%setup and %%patch macros.
- Backported xz/lzma payload support.

* Thu Sep 02 2010 Solar Designer <solar-at-owl.openwall.com> 4.2-owl23
- Moved a relevant comment to inside %%triggerpostun such that it does not
affect RPM's processing of the preceding "%%postun -p /sbin/ldconfig".
Thanks to Pavel Kankovsky for figuring this out.

* Tue Mar 30 2010 Solar Designer <solar-at-owl.openwall.com> 4.2-owl22
- Added a trigger to remove __db.00? files that look like they're pre-NPTL.

* Fri Nov 27 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2-owl21
- Changed default build architecture on i686+ CPUs to i686.

* Wed Sep 09 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2-owl20
- Implemented automated %%check control using --with/--without
check/test switches.

* Fri Aug 21 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2-owl19
- Predefined a bunch of autoconf variables by sourcing new configure-presets
script in %%___build_pre macro, to harden configure checks for security
sensitive functions, and to speedup configure checks for most popular
functions.
- Fixed gendiff to avoid producing changelog diffs with no context.

* Fri Aug 17 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2-owl18
- Changed rpmbuild to pass --wildcards to tar on build from tarball.

* Sun Nov 19 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2-owl17
- Backported upstream fix for potential heap buffer overflow in
showQueryPackage function (CVE-2006-5466).
- Added x86-64 support to rpminit script.

* Sun May 07 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl16
- Removed unused macros: WITH_INCLUDED_GETTEXT, WITH_API_DOCS, and WITH_BZIP2.
- Added a dependency on the file package to rpm-build (find-provides is
using the file utility).

* Tue Apr 04 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2-owl15
- Backported upstream fix to check-prereqs script.
- Corrected specfile to make it build on x86_64.
- Updated rpmrc optflags for x86_64.

* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2-owl14
- Compressed CHANGES file.

* Sat Dec 24 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2-owl13
- Corrected build to generate proper values for %%_host, %%_host_alias,
%%_host_cpu and %%_host_vendor macros.

* Wed Dec 21 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2-owl12
- Fixed build to avoid linking of librpmbuild with system librpm.

* Fri Nov 18 2005 Solar Designer <solar-at-owl.openwall.com> 4.2-owl11
- Added public domain statements to the rpminit script and its man page.

* Sat Nov 05 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2-owl10
- Fixed macro files which appeared to be incomplete due to outdated
vendor autodetection code in configure scripts.

* Mon Oct 17 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2-owl9
- Backported fix to nested %if handling.
- Changed package upgrade algorithm to remove old files
on "-U --force" even if package versions match.
- When comparing package versions on -U or -F, take build dates
into account.
- Set umask 022 for install scripts and triggers execution.
- Build debugedit utility with system libelf.
- Applied sparc optflags update from Alexandr Kanevskiy.

* Fri Sep 23 2005 Michail Litvak <mci-at-owl.openwall.com> 4.2-owl8
- Don't package .la files.

* Sat Jun 25 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.2-owl7
- Do not use system's libelf even if the library is available during build.

* Sat Apr 02 2005 Solar Designer <solar-at-owl.openwall.com> 4.2-owl6
- Allow unpackaged files and missing docs by default for building legacy
third-party packages (our build environment overrides this for native ones).
- Re-implemented the gendiff script.

* Tue Mar 22 2005 Solar Designer <solar-at-owl.openwall.com> 4.2-owl5
- Updated the default rpmrc to use -march/-mtune as required for gcc 3.4.3+
and to use -pipe with all supported archs.

* Sun Mar 20 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl4
- Fixed a bug with creating and packaging /var/lib/lib/rpm.

* Wed Jan 05 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl3
- Applied rpmal-bounds patch to avoid going out of array bounds in the
dependency checker.

* Sun Dec 26 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl2
- Applied chroot-ugid patch to not rely on host OS provided NSS modules.

* Tue Nov 02 2004 Solar Designer <solar-at-owl.openwall.com> 4.2-owl1
- Corrected the long text messages for consistency with owl-etc.
- Set Release to -owl1 such that we can make this public.

* Wed Sep 29 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.18
- Added db1 format support into rpmdb
- Fixed configure.ac to use proper AC_CONFIG_HEADERS syntax
- Removed "create" from __dbi_cdb definition in macros.in, because it breaks upgrade logic
- Modified %%pre section to be more friendly to end-user

* Wed May 05 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.17
- Finally fixed the problem with db environment opens inside & outside chroot.

* Mon Mar 22 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.16
- Quick and dirty fix for the problem with installing into a chroot jail
from read-only filesystem. (Discovered by Solar Designer)

* Fri Mar 19 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.15
- Fixed problem during package upgrade with Obsoletes tag pointed to
not installed package
- Removed unneeded PreReqs, added necessary Requires

* Thu Mar 11 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.14
- Fixed permissions during install of packages. Not explictly included
directories (that is, those in the middle of an included pathname) will be
created with mode 755, all files will be created with mode 600 and then
chmod'ed to the specified access rights.

* Wed Mar 10 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.13
- Minor changes to the spec file (exporting CFLAGS, making sure that any
passed value of CFLAGS gets into compilation process).

* Thu Mar 04 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.12
- Changed type of rpmError for errors during opening of /etc/mtab from error
to debug.
- Modified version of Owl RPM3 closeall patch added
- Modified version of Owl RPM3 gendiff patch added
- Regenerated Owl RPM3 patches: autodeps-symbol-versioning, autoreq,
buildhost, popt-sgid, rpmrc
- Added vendor-setup patch to setup our environment (compatible with RH)

* Wed Mar 03 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.11
- Added missing --enable-posixmutexes option to configure

* Fri Feb 20 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.10
- Removed unnecessary verify prefix from rpmmacros and rpmpopt
- Applied style corrections as described by Solar Designer

* Mon Feb 16 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.9
- It seems to be first fully working version of this package and drop-in
replacement for rpm 3.0.6 (except upgrade procedure)
- Applied patch to ignore umask and follow the logical behavior of honoring
permissions settings in the macros.

* Fri Feb 13 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.8
- Fixed issue with platforms directories

* Thu Feb 12 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.7
- Changed macros file to use external dependency generator (internal one
is very ugly :( )
- Minor changes in %_libdir/rpm directory

* Wed Feb 11 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.6
- Fixed brp- scripts

* Tue Feb 10 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.5
- Cleaned up the spec file (to use macros in file sections)
- Added %%config to configuration files
- Fixed permissions on platform directories under %__libdir/rpm/

* Mon Feb 09 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.4
- Making only libelf.a from elfutils, not 'make all' in libelf subdirectory
- Removed dependency on gcc3+ and binutils 2.14.90+

* Thu Feb 05 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.3
- Tested building of this package under rpm 3.0.6 and rebuilding under
rpm 4.2
- Added -DMAGIC option to CFLAGS for configure in file subdirectory to
hardcode correct path to file's magic database in /usr/share
- Linked rpmq, rpmv and rpmdeps to static librpmbuild to avoid rpm-build
dependency from rpm
- Added missing rpmrc, rpmdeps

* Wed Feb 04 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.2
- Moved compilation of libelf.a, libfmagic.so to prep and removed
source trees for elfutils and file (Hope, someday we will package
them independently).
- Solved problem with linking librpm.so.0 into librpmbuild if we're
building on a system with installed rpm 3.x

* Tue Feb 03 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.2-owl0.1
- Updated to version 4.2
- Spec file was heavily reviewed

* Fri Jan 16 2004 Michail Litvak <mci-at-owl.openwall.com> 3.0.6-owl11
- Make /usr/lib/rpm directory owned by this package.

* Fri Dec 12 2003 Solar Designer <solar-at-owl.openwall.com> 3.0.6-owl10
- In brp-strip*, use sed expressions which allow SUID/SGID binaries to get
stripped.

* Sun Dec 07 2003 Solar Designer <solar-at-owl.openwall.com> 3.0.6-owl9
- Don't use a file under /tmp in installplatform script used during builds,
spotted by (GalaxyMaster).

* Tue May 27 2003 Solar Designer <solar-at-owl.openwall.com> 3.0.6-owl8
- Obey AutoReq: false also for dependency on the shell with triggers.

* Thu May 15 2003 Solar Designer <solar-at-owl.openwall.com> 3.0.6-owl7
- Don't call gzerror() after gzclose(), patch from Dmitry V. Levin.

* Wed Apr 30 2003 Solar Designer <solar-at-owl.openwall.com> 3.0.6-owl6
- In popt, handle uses from SGID apps in the same way as from SUID ones.

* Sun Feb 23 2003 Michail Litvak <mci-at-owl.openwall.com>
- Fixed misplaced semicolon in /usr/lib/rpm/macros file
  (Thanks to Oleg Lukashin)

* Fri Jan 17 2003 Solar Designer <solar-at-owl.openwall.com>
- In find-requires, support symbol versioning with package dependencies
for libraries other than glibc (from Dmitry V. Levin of ALT Linux).

* Tue Dec 17 2002 Solar Designer <solar-at-owl.openwall.com>
- Added rpminit, a script to create private RPM package build directories,
and its man page.
- Changed the default rpmrc to use more optimal optflags for our gcc (note
that builds of Owl itself use a different set of optflags anyway).

* Sun Mar 03 2002 Solar Designer <solar-at-owl.openwall.com>
- Support setting the BuildHost tag explicitly rather than only from what
the kernel thinks the system's hostname is.
- Don't package vpkg-provides* (temporary file handling issues, non-Linux).
- Don't package rpmgettext/rpmputtext because of poor quality and no uses
by RPM itself.

* Wed Feb 06 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Tue Jun 12 2001 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- update to 3.0.6 release

* Thu Nov 30 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- disable /usr/src/RPM for security reasons

* Sun Nov 19 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- gendiff fix

* Sun Nov 12 2000 Solar Designer <solar-at-owl.openwall.com>
- Added missing #include's to lib/rpmio.c (it wouldn't build with a
sparc64 kernel).

* Fri Oct 20 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- disabled /usr/share/man autodetection

* Sun Sep 03 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- vendor fix
- FHS
- closeall security fix
- RH 6.2 updates merge

* Sat Aug 05 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- change build target
- /usr/src/redhat -> /usr/src/RPM

* Thu Jul 20 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import from official RPM team test rpm.
- disable Python module
