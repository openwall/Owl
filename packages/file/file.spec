# $Id: Owl/packages/file/file.spec,v 1.2 2002/01/31 23:07:00 mci Exp $

Summary: A utility for determining file types.
Name: file
Version: 3.33
Release: owl1
License: distributable
Group: Applications/File
Source0: ftp://ftp.astron.com/pub/file/file-%{version}.tar.gz
Patch0: file-3.33-rh-fnovfl.diff
Patch1: file-3.33-rh-ia64.diff
Patch2: file-3.33-deb-magic.diff
Patch3: file-3.33-deb-magi2mime.diff
Patch4: file-3.33-deb-make.diff
Prefix: %{_prefix}
BuildRoot: /override/%{name}-%{version}

%description
The file command is used to identify a particular file according to the
type of data contained by the file.  file can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build

automake
%configure
make LDFLAGS=-s

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man5
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}

%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/magic*
%{_mandir}/man*/*

%changelog
* Thu Jan 31 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions.

* Thu Nov 29 2000 Michail Litvak <mci@owl.openwall.com>
- Imported from RH and updated to 3.33
- added some patches from Debian and RH
