# $Id: Owl/packages/bash/bash.spec,v 1.9 2001/10/24 13:06:03 mci Exp $

Version: 2.05
Name: bash
Summary: The GNU Bourne Again shell (bash) version %{version}.
Release: 1owl
Group: System Environment/Shells
License: GPL
Source0: ftp://ftp.gnu.org/gnu/bash/bash-%{version}.tar.gz
Source1: ftp://ftp.gnu.org/gnu/bash/bash-doc-%{version}.tar.gz
Source2: dot-bashrc
Source3: dot-bash_profile
Source4: dot-bash_logout
Patch0: bash-2.03-rh-paths.diff
Patch1: bash-2.04-rh-bash1_compat.diff
Patch2: bash-2.04-rh-shellfunc.diff
Patch3: bash-2.05-rh-profile.diff
Patch4: bash-2.05-rh-requires.diff
Patch5: bash-2.05-rh-security.diff
Patch6: bash-2.05-alt-bashbug.diff
Patch7: bash-2.05-alt-man.diff
Patch8: bash-2.05-alt-nostrcoll.diff
Patch9: bash-2.05-deb-64bit.diff
Patch10: bash-2.05-deb-gnusource.diff
Patch11: bash-2.05-deb-misc.diff
Patch12: bash-2.05-deb-printcmd.diff
Patch13: bash-2.05-deb-privmode.diff
Patch14: bash-2.05-deb-random.diff
Patch15: bash-2.05-deb-vxman.diff
Patch16: bash-2.05-owl-glibc-build-hack.diff
Patch17: bash-2.05-owl-tmp.diff
Prefix: %{_prefix}
Requires: mktemp
Provides: bash2
Obsoletes: bash2 etcskel
BuildRoot: /override/%{name}-%{version}

%description
The GNU Bourne Again shell (Bash) is a shell or command language
interpreter that is compatible with the Bourne shell (sh).  Bash
incorporates useful features from the Korn shell (ksh) and the C shell
(csh).  Most sh scripts can be run by bash without modification.  This
package (bash) contains bash version %{version}, which improves POSIX
compliance over previous versions.

Documentation for bash version %{version} is contained in the bash-doc 
package.

%package doc
Group: Documentation
Summary: Documentation for the GNU Bourne Again shell (bash) version %{version}.
Obsoletes: bash2-doc

%description doc
The bash-doc package contains documentation for the GNU Bourne
Again shell version %{version}.

%prep
%setup -q -a 1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1

echo %{version} > _distribution
echo %{release} | sed -e "s/[A-Za-z]//g" > _patchlevel

%build
autoconf
%configure \
        --enable-alias \
        --enable-help-builtin \
        --enable-history \
        --enable-job-control \
        --enable-restricted \
        --enable-readline \
        --enable-extended-glob \
        --enable-dparen-arithmetic \
        --with-installed-readline
make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

mkdir -p $RPM_BUILD_ROOT/bin
mv $RPM_BUILD_ROOT%_bindir/%name $RPM_BUILD_ROOT/bin/%name
ln -s %name $RPM_BUILD_ROOT/bin/sh
ln -s %name $RPM_BUILD_ROOT/bin/bash2

gzip -9nf doc/*.ps

# make manpages for bash builtins as per suggestion in DOC/README
pushd doc
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

for i in `cat man.pages` ; do
  echo .so man1/builtins.1 > ${RPM_BUILD_ROOT}%{_mandir}/man1/$i.1
done

popd

# Those conflicts with real manpages
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/{echo,export,pwd,test,kill}.1

mkdir -p $RPM_BUILD_ROOT/etc/skel
install -c -m 644 %{SOURCE2} $RPM_BUILD_ROOT/etc/skel/.bashrc
install -c -m 644 %{SOURCE3} $RPM_BUILD_ROOT/etc/skel/.bash_profile
install -c -m 644 %{SOURCE4} $RPM_BUILD_ROOT/etc/skel/.bash_logout

%clean
rm -rf $RPM_BUILD_ROOT

# ***** bash doesn't use install-info. It's always listed in %{_infodir}/dir
# to prevent prereq loops

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

find examples -type f -print0 | xargs -r0 chmod -x

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
%doc doc/*.ps* doc/*.0 doc/*.html doc/article.txt

%changelog
* Tue Oct 23 2001 Michail Litvak <mci@owl.openwall.com>
- 2.05
- Many patches from Debian, ALT Linux
- some spec rework

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
