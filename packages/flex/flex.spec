# $Id: Owl/packages/flex/flex.spec,v 1.5 2002/07/07 21:11:41 mci Exp $

Summary: A tool for creating scanners (text pattern recognizers).
Name: flex
Version: 2.5.4a
Release: owl12
License: GPL
Group: Development/Tools
Source: ftp://ftp.gnu.org/non-gnu/flex/flex-%{version}.tar.gz
Patch0: flex-2.5.4a-rh-skel.diff
PreReq: /sbin/install-info
Prefix: %{_prefix}
BuildRoot: /override/%{name}-%{version}

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
rm -rf $RPM_BUILD_ROOT

%makeinstall mandir=$RPM_BUILD_ROOT/%{_mandir}/man1

pushd $RPM_BUILD_ROOT
ln -sf flex .%{_prefix}/bin/lex
ln -s flex.1 .%{_mandir}/man1/lex.1
ln -s flex.1 .%{_mandir}/man1/flex++.1
ln -s libfl.a .%{_prefix}/lib/libl.a
popd

mkdir $RPM_BUILD_ROOT/%{_infodir}
install -m 644 MISC/texinfo/flex.info $RPM_BUILD_ROOT/%{_infodir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/flex.info.gz %{_infodir}/dir \
	--entry="* Flex: (flex).            A fast scanner generator."
%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/flex.info.gz %{_infodir}/dir \
	--entry="* Flex: (flex).            A fast scanner generator."
fi

%files
%defattr(-,root,root)
%doc COPYING NEWS README
%{_prefix}/bin/lex
%{_prefix}/bin/flex
%{_prefix}/bin/flex++
%{_mandir}/man1/*
%{_infodir}/flex.*
%{_prefix}/lib/libl.a
%{_prefix}/lib/libfl.a
%{_prefix}/include/FlexLexer.h

%changelog
* Sun Jul 07 2002 Michail Litvak <mci@owl.openwall.com>
- Package flex.info

* Fri Feb 01 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
