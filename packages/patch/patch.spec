# $Id: Owl/packages/patch/patch.spec,v 1.3 2002/02/06 22:41:22 mci Exp $

Summary: The GNU patch command, for modifying/upgrading files.
Name: patch
Version: 2.5.4
Release: owl6
License: GPL
Group: Development/Tools
Source: ftp://ftp.gnu.org/gnu/patch/patch-%{version}.tar.gz
Patch0: patch-2.5.4-mdk-sigsegv.diff
Patch1: patch-2.5.4-rh-stderr.diff
Patch2: patch-2.5.4-owl-backup.diff
Prefix: %{_prefix}
BuildRoot: /override/%{name}-%{version}

%description
The patch program applies diff files to originals.  The diff command
is used to compare an original to a changed file.  Diff lists the
changes made to the file.  A person who has the original file can then
use the patch command with the diff file to add the changes to their
original file (patching the file).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
# (fg) Large file support can be disabled from ./configure - it is necessary at
# least on sparcs
%ifnarch sparc sparcv9 sparc64 alpha
%configure
%else
%configure --disable-largefile
%endif

make "CFLAGS=$RPM_OPT_FLAGS -D_GNU_SOURCE -W -Wall" LDFLAGS=-s

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc NEWS README AUTHORS ChangeLog
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Thu Feb 07 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions.

* Wed Dec 20 2000 Michail Litvak <mci@owl.openwall.com>
- added patch to fix default backup extension

* Tue Nov 17 2000 Michail Litvak <mci@owl.openwall.com>
- import from RH and Mandrake 
- sigsegv patch from MDK, stderr from RH
