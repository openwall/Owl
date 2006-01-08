# $Owl: Owl/packages/bash/bash.spec,v 1.32 2006/01/08 22:42:08 ldv Exp $

Summary: The GNU Bourne-Again SHell (Bash).
Name: bash
%define bash_version 3.1
%define bash_patchlevel 1
Version: %bash_version.%bash_patchlevel
Release: owl1
Group: System Environment/Shells
License: GPL
Source0: ftp://ftp.gnu.org/gnu/bash/bash-%bash_version.tar.gz
Source1: ftp://ftp.gnu.org/gnu/bash/bash-doc-%bash_version.tar.gz
Source2: dot-bashrc
Source3: dot-bash_profile
Source4: dot-bash_logout
Patch0: bash-3.1-up-pl1.diff
Patch10: bash-3.1-owl-warnings.diff
Patch11: bash-3.1-owl-tmp.diff
Patch12: bash-3.1-owl-vitmp.diff
Patch13: bash-3.1-owl-defaults.diff
Patch14: bash-3.1-alt-man.diff
Patch20: bash-3.1-rh-ulimit.diff
Patch21: bash-3.1-rh-setlocale.diff
Patch22: bash-3.1-rh-read-memleak.diff
Patch23: bash-3.1-rh-alt-requires.diff
Patch24: bash-3.1-rh-man.diff
Patch30: bash-3.1-deb-random.diff
Patch31: bash-3.1-deb-doc.diff
Patch100: readline-5.1-up-pl1.diff
Patch101: readline-5.1-alt-warnings.diff
Patch102: readline-5.1-alt-nls.diff
Patch103: readline-5.1-deb-alt-inputrc.diff
Patch104: readline-5.1-rh-wrap.diff
Requires: mktemp >= 1:1.3.1
Provides: bash2
Obsoletes: bash2, etcskel
Prefix: %_prefix
BuildRequires: mktemp >= 1:1.3.1, readline-devel >= 0:4.3, rpm-build >= 0:4
BuildRoot: /override/%name-%version

%description
The GNU Bourne Again shell (Bash) is a shell or command language
interpreter that is compatible with the Bourne shell (sh).  Bash
incorporates useful features from the Korn shell (ksh) and the C shell
(csh).  Most sh scripts can be run by bash without modification.

Documentation for bash is contained in the bash-doc package.

%package doc
Group: Documentation
Summary: Documentation for the GNU Bourne Again shell (bash).
Obsoletes: bash2-doc

%description doc
The bash-doc package contains documentation for the GNU Bourne
Again shell version %version.

%prep
%setup -q -a1 -n bash-%bash_version
%patch0 -p0
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch30 -p1
%patch31 -p1
pushd lib/readline
%patch100 -p0
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
popd

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

%install
rm -rf %buildroot

%makeinstall

mkdir -p %buildroot/bin
mv %buildroot%_bindir/bash %buildroot/bin/
ln -s bash %buildroot/bin/sh
ln -s bash %buildroot/bin/bash2

ln -s bash.1 %buildroot%_mandir/man1/sh.1
ln -s bash.1 %buildroot%_mandir/man1/bash2.1

cd doc
gzip -9nf *.{ps,txt}

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
install -m 644 %_sourcedir/dot-bashrc etc/skel/.bashrc
install -m 644 %_sourcedir/dot-bash_profile etc/skel/.bash_profile
install -m 644 %_sourcedir/dot-bash_logout etc/skel/.bash_logout

# Remove unpackaged files if any
rm -f %buildroot%_infodir/dir

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
%config(noreplace) /etc/skel/.b*
%doc AUTHORS CHANGES COMPAT NEWS NOTES POSIX
%doc doc/FAQ doc/INTRO doc/article.ms
%doc examples/bashdb/ examples/functions/ examples/misc/
%doc examples/scripts.noah/ examples/scripts.v2/ examples/scripts/
%doc examples/startup-files/
/bin/sh
/bin/bash
/bin/bash2
%_datadir/bash
%_infodir/bash.info*
%_mandir/man1/*.1*
%_mandir/man1/..1*
%_bindir/bashbug
%_datadir/locale/en@*/LC_MESSAGES/bash.mo

%files doc
%defattr(-,root,root)
%doc doc/*.ps* doc/*.html doc/article.txt*

%changelog
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
