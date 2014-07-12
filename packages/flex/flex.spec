# $Owl: Owl/packages/flex/flex.spec,v 1.20 2014/07/12 13:50:09 galaxy Exp $

Summary: A tool for creating scanners (text pattern recognizers).
Name: flex
Version: 2.5.39
Release: owl1
License: GPL
Group: Development/Tools
URL: http://flex.sourceforge.net
Source: http://downloads.sourceforge.net/%name/%name-%version.tar.xz
Patch0: %name-2.5.37-fc-updated-bison-construct.diff
# re-generation of docs requires textinfo, tex, help2man
Patch1: %name-2.5.39-owl-skip-docs-build.diff
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
BuildRequires: bison >= 2.6.1
BuildRequires: gettext, libtool, autoconf >= 2.69, automake, m4
Prefix: %_prefix
BuildRoot: /override/%name-%version

%description
The flex program generates scanners.  Scanners are programs which can
recognize lexical patterns in text.  flex takes pairs of regular
expressions and C code as input and generates a C source file as
output.  The output file is compiled and linked with a library to
produce an executable.  The executable searches through its input for
occurrences of the regular expressions.  When a match is found, it
executes the corresponding C code.  flex was designed to work with
both Yacc and Bison, and is used by many programs as part of their
build process.

%prep
%setup -q
%patch0 -p1 -b .updated-bison-construct
%patch1 -p1 -b .skip-docs-build

gettextize -f -q --symlink
rm gettext.h
ln -s '%_datadir/gettext/gettext.h'
aclocal --force -I m4
autoreconf -fis

%build

%configure \
	--disable-rpath \
#

%__make

%check
%__make check

%install
[ '%buildroot' != '/' -a -d '%buildroot' ] && rm -rf -- '%buildroot'

%makeinstall

# since we removed the doc subdir from the build process, we need to
# install docs ourselves.
mkdir -p '%buildroot%_mandir/man1/'
install -p -m644 doc/flex.1 '%buildroot%_mandir/man1/'
mkdir -p '%buildroot%_infodir/'
install -p -m644 doc/flex.info* '%buildroot%_infodir/'

/sbin/ldconfig -v -n '%buildroot%_libdir'

pushd '%buildroot'
ln -sf flex '.%_bindir/lex'
ln -sf flex '.%_bindir/flex++'
ln -s flex.1 '.%_mandir/man1/lex.1'
ln -s flex.1 '.%_mandir/man1/flex++.1'
ln -s libfl.a '.%_libdir/libl.a'
popd

%find_lang %name || :
touch '%name.lang'

# remove unpackaged files
find '%buildroot' -type f -name '*.la' -delete
rm -r -- '%buildroot%_datadir/doc'

%post
/sbin/install-info '%_infodir/flex.info' '%_infodir/dir' \
	--entry="* Flex: (flex).					A fast scanner generator."
%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete '%_infodir/flex.info' '%_infodir/dir' \
		--entry="* Flex: (flex).					A fast scanner generator."
fi

%files -f %name.lang
%defattr(0644,root,root,0755)
%doc AUTHORS COPYING NEWS README THANKS
# XXX: Consider packaging doc/flex.pdf and examples/ (in some form).
%attr(0755,root,root) %_bindir/flex
# symlinks
%_bindir/lex
%_bindir/flex++
%_mandir/man1/flex.1*
%_mandir/man1/lex.1*
%_mandir/man1/flex++.1*
%_infodir/flex.info*
%_libdir/libfl.so.*
%_libdir/libfl_pic.so.*
%_libdir/libfl.so
%_libdir/libfl_pic.so
%_libdir/libl.a
%_libdir/libfl.a
%_libdir/libfl_pic.a
%_prefix/include/FlexLexer.h

%changelog
* Thu Jun 19 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 2.5.39-owl1
- Updated to 2.5.39.

* Tue Sep 13 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 2.5.35-owl2
- Fixed build bug with gcc 4.6.1.

* Mon Oct 11 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 2.5.35-owl1
- Updated to 2.5.35.
- Imported patches from ALT Linux and SuSE.
- Added documentation files.
- Introduced %find_lang.
- Introduced %check.

* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.5.4a-owl14
- Corrected info files installation.

* Mon Aug 19 2002 Michail Litvak <mci-at-owl.openwall.com> 2.5.4a-owl13
- Deal with info dir entries such that the menu looks pretty.

* Sun Jul 07 2002 Michail Litvak <mci-at-owl.openwall.com>
- Package flex.info

* Fri Feb 01 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import from RH
