# $Id: Owl/packages/bash/bash.spec,v 1.1 2000/09/03 19:56:34 kad Exp $

Version: 	2.04
Name: 		bash
Summary: 	The GNU Bourne Again shell (bash) version %{version}.
Release: 	8owl
Group: 		System Environment/Shells
Copyright: 	GPL
Source0:	ftp://ftp.gnu.org/gnu/bash/bash-%{version}.tar.gz
Source1: 	ftp://ftp.gnu.org/gnu/bash/bash-doc-%{version}.tar.gz
Source2: 	dot-bashrc
Source3: 	dot-bash_profile
Source4: 	dot-bash_logout
Patch0: 	bash-2.03-rh-paths.diff
Patch1: 	bash-2.02-rh-security.diff
Patch2: 	bash-2.03-rh-profile.diff
Patch3: 	bash-2.04-rh-requires.diff
Patch4: 	bash-2.04-rh-bash1_compat.diff
Patch5: 	bash-2.04-rh-shellfunc.diff
Prefix: 	%{_prefix}
Requires: 	mktemp
Provides: 	bash2
Obsoletes:	bash2 etcskel
BuildRoot: 	/var/rpmbuild-root/%{name}-root

%description
The GNU Bourne Again shell (Bash) is a shell or command language
interpreter that is compatible with the Bourne shell (sh). Bash
incorporates useful features from the Korn shell (ksh) and the C shell
(csh). Most sh scripts can be run by bash without modification. This
package (bash) contains bash version %{version}, which improves POSIX
compliance over previous versions. However, many old shell scripts
will depend upon the behavior of bash 1.14, which is included in the
bash1 package. Bash is the default shell for Red Hat Linux.  It is
popular and powerful, and you'll probably end up using it.

Documentation for bash version %{version} is contained in the bash-doc 
package.

%package doc
Group: Documentation
Summary: Documentation for the GNU Bourne Again shell (bash) version 2.03.
Obsoletes: bash2-doc

%description doc
The bash-doc package contains documentation for the GNU Bourne
Again shell version %{version}.

%prep
%setup -q -a 1
%patch0 -p1 -b .paths
%patch1 -p1 -b .security
%patch2 -p1 -b .profile
%patch3 -p1 -b .requires
%patch4 -p1 -b .compat
%patch5 -p1 -b .shellfunc
echo %{version} > _distribution
echo %{release} | sed -e "s/[A-Za-z]//g" > _patchlevel

%build

%configure
make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

# Take out irritating ^H's from the documentation
chmod u+w doc/*
for i in `ls --color=no doc/` ; \
	do cat doc/$i > $i ; \
	cat $i | perl -p -e 's/.//g' > doc/$i ; \
	rm $i ; \
	done

# make manpages for bash builtins as per suggestion in DOC/README
cd doc
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
for i in echo pwd test kill; do
  perl -pi -e "s,$i,,g" man.pages
  perl -pi -e "s,  , ,g" man.pages
done

install -c -m 644 builtins.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/builtins.1

for i in `cat man.pages` ; do
  echo .so man1/builtins.1 > ${RPM_BUILD_ROOT}%{_mandir}/man1/$i.1
done

# now turn man.pages into a filelist for the man subpackage
cat man.pages | tr -s ' ' '\n' | sed '
1i\
%defattr(0644,root,root,0755)
s:^:%{_mandir}/man1/:
s/$/.1*/
' > ../man.pages

{ cd $RPM_BUILD_ROOT
  mkdir ./bin
  mv ./usr/bin/bash ./bin
  ln -sf bash ./bin/bash2
  ln -sf bash ./bin/sh
  strip ./bin/* || :
  gzip -9nf .%{_infodir}/bash.info
  rm -f .%{_infodir}/dir
}
mkdir -p $RPM_BUILD_ROOT/etc/skel
install -c -m644 %{SOURCE2} $RPM_BUILD_ROOT/etc/skel/.bashrc
install -c -m644 %{SOURCE3} \
	$RPM_BUILD_ROOT/etc/skel/.bash_profile
install -c -m644 %{SOURCE4} \
	$RPM_BUILD_ROOT/etc/skel/.bash_logout


%clean
rm -rf $RPM_BUILD_ROOT

# ***** bash doesn't use install-info. It's always listed in %{_infodir}/dir
# to prevent prereq loops

%post

HASBASH2=""
HASBASH=""
HASSH=""

if [ ! -f /etc/shells ]; then
	> /etc/shells
fi

(while read line ; do
	if [ $line = /bin/bash ]; then
		HASBASH=1
	elif [ $line = /bin/sh ]; then
		HASSH=1
	elif [ $line = /bin/bash2 ]; then
		HASBASH2=1
	fi
 done

 if [ -z "$HASBASH2" ]; then
	echo "/bin/bash2" >> /etc/shells
 fi
 if [ -z "$HASBASH" ]; then
	echo "/bin/bash" >> /etc/shells
 fi
 if [ -z "$HASSH" ]; then
	echo "/bin/sh" >> /etc/shells
fi) < /etc/shells


%postun
if [ "$1" = 0 ]; then
	# is "rm -f /etc/shells" better?
	grep -v '^/bin/bash2$' < /etc/shells | \
		grep -v '^/bin/bash$' | \
		grep -v '^/bin/sh$' > /etc/shells.new
	mv /etc/shells.new /etc/shells
fi

%files -f man.pages
%defattr(-,root,root)
%doc CHANGES COMPAT NEWS NOTES CWRU/POSIX.NOTES
%doc doc/FAQ doc/INTRO doc/article.ms
%doc examples/bashdb/ examples/functions/ examples/misc/
%doc examples/scripts.noah/ examples/scripts.v2/ examples/scripts/
%doc examples/startup-files/
#%config /etc/bashrc
%config /etc/skel
/bin/sh
/bin/bash
/bin/bash2
%{_infodir}/bash.info.gz
%{_mandir}/man1/bash.1*
%{_mandir}/man1/builtins.1*
%{_prefix}/bin/bashbug
%{_mandir}/man1/bashbug.1*

%files doc
%defattr(-,root,root)
%doc doc/*.ps doc/*.0 doc/*.html doc/article.txt

%changelog
* Sun Sep  3 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from rawhide.
- spec cleanup
- /etc/bashrc now in owl-etc

