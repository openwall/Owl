# $Id: Owl/packages/cpio/cpio.spec,v 1.9 2002/08/26 15:23:17 mci Exp $

Summary: A GNU archiving program.
Name: cpio
Version: 2.4.2
Release: owl26
License: GPL
Group: Applications/Archiving
Source: ftp://ftp.gnu.org/gnu/cpio-%{version}.tar.gz
Patch0: cpio-2.4.2-deb-cpio.diff
Patch1: cpio-2.4.2-deb-mt_scsi.diff
Patch2: cpio-2.4.2-deb-rmt.diff
Patch3: cpio-2.4.2-deb-glibc21.diff
Patch4: cpio-2.4.2-deb-cpio_man.diff
Patch5: cpio-2.4.2-deb-mt_man.diff
Patch6: cpio-2.4.2-deb-rmt_man.diff
Patch7: cpio-2.4.2-deb-owl-info.diff
Patch8: cpio-2.4.2-rh-fhs.diff
Patch9: cpio-2.4.2-rh-glibc.diff
Patch10: cpio-2.4.2-rh-man.diff
Patch11: cpio-2.4.2-rh-mtime.diff
Patch12: cpio-2.4.2-rh-svr4compat.diff
Patch13: cpio-2.4.2-rh-lchown.diff
PreReq: /sbin/install-info
Provides: mt-st, rmt
Prefix: %{_prefix}
BuildRoot: /override/%{name}-%{version}

%description
GNU cpio copies files into or out of a cpio or tar archive.  Archives
are files which contain a collection of other files plus information
about them, such as their file name, owner, timestamps, and access
permissions.  The archive can be another file on the disk, a magnetic
tape, or a pipe.  GNU cpio supports the following archive formats:  binary,
old ASCII, new ASCII, crc, HPUX binary, HPUX old ASCII, old tar and POSIX.1
tar.  By default, cpio creates binary format archives, so that they are
compatible with older cpio programs.  When it is extracting files from
archives, cpio automatically recognizes which kind of archive it is reading
and can read archives created on machines with a different byte-order.

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
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1

%build
rm cpio.info
%configure
make LDFLAGS=-s

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall bindir=$RPM_BUILD_ROOT/bin mandir=$RPM_BUILD_ROOT/%{_mandir}/

mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man8/
install -m 644 rmt.8 ${RPM_BUILD_ROOT}%{_mandir}/man8/

mkdir -p $RPM_BUILD_ROOT/{etc,sbin}
ln -s /usr/libexec/rmt $RPM_BUILD_ROOT/etc/
ln -s /usr/libexec/rmt $RPM_BUILD_ROOT/sbin/

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/cpio.info.gz %{_infodir}/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/cpio.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
%doc README NEWS
/bin/cpio
/bin/mt
/usr/libexec/rmt
/etc/rmt
/sbin/rmt
%{_infodir}/cpio.*
%{_mandir}/man1/cpio.1*
%{_mandir}/man8/rmt.8*

%changelog
* Mon Aug 19 2002 Michail Litvak <mci@owl.openwall.com>
- Deal with info dir entries such that the menu looks pretty.

* Sun Mar 24 2002 Solar Designer <solar@owl.openwall.com>
- Group: Applications/Archiving (be the same as tar).

* Thu Jan 24 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Sun Dec 24 2000 Solar Designer <solar@owl.openwall.com>
- Conflicts -> Provides: mt-st, rmt

* Sat Dec 02 2000 Solar Designer <solar@owl.openwall.com>
- Added /etc/rmt and /sbin/rmt symlinks.
- Conflicts: rmt

* Wed Nov 29 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- imported lchown patch from RH7

* Sun Nov 26 2000 Michail Litvak <mci@owl.openwall.com>
- Imported from RH
- added some patches from Debian
  (many bug fixes in cpio, mt and rmt improvements)
- man page for rmt
