# $Owl: Owl/packages/help2man/help2man.spec,v 1.1 2015/01/03 23:11:09 solar Exp $

Summary: help2man creates simple man pages from the output of programs.
Name: help2man
Version: 1.46.4
Release: owl1
License: GPLv3+
Group: Development/Tools
URL: http://www.gnu.org/software/help2man/
Source: ftp://ftp.gnu.org/gnu/help2man/help2man-%version.tar.xz
BuildRoot: /override/%name-%version

%description
help2man is a tool for automatically generating simple manual pages from
program output.

This program is intended to provide an easy way for software authors to include
a manual page in their distribution without having to maintain that document.

Given a program which produces reasonably standard --help and --version
outputs, help2man can re-arrange that output into something which resembles a
manual page.

%prep
%setup -q
install -pm644 debian/README README.example

%{expand:%%define optflags %optflags -Wall}

%build
%configure
%__make

%install
rm -rf %buildroot
%__make install DESTDIR=%buildroot

%files
%defattr(-,root,root)
%doc ChangeLog NEWS README* THANKS
%_bindir/*
%_mandir/man1/*
%_infodir/*.info*

%changelog
* Sun Jan 04 2015 Solar Designer <solar-at-owl.openwall.com> 1.46.4-owl1
- Packaged for Owl, loosely based on spec file from ALT Linux.
