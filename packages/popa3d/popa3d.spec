# $Id: Owl/packages/popa3d/popa3d.spec,v 1.7 2001/09/08 21:47:01 solar Exp $

Summary: A tiny POP3 server with security as its primary design goal
Name: popa3d
Version: 0.4.9.3
Release: 1owl
Copyright: relaxed BSD and (L)GPL-compatible
Group: System Environment/Daemons
Source0: ftp://ftp.openwall.com/pub/projects/popa3d/popa3d-%{version}.tar.gz
Source1: popa3d.pam
Source2: popa3d.init
Source3: popa3d.xinetd
Patch0: popa3d-0.4.9.3-owl-params.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Requires: /usr/share/empty, pam_userpass, xinetd
Prereq: /sbin/chkconfig, /dev/null, grep, shadow-utils

%description
popa3d is a tiny POP3 server with security as its primary design goal.

%prep
%setup -q
%patch0 -p1

%build
make CFLAGS="-c -Wall $RPM_OPT_FLAGS -DHAVE_PROGNAME" LIBS="-lpam"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{usr/sbin,etc/{pam.d,rc.d/init.d,xinetd.d}}

install -m 700 popa3d $RPM_BUILD_ROOT/usr/sbin/
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
/usr/sbin/popa3d
%config(noreplace) /etc/pam.d/popa3d
%config /etc/rc.d/init.d/popa3d
%config /etc/xinetd.d/popa3d
%doc DESIGN LICENSE

%changelog
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
