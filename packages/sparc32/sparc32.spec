# $Id: Owl/packages/sparc32/Attic/sparc32.spec,v 1.3 2002/02/05 16:28:29 solar Exp $

Summary: A SPARC32 compilation environment.
Name: sparc32
Version: 1.1
Release: owl2
License: GPL
Group: System Environment/Kernel
Source: sparc32-1.1.tgz
ExclusiveArch: sparc sparcv9 sparc64
BuildRoot: /override/%{name}-%{version}

%description
sparc32 is a simple utility for compiling SPARC32 packages on SPARC64
machines.  sparc32 creates an environment for the specified program
(shell) and all child processes.  In the created environment, uname -m
returns sparc, so one can create 32-bit SPARC programs.

%prep
%setup -q

%build
gcc $RPM_OPT_FLAGS sparc32.c -s -o sparc32

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
* Tue Feb 05 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Thu Nov 16 2000 Solar Designer <solar@owl.openwall.com>
- Imported from RH.
