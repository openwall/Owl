Summary: A small utility for safely making /tmp files.
Name: mktemp
%define version 1.5
Version: %{version}
Release: 3owl
Copyright: BSD
Group: System Environment/Base
Source: ftp://ftp.openbsd.org/pub/OpenBSD/src/usr.bin/mktemp-%{version}.tar.gz
Patch0: mktemp-1.5-rh-owl-linux.diff
Url: http://www.openbsd.org
Buildroot: /var/rpm-buildroot/%{name}-%{version}

%description
The mktemp utility takes a given file name template and overwrites a
portion of it to create a unique file name.  This allows shell scripts
and other programs to safely create and use /tmp files.

Install the mktemp package if you need to use shell scripts or other
programs which will create and use unique /tmp files.

%prep
%setup
%patch -p1

%build
make CFLAGS="-c $RPM_OPT_FLAGS"

%install
mkdir -p $RPM_BUILD_ROOT/bin $RPM_BUILD_ROOT/usr/man/man1
make FAKEROOT="$RPM_BUILD_ROOT" install
gzip -9 $RPM_BUILD_ROOT/usr/man/man1/mktemp.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
/bin/mktemp
/usr/man/man1/mktemp.*

%changelog
* Fri Jul  7 2000 Solar Designer <solar@false.com>
- import from RH, and fix for arbitrary buildroot

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Mon Mar 22 1999 Erik Troan <ewt@redhat.com>
- sync'd man page with openbsd latest, and updated it for some Linux-specific
  changes

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Tue Dec 29 1998 Cristian Gafton <gafton@redhat.com>
- build for 6.0

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Oct 01 1997 Erik Troan <ewt@redhat.com>
- moved to /bin

