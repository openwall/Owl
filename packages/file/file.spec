# $Id: Owl/packages/file/file.spec,v 1.5 2003/03/06 23:29:45 mci Exp $

Summary: A utility for determining file types.
Name: file
Version: 3.41
Release: owl1
License: distributable
Group: Applications/File
URL: http://www.darwinsys.com/freeware/file.html
Source0: ftp://ftp.astron.com/pub/file/file-%{version}.tar.gz
Patch0: file-3.41-rh-ia64.diff
Patch1: file-3.41-mdk-alt-zsh.patch
Patch2: file-3.41-alt-doctype.patch
Patch3: file-3.41-alt-mng.patch
Patch4: file-3.41-deb-compress.diff
Patch5: file-3.41-deb-magic2mime.diff
Patch6: file-3.41-deb-make.diff
Patch7: file-3.41-deb-magic.diff
Patch8: file-3.41-deb-owl-man.diff
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
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
automake
%configure --enable-fsect-man5
make LDFLAGS=-s

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man{1,5}
mkdir -p $RPM_BUILD_ROOT%{_datadir}

%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/magic*
%{_mandir}/man*/*

%changelog
* Fri Mar 07 2002 Michail Litvak <mci@owl.openwall.com>
- 3.41
- Patch updates

* Thu Jan 31 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions.

* Thu Nov 29 2000 Michail Litvak <mci@owl.openwall.com>
- Imported from RH and updated to 3.33
- added some patches from Debian and RH
