# $Id: Owl/packages/bash/bash.spec,v 1.12 2001/10/27 17:30:57 solar Exp $

Version: 2.05
Name: bash
Summary: The GNU Bourne-Again SHell (Bash).
Release: 1owl
Group: System Environment/Shells
License: GPL
Source0: ftp://ftp.gnu.org/gnu/bash/bash-%{version}.tar.gz
Source1: ftp://ftp.gnu.org/gnu/bash/bash-doc-%{version}.tar.gz
Source2: dot-bashrc
Source3: dot-bash_profile
Source4: dot-bash_logout
Patch0: bash-2.05-cwru-fixes.diff
Patch10: bash-2.05-owl-fixes.diff
Patch11: bash-2.05-owl-tmp.diff
Patch12: bash-2.05-owl-paths.diff
Patch20: bash-2.04-rh-bash1_compat.diff
Patch21: bash-2.04-rh-shellfunc.diff
Patch22: bash-2.05-rh-requires.diff
Patch23: bash-2.05-rh-profile.diff
Patch24: bash-2.05-rh-readline.diff
Patch30: bash-2.05-deb-64bit.diff
Patch31: bash-2.05-deb-gnusource.diff
Patch32: bash-2.05-deb-print_cmd.diff
Patch33: bash-2.05-deb-random.diff
Patch34: bash-2.05-deb-man.diff
Patch40: bash-2.05-alt-fnmatch-disable-strcoll.diff
Patch41: bash-2.05-alt-man.diff
Prefix: %{_prefix}
Requires: mktemp >= 1:1.3.1
Provides: bash2
Obsoletes: bash2 etcskel
Buildroot: /override/%{name}-%{version}

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
Again shell version %{version}.

%prep
%setup -q -a 1
%patch0 -p0
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch40 -p1
%patch41 -p1

echo %{version} > _distribution
echo %{release} | sed -e "s/[A-Za-z]//g" > _patchlevel

# Would anyone volunteer to fix those? Probably not.
find examples -type f -print0 | xargs -r0 grep -lZ /tmp | xargs -r0 rm -f --

# Prevent bogus dependencies
find examples -type f -print0 | xargs -r0 chmod -x --

%{expand:%%define optflags %optflags -Wall}

%build
rm -f configure doc/bashref.info
autoconf
export \
	bash_cv_dev_fd=standard \
	bash_cv_dev_stdin=present \
	bash_cv_mail_dir=/var/mail \
%configure \
	--without-curses \
	--without-installed-readline \
	--disable-restricted \
	--disable-net-redirections
make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

mkdir -p $RPM_BUILD_ROOT/bin
mv $RPM_BUILD_ROOT%_bindir/%name $RPM_BUILD_ROOT/bin/%name
ln -s %name $RPM_BUILD_ROOT/bin/sh
ln -s %name $RPM_BUILD_ROOT/bin/bash2

gzip -9nf doc/*.{ps,txt}

pushd doc

# Make manpages for bash builtins as per suggestion in doc/README
sed -e '
/^\.SH NAME/, /\\- bash built-in commands, see \\fBbash\\fR(1)$/{
/^\.SH NAME/d
s/^bash, //
s/\\- bash built-in commands, see \\fBbash\\fR(1)$//
s/,//g
b
}
d
' builtins.1 > man.pages

install -c -m 644 builtins.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/builtins.1

for c in `cat man.pages`; do
	echo .so man1/builtins.1 > ${RPM_BUILD_ROOT}%{_mandir}/man1/$c.1
done

popd

# These conflict with real manpages
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/{echo,pwd,test,kill}.1

mkdir -p $RPM_BUILD_ROOT/etc/skel
install -c -m 644 %{SOURCE2} $RPM_BUILD_ROOT/etc/skel/.bashrc
install -c -m 644 %{SOURCE3} $RPM_BUILD_ROOT/etc/skel/.bash_profile
install -c -m 644 %{SOURCE4} $RPM_BUILD_ROOT/etc/skel/.bash_logout

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- libtermcap
if [ ! -f /etc/shells ]; then
	echo "/bin/sh" >> /etc/shells
	echo "/bin/bash" >> /etc/shells
	echo "/bin/bash2" >> /etc/shells
elif [ -x /bin/grep ]; then
	grep '^/bin/sh$' /etc/shells &> /dev/null || \
		echo "/bin/sh" >> /etc/shells
	grep '^/bin/bash$' /etc/shells &> /dev/null || \
		echo "/bin/bash" >> /etc/shells
	grep '^/bin/bash2$' /etc/shells &> /dev/null || \
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
%doc CHANGES COMPAT NEWS NOTES CWRU/POSIX.NOTES
%doc doc/FAQ doc/INTRO doc/article.ms
%doc examples/bashdb/ examples/functions/ examples/misc/
%doc examples/scripts.noah/ examples/scripts.v2/ examples/scripts/
%doc examples/startup-files/
/bin/sh
/bin/bash
/bin/bash2
%{_infodir}/bash.info*
%{_mandir}/man1/*
%{_prefix}/bin/bashbug

%files doc
%defattr(-,root,root)
%doc doc/*.ps* doc/*.html doc/article.txt*

%changelog
* Sat Oct 27 2001 Solar Designer <solar@owl.openwall.com>
- Applied many cleanups to bash sources to build with -Wall also fixing a
few real bugs, disabling pieces of dead code, and commenting on likely
signal races (which remain).
- Updated the temporary file handling fixes to fit the new tmpfile.c
interfaces, reviewed and applied fixes to scripts used during bash builds
and to bashbug as well.
- The official bash patches are now in a separate file and applied first.
- Dropped some obsolete patches.

* Wed Oct 24 2001 Michail Litvak <mci@owl.openwall.com>
- 2.05
- Many patches from Debian, ALT Linux.
- some spec rework.
- removed -glibc-build-hack.diff which is no longer needed.
- #if 0'ed not used valid_exportstr function.

* Sat Jan 13 2001 Solar Designer <solar@owl.openwall.com>
- One more temporary file handling fix for the history editor, as reported
by Marcus Meissner of Caldera.
- Use $TMPDIR.

* Mon Dec 11 2000 Solar Designer <solar@owl.openwall.com>
- Some /tmp fixes (the old code was mostly safe, though).

* Sat Oct 28 2000 Solar Designer <solar@owl.openwall.com>
- Use %triggerin to create /etc/shells when libtermcap is installed, as
the commands require a working bash already.
- %postun -> %preun.
- "%triggerin -- libtermcap" and "%preun" script cleanups.

* Thu Sep 07 2000 Solar Designer <solar@owl.openwall.com>
- Workaround for glibc builds (allow '-' in identifiers in the exportstr
code, which is new for bash 2.04).

* Sun Sep 03 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from rawhide.
- spec cleanup
- /etc/bashrc now in owl-etc
