# $Id: Owl/packages/popa3d/popa3d.spec,v 1.11 2002/02/06 22:52:45 mci Exp $

Summary: Post Office Protocol server.
Name: popa3d
Version: 0.5
Release: owl2
License: relaxed BSD and (L)GPL-compatible
Group: System Environment/Daemons
Source0: ftp://ftp.openwall.com/pub/projects/popa3d/popa3d-%{version}.tar.gz
Source1: params.h
Source2: popa3d.pam
Source3: popa3d.init
Source4: popa3d.xinetd
PreReq: /sbin/chkconfig, /dev/null, grep, shadow-utils
Requires: /var/empty, tcb, pam_userpass, xinetd
BuildRoot: /override/%{name}-%{version}

%description
popa3d is a tiny Post Office Protocol version 3 (POP3) server with
security as its primary design goal.

%prep
%setup -q
cp $RPM_SOURCE_DIR/params.h params.h

%build
make CFLAGS="-c -Wall $RPM_OPT_FLAGS -DHAVE_PROGNAME" LIBS="-lpam"

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT SBINDIR=%_sbindir MANDIR=%_mandir

mkdir -p $RPM_BUILD_ROOT/etc/{pam.d,rc.d/init.d,xinetd.d}
install -m 600 $RPM_SOURCE_DIR/popa3d.pam \
	$RPM_BUILD_ROOT/etc/pam.d/popa3d
install -m 700 $RPM_SOURCE_DIR/popa3d.init \
	$RPM_BUILD_ROOT/etc/rc.d/init.d/popa3d
install -m 600 $RPM_SOURCE_DIR/popa3d.xinetd \
	$RPM_BUILD_ROOT/etc/xinetd.d/popa3d

%clean
rm -rf $RPM_BUILD_ROOT

%pre
grep ^popa3d: /etc/group &> /dev/null || groupadd -g 184 popa3d
grep ^popa3d: /etc/passwd &> /dev/null ||
	useradd -g popa3d -u 184 -d / -s /bin/false -M popa3d
rm -f /var/run/popa3d.restart
if [ $1 -ge 2 ]; then
	/etc/rc.d/init.d/popa3d status && touch /var/run/popa3d.restart || :
	/etc/rc.d/init.d/popa3d stop || :
fi

%post
test -f /var/run/popa3d.restart && /etc/rc.d/init.d/popa3d start || :
rm -f /var/run/popa3d.restart

%preun
if [ $1 -eq 0 ]; then
	/etc/rc.d/init.d/popa3d stop || :
	/sbin/chkconfig --del popa3d
fi

%files
%defattr(-,root,root)
%_sbindir/popa3d
%_mandir/man8/popa3d.8*
%config(noreplace) /etc/pam.d/popa3d
%config /etc/rc.d/init.d/popa3d
%config /etc/xinetd.d/popa3d
%doc DESIGN LICENSE

%changelog
* Thu Feb 07 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions.

* Fri Nov 16 2001 Solar Designer <solar@owl.openwall.com>
- Use pam_tcb.

* Sun Oct 28 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 0.5 which adds a popa3d(8) man page.

* Tue Sep 11 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 0.4.9.4 (fixed two bugs introduced with 0.4.9.2 and 0.4.9.3).

* Sun Sep 09 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 0.4.9.3.
- The same popa3d binary may now be run as a standalone server as well as
via xinetd, an /etc/xinetd.d file is provided.

* Sun Sep 02 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 0.4.9.2.

* Wed Jun 20 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 0.4.9.1 (finally replaced the GNU MD5 routines to relax
the license for the entire package, solve certain portability issues,
and reduce code size).

* Mon May 28 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 0.4.9.

* Thu Dec 07 2000 Solar Designer <solar@owl.openwall.com>
- Updated popa3d.init to use --expect-user.

* Wed Dec 06 2000 Solar Designer <solar@owl.openwall.com>
- 0.4.4 with pam_userpass support.
- Wrote this spec file, popa3d.pam, and popa3d.init.
