# $Id: Owl/packages/fileutils/Attic/fileutils.spec,v 1.5 2002/01/31 23:27:45 mci Exp $

Summary: The GNU versions of common file management utilities.
Name: fileutils
Version: 4.0.27
Release: owl4
License: GPL
Group: Applications/File
Source0: ftp://alpha.gnu.org/gnu/fetish/%{name}-%{version}.tar.gz
Source1: DIR_COLORS
Source2: colorls.sh
Source3: colorls.csh
Source4: shred.1
Patch0: fileutils-4.0-rh-spacedir.diff
Patch1: fileutils-4.0-rh-samefile.diff
Patch2: fileutils-4.0-rh-C-option.diff
Patch3: fileutils-4.0p-rh-strip.diff
Patch4: fileutils-4.0x-rh-force-chmod.diff
Patch5: fileutils-4.0x-rh-overwrite.diff
Patch6: fileutils-4.0-rh-ls-dumbterm.diff
PreReq: /sbin/install-info
BuildRoot: /override/%{name}-%{version}

%description
The fileutils package includes a number of GNU versions of common and
popular file management utilities.  fileutils includes the following
tools: chgrp (changes a file's group ownership), chown (changes a
file's ownership), chmod (changes a file's permissions), cp (copies
files), dd (copies and converts files), df (shows a filesystem's disk
usage), dir (gives a brief directory listing), dircolors (the setup
program for the color version of the ls command), du (shows disk
usage), install (copies files and sets permissions), ln (creates file
links), ls (lists directory contents), mkdir (creates directories),
mkfifo (creates FIFOs or named pipes), mknod (creates special files),
mv (renames files), rm (removes/deletes files), rmdir (removes empty
directories), sync (synchronizes memory and disk), touch (changes file
timestamps), and vdir (provides long directory listings).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
unset LINGUAS || :
%ifos linux
%define _exec_prefix /
%endif
%configure

make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

cd $RPM_BUILD_ROOT

%ifos linux
mkdir -p .%{_prefix}/bin
for i in dir dircolors du install mkfifo shred vdir
do
	mv -f ./bin/$i .%{_prefix}/bin/$i
done
strip -R .comment ./bin/* || :
%endif

mkdir -p ./etc/profile.d
install -c -m 644 $RPM_SOURCE_DIR/DIR_COLORS ./etc
install -c -m 755 $RPM_SOURCE_DIR/colorls.sh ./etc/profile.d
install -c -m 755 $RPM_SOURCE_DIR/colorls.csh ./etc/profile.d

install -c -m 644 $RPM_SOURCE_DIR/shred.1 $RPM_BUILD_ROOT/%{_mandir}/man1/

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/fileutils.info.gz %{_infodir}/dir

%preun
if [ $1 = 0 ]; then
	/sbin/install-info --delete %{_infodir}/fileutils.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
%doc ABOUT-NLS AUTHORS COPYING ChangeLog NEWS README THANKS TODO
%config %{_sysconfdir}/DIR_COLORS
%config %{_sysconfdir}/profile.d/*

%ifos linux
%{_exec_prefix}/bin/*
%endif
%{_prefix}/bin/*
%{_mandir}/man*/*

%{_infodir}/fileutils*
%{_prefix}/share/locale/*/*/*

%changelog
* Fri Feb 01 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce oour new spec file conventions.
- Changed %SOURCE* to explicit $RPM_SOURCE_DIR/*

* Thu Nov 30 2000 Solar Designer <solar@owl.openwall.com>
- Avoid listing %{_sysconfdir}/profile.d (the directory itself).

* Wed Nov 29 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- add warning to shred(1) man.

* Thu Oct 19 2000 Solar Designer <solar@owl.openwall.com>
- Fixed a bug in RH patch to mv (don't exit if lstat on a file fails).

* Sun Oct  1 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- v4.0.27

* Sun Sep 24 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import spec from RH
