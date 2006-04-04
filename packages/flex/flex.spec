# $Owl: Owl/packages/flex/flex.spec,v 1.14 2006/04/04 00:28:34 ldv Exp $

Summary: A tool for creating scanners (text pattern recognizers).
Name: flex
Version: 2.5.4a
Release: owl14
License: GPL
Group: Development/Tools
Source: ftp://ftp.gnu.org/non-gnu/flex/flex-%version.tar.gz
Patch0: flex-2.5.4a-rh-skel.diff
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
%setup -q -n flex-2.5.4
%patch0 -p1

%build
autoconf
%configure
make

%install
rm -rf %buildroot

%makeinstall mandir=%buildroot%_mandir/man1

pushd %buildroot
ln -sf flex .%_bindir/lex
ln -s flex.1 .%_mandir/man1/lex.1
ln -s flex.1 .%_mandir/man1/flex++.1
ln -s libfl.a .%_libdir/libl.a
popd

mkdir %buildroot%_infodir
install -m 644 MISC/texinfo/flex.info %buildroot%_infodir/

%post
/sbin/install-info %_infodir/flex.info %_infodir/dir \
	--entry="* Flex: (flex).                                 A fast scanner generator."
%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/flex.info %_infodir/dir \
		--entry="* Flex: (flex).                                 A fast scanner generator."
fi

%files
%defattr(-,root,root)
%doc COPYING NEWS README
%_bindir/lex
%_bindir/flex
%_bindir/flex++
%_mandir/man1/*
%_infodir/flex.*
%_libdir/libl.a
%_libdir/libfl.a
%_prefix/include/FlexLexer.h

%changelog
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
