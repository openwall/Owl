# $Id: Owl/packages/sparc32/Attic/sparc32.spec,v 1.1 2000/11/16 11:54:46 solar Exp $

Summary: A SPARC32 compilation environment.
Name: sparc32
Version: 1.1
Release: 2owl
Copyright: GPL
Group: System Environment/Kernel
Source: sparc32-1.1.tgz
ExclusiveOS: Linux
ExclusiveArch: sparc sparcv9 sparc64
Buildroot: /var/rpm-buildroot/%{name}-%{version}

%description
sparc32 is a simple utility for compiling SPARC32 packages on SPARC64
machines.  sparc32 creates an environment for the specified program
(shell) and all child processes.  In the created environment, uname -m
returns sparc, so one can create 32-bit SPARC programs.

Install sparc32 if you need to compile SPARC32 packages on a SPARC64.

%prep
%setup -q

%build
gcc -c $RPM_OPT_FLAGS sparc32.c -s -o sparc32

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/{bin,man/man8}
make install PREFIX=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
/usr/bin/*
/usr/man/man8/*

%changelog
* Thu Nov 16 2000 Solar Designer <solar@owl.openwall.com>
- Imported from RH.

* Tue Feb 22 2000 Bill Nottingham <notting@redhat.com>
- rebuild to catch compressed manpages

* Fri Sep 24 1999 Jakub Jelinek <jakub@redhat.com>
- add sparc64 command

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Thu Nov  5 1998 Jeff Johnson <jbj@redhat.com>
- import from ultrapenguin 1.1.

* Thu Oct 29 1998 Jakub Jelinek <jj@ultra.linux.cz>
- new package
