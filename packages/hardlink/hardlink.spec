# $Owl: Owl/packages/hardlink/hardlink.spec,v 1.4 2011/12/27 01:25:52 solar Exp $

Summary: Consolidate duplicate files via hardlinks.
Name: hardlink
Version: 1.0
Release: owl2
Epoch: 1
License: GPLv2+
Group: System Environment/Base
URL: http://pkgs.fedoraproject.org/gitweb/?p=hardlink.git
Source0: hardlink.c
Source1: hardlink.1
BuildRoot: /override/%name-%version

%description
This package contains hardlink, an utility which consolidates duplicate
files in one or more directories using hardlinks.

hardlink traverses one or more directories searching for duplicate files.
When it finds duplicate files, it uses one of them as the master.  It then
removes all other duplicates and places a hardlink for each one pointing
to the master file.  This allows for conservation of disk space where
multiple directories on a single filesystem contain many duplicate files.

Since hard links can only span a single filesystem, hardlink is only
useful when all directories specified are on the same filesystem.

%prep
%setup -q -c -T

%{expand:%%define optflags %optflags -Wall}

%build
%__cc %optflags %_sourcedir/hardlink.c -o hardlink

%install
rm -rf %buildroot
install -pDm755 hardlink %buildroot%_bindir/hardlink
install -pDm644 %_sourcedir/hardlink.1 %buildroot%_mandir/man1/hardlink.1

%files
%defattr(-,root,root)
%_bindir/hardlink
%_mandir/man1/hardlink.1*

%changelog
* Tue Dec 27 2011 Solar Designer <solar-at-owl.openwall.com> 1:1.0-owl2
- Removed an erroneous close(fd) call in a code path triggered on error and for
empty files (luckily, this did not actually matter in the latter case).

* Sat Oct 15 2011 Solar Designer <solar-at-owl.openwall.com> 1:1.0-owl1
- Initial packaging for Owl, based on a mix of Fedora's and ALT Linux's.
- Made changes to the program to avoid buffer and integer overflows with deeply
nested directories and/or with long directory or file names.
- Added section "BUGS" to the man page explaining that "hardlink" must not be
used on potentially changing directory trees.
