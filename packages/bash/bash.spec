# $Owl: Owl/packages/bash/bash.spec,v 1.52 2014/09/26 23:07:54 solar Exp $

Summary: The GNU Bourne-Again SHell (Bash).
Name: bash
%define bash_version 3.1
%define bash_patchlevel 19
Version: %bash_version.%bash_patchlevel
Release: owl1
Group: System Environment/Shells
License: GPL
# ftp://ftp.gnu.org/gnu/bash/bash-%bash_version.tar.gz
Source0: bash-%bash_version.tar.bz2
# ftp://ftp.gnu.org/gnu/bash/bash-doc-%bash_version.tar.gz
Source1: bash-doc-%bash_version.tar.bz2
Source2: profile
Source3: bashrc
Source4: dot-bashrc
Source5: dot-bash_profile
Source6: dot-bash_logout
Patch0: bash-3.1-up-patchlevel.diff
Patch10: bash-3.1-owl-warnings.diff
Patch11: bash-3.1-owl-tmp.diff
Patch12: bash-3.1-owl-vitmp.diff
Patch13: bash-3.1-owl-defaults.diff
Patch14: bash-3.1-alt-man.diff
Patch15: bash-3.1-alt-unbound.diff
Patch16: bash-3.1-alt-dlopen.diff
Patch20: bash-3.1-rh-login.diff
Patch21: bash-3.1-rh-ulimit.diff
Patch22: bash-3.1-rh-setlocale.diff
Patch23: bash-3.1-rh-read-memleak.diff
Patch24: bash-3.1-rh-alt-requires.diff
Patch25: bash-3.1-rh-man.diff
Patch26: bash-3.1-rh-info-tags.diff
Patch30: bash-3.1-deb-random.diff
Patch31: bash-3.1-deb-doc.diff
Patch32: bash-3.1-up-rl_completion_append_character.diff
Patch100: readline-5.1-up-pl1.diff
Patch101: readline-5.1-alt-warnings.diff
Patch102: readline-5.1-alt-nls.diff
Patch103: readline-5.1-deb-alt-inputrc.diff
Patch104: readline-5.1-rh-wrap.diff
Requires: mktemp >= 1:1.3.1
Provides: bash2
Obsoletes: bash2, etcskel
BuildRequires: mktemp >= 1:1.3.1, readline-devel >= 0:4.3, rpm-build >= 0:4
BuildRoot: /override/%name-%version

%description
The GNU Bourne Again shell (Bash) is a shell or command language
interpreter that is compatible with the Bourne shell (sh).  Bash
incorporates useful features from the Korn shell (ksh) and the C shell
(csh).  Most sh scripts can be run by bash without modification.

Documentation and examples for bash are contained in the bash-doc package.

%package devel
Summary: Bash loadable builtins development files.
Group: Development/Libraries
Requires: %name = %version-%release

%description devel
GNU Bourne Again shell (bash) can dynamically load new builtin commands.
This package contains header files necessary to compile custom builtins.

%package doc
Summary: Documentation for the GNU Bourne Again shell (bash).
Group: Documentation
Obsoletes: bash2-doc

%description doc
This package contains documentation for the GNU Bourne Again shell
version %version.

%prep
%setup -q -a1 -n bash-%bash_version
%patch0 -p0
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
pushd lib/readline
%patch100 -p0
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
popd

bzip2 -9k CHANGES NEWS doc/FAQ

# Prevent bogus dependencies
find examples -type f -print0 | xargs -r0 chmod -x --

%{expand:%%define optflags %optflags -Wall}

%build
# Remove files which should be regenerated during build
rm configure y.tab.? doc/*.info*

# Bundled texi2dvi is outdated
install -pm755 /usr/bin/texi2dvi support/

# Fix temporary file handling
sed -i 's,/tmp/,,g' aclocal.m4

# Would anyone volunteer to fix those? Probably not
find examples -type f -print0 |
	xargs -r0 grep -FlZ -- /tmp |
	xargs -r0 rm -f --

autoconf
export \
	bash_cv_dev_fd=standard \
	bash_cv_dev_stdin=present \
	bash_cv_mail_dir=/var/mail

%configure \
	--disable-net-redirections \
	--disable-restricted \
	--enable-separate-helpfiles \
	--without-bash-malloc \
	--without-curses \
	--without-installed-readline

%__make

%check
%{expand:%%{!?_with_test: %%{!?_without_test: %%global _without_test --without-test}}}
%__make check

%install
rm -rf %buildroot

%makeinstall

mkdir -p %buildroot/bin
mv %buildroot%_bindir/bash %buildroot/bin/
ln -s bash %buildroot/bin/sh
ln -s bash %buildroot/bin/bash2

ln -s bash.1 %buildroot%_mandir/man1/sh.1
ln -s bash.1 %buildroot%_mandir/man1/bash2.1

# Install header files necessary to compile custom builtins.
mkdir -p %buildroot%_includedir/bash
for f in examples/loadables/*.c; do
	%__cc -MM -DHAVE_CONFIG_H -DSHELL -Iexamples/loadables -I. -Ilib -Ibuiltins -Iinclude "$f"
done |
	tr -d '\:' |
	tr -s '[:space:]' '\n' |
	fgrep .h |
	fgrep -v examples/loadables/ |
	sort -u |
	while read f; do
		install -pm644 "$f" %buildroot%_includedir/bash/
	done

# Prepare documentation.
%define docdir %_docdir/%name-%version
mkdir -p %buildroot%docdir/{html,ps,txt}
install -pm644 \
	AUTHORS CHANGES COMPAT NEWS NOTES POSIX doc/{FAQ,INTRO} \
	%buildroot%docdir/
install -pm644 doc/*.html %buildroot%docdir/html/
install -pm644 doc/*.ps %buildroot%docdir/ps/
install -pm644 doc/*.txt %buildroot%docdir/txt/
find %buildroot%docdir/{[A-Z],txt/}* -type f -size +8k -print0 |
	xargs -r0 bzip2 -9 --
gzip -9nf %buildroot%docdir/ps/*.ps
cp -a examples %buildroot%docdir/
find %buildroot%docdir/examples/ -type f -name 'Makefile*' -delete
# We build bash with --disable-restricted option.
find %buildroot%docdir/ -iname '*rbash*' -delete

# Prepare sample Makefile for building custom builtins.
cat >%buildroot%docdir/examples/loadables/Makefile <<'EOF'
CC = %__cc
CPPFLAGS = -DHAVE_CONFIG_H -I. -I%_includedir/bash
CFLAGS = %optflags %optflags_shared
LDFLAGS = -shared

%%.so: %%.c
	$(LINK.c) $^ $(LOADLIBES) $(LDLIBS) -o $@
EOF

cd doc
# Make manpages for bash builtins as per suggestion in doc/README
sed '
/^\.SH NAME/, /\\- bash built-in commands$/{
/^\.SH NAME/d
s/^bash, //
s/\\- bash built-in commands$//
s/,//g
b
}
d
' builtins.1 > man.pages
for c in `cat man.pages`; do
	ln -s builtins.1 %buildroot%_mandir/man1/$c.1
done

cd %buildroot
# These conflict with real manpages
rm .%_mandir/man1/{echo,kill,printf,pwd,test}.1

mkdir -p etc/skel
install -pm 644 %_sourcedir/profile etc/
install -pm 644 %_sourcedir/bashrc etc/
install -pm 644 %_sourcedir/dot-bashrc etc/skel/.bashrc
install -pm 644 %_sourcedir/dot-bash_profile etc/skel/.bash_profile
install -pm 644 %_sourcedir/dot-bash_logout etc/skel/.bash_logout

# Remove unpackaged files
rm %buildroot%_infodir/dir

%triggerin -- libtermcap
if [ ! -f /etc/shells ]; then
	echo "/bin/sh" >> /etc/shells
	echo "/bin/bash" >> /etc/shells
	echo "/bin/bash2" >> /etc/shells
elif [ -x /bin/grep ]; then
	grep -q '^/bin/sh$' /etc/shells || \
		echo "/bin/sh" >> /etc/shells
	grep -q '^/bin/bash$' /etc/shells || \
		echo "/bin/bash" >> /etc/shells
	grep -q '^/bin/bash2$' /etc/shells || \
		echo "/bin/bash2" >> /etc/shells
fi

%preun
if [ $1 -eq 0 -a -x /bin/grep ]; then
	grep -vE '^/bin/sh$|^/bin/bash$|^/bin/bash2$' \
		/etc/shells > /etc/shells.bash-un
	mv /etc/shells.bash-un /etc/shells
	test -s /etc/shells || rm /etc/shells
fi

%files
%defattr(-,root,root)
%config(noreplace) /etc/profile
%config(noreplace) /etc/bashrc
%config(noreplace) /etc/skel/.b*
%dir %docdir
%docdir/[A-Z]*
/bin/sh
/bin/bash
/bin/bash2
%_datadir/bash
%_infodir/bash.info*
%_mandir/man1/*.1*
%_mandir/man1/..1*
%_bindir/bashbug
%_datadir/locale/en@*/LC_MESSAGES/bash.mo

%files devel
%defattr(-,root,root)
%_includedir/bash
%dir %docdir
%dir %docdir/examples
%docdir/examples/loadables

%files doc
%defattr(-,root,root)
%dir %docdir
%docdir/examples
%exclude %docdir/examples/loadables
%docdir/html
%docdir/ps
%docdir/txt

%changelog
* Sat Sep 27 2014 Solar Designer <solar-at-owl.openwall.com> 3.1.19-owl1
- Updated to 3.1 patchlevel 19.

* Thu Sep 25 2014 Solar Designer <solar-at-owl.openwall.com> 3.1.18-owl1
- Updated to 3.1 patchlevel 18.

* Sat Jun 28 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.1.17-owl8
- Regenerated the owl-warnings patch since it was fuzzy.

* Sat Dec 04 2010 Solar Designer <solar-at-owl.openwall.com> 3.1.17-owl7
- Revised the default shell prompt per gremlin@'s suggestion.

* Tue Mar 30 2010 Solar Designer <solar-at-owl.openwall.com> 3.1.17-owl6
- Moved /etc/profile and /etc/bashrc from the owl-etc package to this one.

* Mon Mar 22 2010 Solar Designer <solar-at-owl.openwall.com> 3.1.17-owl5
- Added upstream fix (introduced in 4.x) to reset the character appended to
pathnames on completion such that it does not get stuck at '/'.

* Mon Oct 08 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.1.17-owl4
- Moved bash examples to -doc subpackage.
- Repackaged documentation to reside in single directory inside %_docdir/.

* Sun Oct 07 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.1.17-owl3
- Added missing check for unbound variables (Alexey Tourbin).
- In "enable" builtin, set RTLD_NOW flag in dlopen(3) call.
- Imported FC fix for out of date tags (RH#150118).
- Packaged -devel subpackage with header files necessary to compile
custom builtins.

* Wed Feb 21 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.1.17-owl2
- Fixed redundant RLIMIT_LOCKS in "ulimit -a", reported by galaxy@owl.

* Tue Jun 06 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.1.17-owl1
- Updated to 3.1 patchlevel 17.

* Tue Apr 04 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.1.16-owl1
- Updated to 3.1 patchlevel 16.

* Mon Feb 20 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.1.8-owl1
- Updated to 3.1 patchlevel 8.

* Wed Feb 08 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.1.7-owl1
- Updated to 3.1 patchlevel 7.
- Imported FC fix for bug in setting login shell invocation attribute.
.
* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.1.5-owl2
- Compressed CHANGES, FAQ and NEWS files.

* Wed Jan 11 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.1.5-owl1
- Updated to 3.1 patchlevel 5.

* Thu Jan 05 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.1.1-owl1
- Updated to 3.1 patchlevel 1.
- Changed build to use readline version 5.1 bundled with bash until
system readline updated to this version.
- Enabled build option to use external files for help builtin
documentation.

* Thu Mar 31 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.0-owl0
- Updated to 3.0.
- Removed the _distribution and _patchlevel creation from spec,
these files are not used in the new version.
- Used a new notation for CWRU-fixes (before: -cwru-fixes, after: -pl<n>),
this allows to keep track what is the last patchlevel.
- Updated to the patchlevel 16.

* Sat Sep 11 2004 Solar Designer <solar-at-owl.openwall.com> 2.05-owl8
- Use RPM's exclude macro on info dir file.

* Tue Feb 24 2004 Michail Litvak <mci-at-owl.openwall.com> 2.05-owl7
- Statically link with system readline.

* Fri Feb 20 2004 Michail Litvak <mci-at-owl.openwall.com> 2.05-owl6
- Build with system readline.

* Tue Apr 15 2003 Solar Designer <solar-at-owl.openwall.com> 2.05-owl5
- Added /usr/local/sbin to the default PATH.

* Sun Jul 07 2002 Solar Designer <solar-at-owl.openwall.com> 2.05-owl4
- Use grep -q in this spec file.

* Sat May 25 2002 Solar Designer <solar-at-owl.openwall.com>
- Declare that the new mktemp is also required for bash _builds_.

* Thu Apr 25 2002 Solar Designer <solar-at-owl.openwall.com>
- Default to vitmp in fc (the history editor) and bashbug script.
- Provide sh.1 and bash2.1 symlinks to the man page.

* Thu Jan 24 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Sat Oct 27 2001 Solar Designer <solar-at-owl.openwall.com>
- Applied many cleanups to bash sources to build with -Wall also fixing a
few real bugs, disabling pieces of dead code, and commenting on likely
signal races (which remain).
- Updated the temporary file handling fixes to fit the new tmpfile.c
interfaces, reviewed and applied fixes to scripts used during bash builds
and to bashbug as well.
- The official bash patches are now in a separate file and applied first.
- Dropped some obsolete patches.

* Wed Oct 24 2001 Michail Litvak <mci-at-owl.openwall.com>
- 2.05
- Many patches from Debian, ALT Linux.
- some spec rework.
- removed -glibc-build-hack.diff which is no longer needed.
- #if 0'ed not used valid_exportstr function.

* Sat Jan 13 2001 Solar Designer <solar-at-owl.openwall.com>
- One more temporary file handling fix for the history editor, as reported
by Marcus Meissner of Caldera.
- Use $TMPDIR.

* Mon Dec 11 2000 Solar Designer <solar-at-owl.openwall.com>
- Some /tmp fixes (the old code was mostly safe, though).

* Sat Oct 28 2000 Solar Designer <solar-at-owl.openwall.com>
- Use %triggerin to create /etc/shells when libtermcap is installed, as
the commands require a working bash already.
- %postun -> %preun.
- "%triggerin -- libtermcap" and "%preun" script cleanups.

* Thu Sep 07 2000 Solar Designer <solar-at-owl.openwall.com>
- Workaround for glibc builds (allow '-' in identifiers in the exportstr
code, which is new for bash 2.04).

* Sun Sep 03 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import from rawhide.
- spec cleanup
- /etc/bashrc now in owl-etc
