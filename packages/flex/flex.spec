# $Owl: Owl/packages/flex/flex.spec,v 1.18 2010/10/15 01:02:47 solar Exp $

Summary: A tool for creating scanners (text pattern recognizers).
Name: flex
Version: 2.5.35
Release: owl1
License: GPL
Group: Development/Tools
URL: http://flex.sourceforge.net
Source: flex-%version.tar.xz
Patch0: flex-2.5.4a-rh-skel.diff
Patch1: flex-2.5.35-alt-YY_STATE_BUF_SIZE.diff
Patch2: flex-2.5.35-suse-pic.diff
Patch3: flex-2.5.35-alt-info.diff
PreReq: /sbin/install-info
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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
autoconf
%configure
%__make

%check
%__make check

%install
rm -rf %buildroot

%makeinstall

pushd %buildroot
ln -sf flex .%_bindir/lex
ln -sf flex .%_bindir/flex++
ln -s libfl.a .%_libdir/libl.a
ln -s libfl.a .%_libdir/libfl_pic.a
ln -s flex.1 .%_mandir/man1/lex.1
ln -s flex.1 .%_mandir/man1/flex++.1
popd

#mkdir %buildroot%_infodir
#install -m 644 MISC/texinfo/flex.info %buildroot%_infodir/

%find_lang %name

%post
/sbin/install-info %_infodir/flex.info %_infodir/dir \
	--entry="* Flex: (flex).                                 A fast scanner generator."
%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/flex.info %_infodir/dir \
		--entry="* Flex: (flex).                                 A fast scanner generator."
fi

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README THANKS
# XXX: Consider packaging doc/flex.pdf and examples/ (in some form).
%_bindir/lex
%_bindir/flex
%_bindir/flex++
%_mandir/man1/*
%_infodir/flex.*
%_libdir/libl.a
%_libdir/libfl.a
%_libdir/libfl_pic.a
%_prefix/include/FlexLexer.h
%exclude %_infodir/dir

%changelog
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
