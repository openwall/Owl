# $Id: Owl/packages/openssh/openssh.spec,v 1.22 2001/06/10 23:24:12 solar Exp $

Summary: OpenSSH free Secure Shell (SSH) implementation
Name: openssh
Version: 2.9p1
Release: 2owl
URL: http://www.openssh.com/
Source0: ftp://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz
Source1: sshd.pam
Source2: sshd.init
Source3: ssh_config
Source4: sshd_config
Source5: sftp.control
Patch0: openssh-2.9p1-owl-hide-unknown.diff
Patch1: openssh-2.9p1-owl-always-auth.diff
Patch2: openssh-2.9p1-owl-pam_userpass.diff
Patch3: openssh-2.5.1p1-owl-scp-stalltime.diff
Patch4: openssh-2.9p1-markus-unlink.diff
Copyright: BSD
Group: Applications/Internet
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Obsoletes: ssh
Requires: pam_mktemp
PreReq: openssl >= 0.9.6a-1owl
BuildPreReq: openssl-devel >= 0.9.6a-1owl
BuildPreReq: pam >= 0.72-8owl
BuildPreReq: perl
BuildPreReq: zlib-devel
BuildPreReq: tcp_wrappers

%package clients
Summary: OpenSSH Secure Shell protocol clients
Requires: openssh
Group: System Environment/Daemons
Obsoletes: ssh-clients

%package server
Summary: OpenSSH Secure Shell protocol server (sshd)
Group: System Environment/Daemons
Obsoletes: ssh-server
PreReq: openssh, chkconfig >= 0.9, pam_userpass, /dev/urandom

%description
SSH (Secure Shell) is a program for logging into a remote machine and for
executing commands on a remote machine.  It is intended to replace
rlogin and rsh, and provide secure encrypted communications between
two untrusted hosts over an insecure network.  X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's rework of the last free version of SSH, bringing it
up to date in terms of security and features, as well as removing all
patented algorithms to separate libraries (OpenSSL).

This package includes the core files necessary for both the OpenSSH
client and server.  To make this package useful, you should also
install openssh-clients, openssh-server, or both.

%description clients
SSH (Secure Shell) is a program for logging into a remote machine and for
executing commands on a remote machine.  It is intended to replace
rlogin and rsh, and provide secure encrypted communications between
two untrusted hosts over an insecure network.  X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's rework of the last free version of SSH, bringing it
up to date in terms of security and features, as well as removing all
patented algorithms to separate libraries (OpenSSL).

This package includes the clients necessary to make encrypted connections
to SSH servers.

%description server
SSH (Secure Shell) is a program for logging into a remote machine and for
executing commands on a remote machine.  It is intended to replace
rlogin and rsh, and provide secure encrypted communications between
two untrusted hosts over an insecure network.  X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's rework of the last free version of SSH, bringing it
up to date in terms of security and features, as well as removing all
patented algorithms to separate libraries (OpenSSL).

This package contains the secure shell daemon, sshd, which allows SSH
clients to connect to your host.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
CFLAGS="$RPM_OPT_FLAGS" LIBS="-lcrypt -lpam -lpam_misc" ./configure \
	--prefix=/usr --sysconfdir=/etc/ssh --libexecdir=/usr/libexec/ssh \
	--with-pam --disable-suid-ssh \
	--with-tcp-wrappers --with-ipv4-default \
	--with-rsh=/usr/bin/rsh \
	--with-default-path=/bin:/usr/bin:/usr/local/bin
make DESTDIR=$RPM_BUILD_ROOT/

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/pam.d
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT/usr/libexec/ssh
install -m 600 %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/sshd
install -m 700 %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/sshd
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT/etc/ssh/ssh_config
install -m 600 %{SOURCE4} $RPM_BUILD_ROOT/etc/ssh/sshd_config
mkdir -p $RPM_BUILD_ROOT/etc/control.d/facilities
install -m 700 %{SOURCE5} $RPM_BUILD_ROOT/etc/control.d/facilities/sftp

%clean
rm -rf $RPM_BUILD_ROOT

%pre server
rm -f /var/run/sshd.restart
if [ $1 -ge 2 ]; then
	/etc/rc.d/init.d/sshd status && touch /var/run/sshd.restart || :
	/etc/rc.d/init.d/sshd stop || :
fi

%post server
/sbin/chkconfig --add sshd
if [ ! -f /etc/ssh/ssh_host_key -o ! -s /etc/ssh/ssh_host_key ]; then
	/usr/bin/ssh-keygen -b 1024 -f /etc/ssh/ssh_host_key -N '' >&2
fi
if [ ! -f /etc/ssh/ssh_host_dsa_key -o ! -s /etc/ssh/ssh_host_dsa_key ]; then
	/usr/bin/ssh-keygen -d -f /etc/ssh/ssh_host_dsa_key -N '' >&2
fi
if [ -f /var/run/sshd.restart ]; then
	/etc/rc.d/init.d/sshd start
elif [ -f /var/run/sshd.pid ]; then
	/etc/rc.d/init.d/sshd restart
fi
rm -f /var/run/sshd.restart

%preun server
if [ $1 -eq 0 ]; then
	/etc/rc.d/init.d/sshd stop || :
	/sbin/chkconfig --del sshd
fi

%files
%defattr(-,root,root)
%doc README CREDITS LICENCE ChangeLog
%attr(0755,root,root) /usr/bin/ssh-keygen
%attr(0755,root,root) /usr/bin/scp
%attr(0755,root,root) /usr/bin/ssh-keyscan
%attr(0644,root,root) /usr/man/man1/ssh-keygen.1*
%attr(0644,root,root) /usr/man/man1/ssh-keyscan.1*
%attr(0644,root,root) /usr/man/man1/scp.1*
%attr(0755,root,root) %dir /etc/ssh
%attr(0600,root,root) %config(noreplace) /etc/ssh/primes
%attr(0755,root,root) %dir /usr/libexec/ssh

%files clients
%defattr(-,root,root)
%attr(0755,root,root) /usr/bin/ssh
%attr(0755,root,root) /usr/bin/ssh-agent
%attr(0755,root,root) /usr/bin/ssh-add
%attr(0755,root,root) /usr/bin/sftp
%attr(0644,root,root) /usr/man/man1/ssh.1*
%attr(0644,root,root) /usr/man/man1/ssh-agent.1*
%attr(0644,root,root) /usr/man/man1/ssh-add.1*
%attr(0644,root,root) /usr/man/man1/sftp.1*
%attr(0644,root,root) %config(noreplace) /etc/ssh/ssh_config
%attr(-,root,root) /usr/bin/slogin
%attr(-,root,root) /usr/man/man1/slogin.1*

%files server
%defattr(-,root,root)
%attr(0700,root,root) /usr/sbin/sshd
%attr(0755,root,root) /usr/libexec/ssh/sftp-server
%attr(0644,root,root) /usr/man/man8/sshd.8*
%attr(0644,root,root) /usr/man/man8/sftp-server.8*
%attr(0600,root,root) %config(noreplace) /etc/ssh/sshd_config
%attr(0600,root,root) %config(noreplace) /etc/pam.d/sshd
%attr(0700,root,root) %config /etc/rc.d/init.d/sshd
%attr(0700,root,root) /etc/control.d/facilities/sftp

%changelog
* Mon Jun 11 2001 Solar Designer <solar@owl.openwall.com>
- Switch credentials when cleaning up temporary files and sockets to fix
the vulnerability reported by zen-parse@gmx.net on Bugtraq; the patch is
by Markus Friedl, with a later OpenSSH CVS change added.

* Sun May 06 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 2.9p1.
- Added sftp.control.

* Sun Apr 22 2001 Solar Designer <solar@owl.openwall.com>
- New release number for upgrades after building against OpenSSL 0.9.6a.

* Sun Apr 01 2001 Solar Designer <solar@owl.openwall.com>
- Patch from the CVS to not use AES/Rijndael against OpenSSH versions
with bigendian bug.

* Fri Mar 23 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 2.5.2p2.
- Dropped two PAM patches (included in 2.5.2p2).

* Wed Mar 21 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 2.5.2p1.
- Patched a potential uninitialized reference in do_pam_cleanup_proc().

* Mon Mar 19 2001 Solar Designer <solar@owl.openwall.com>
- Package files introduced with 2.5.0 (primes, sftp, ssh-keyscan).

* Sun Mar 18 2001 Solar Designer <solar@owl.openwall.com>
- Increased the STALLTIME for scp from 5 to 60 seconds (needed for large
windows and slow links).
- scp will now calculate ETA without account for possible stall time.

* Wed Feb 28 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 2.5.1p1.
- Updated the don't-log-unknown-users and pam_userpass patches.
- Added a patch to always run PAM authentication, even for unknown users
(makes it less trivial to check for valid usernames; still easy, though).
- Dropped the traffic analysis patch (OpenSSH now includes an improved
version).
- Dropped the client version string NUL termination patch (fixed).

* Fri Jan 26 2001 Solar Designer <solar@owl.openwall.com>
- Added a patch to reduce the impact of traffic analysis by padding initial
login passwords for SSH-1 and simulating echo during interactive sessions.
(Thanks to Dug Song for updating the patch to current OpenSSH.)

* Wed Dec 20 2000 Solar Designer <solar@owl.openwall.com>
- Use pam_mktemp.

* Thu Dec 07 2000 Solar Designer <solar@owl.openwall.com>
- Updated sshd.init to use --pidfile and --expect-user.

* Fri Dec 01 2000 Solar Designer <solar@owl.openwall.com>
- Adjusted sshd.init for owl-startup.
- Restart sshd after package upgrades in an owl-startup compatible way.
- Corrected package descriptions.

* Mon Nov 20 2000 Solar Designer <solar@owl.openwall.com>
- Updated to 2.3.0p1.

* Fri Aug 04 2000 Solar Designer <solar@owl.openwall.com>
- Updated to 2.1.1p4.

* Sun Jul 23 2000 Solar Designer <solar@owl.openwall.com>
- Added dependencies on pam_userpass and /dev/urandom into openssh-server.

* Mon Jul 17 2000 Solar Designer <solar@owl.openwall.com>
- Added a patch to not log unknown usernames (someone could have typed
their password at the username prompt by mistake, even though there's no
such prompt with the "native" client).

* Wed Jul 12 2000 Solar Designer <solar@owl.openwall.com>
- Cleaned up the default ssh*_config.
- The config files are now declared as separate Source's in this spec.
- Moved this changelog to end of spec file.

* Sun Jul 09 2000 Solar Designer <solar@owl.openwall.com>
- Imported current Damien Miller's spec file, removed the X11-specific
stuff, fixed buildroot issues.
- sshd.pam and sshd.init are now taken from separate files, not the
original package.
- Added -lcrypt so that PAM modules may access crypt(3); the OpenSSL
package should also have a patch applied so that it doesn't export its
crypt() function as a symbol, but only #define it in the appropriate
header file.  Other things might break (look for "DES corruption" in
ChangeLog), but this is better than getting failed authentication with
modern hashes and I believe current glibc is careful not to export
internal functions and use weak aliases when exporting things.
- Patched PAM authentication to use pam_userpass rather than assume
that modules can only ask for a password.
- Changed default ssh*_config.
- non-SUID installation by default.

* Mon Jun 12 2000 Damien Miller <djm@mindrot.org>
- Glob manpages to catch compressed files
* Wed Mar 15 2000 Damien Miller <djm@ibs.com.au>
- Updated for new location
- Updated for new gnome-ssh-askpass build
* Sun Dec 26 1999 Damien Miller <djm@mindrot.org>
- Added Jim Knoble's <jmknoble@pobox.com> askpass
* Mon Nov 15 1999 Damien Miller <djm@mindrot.org>
- Split subpackages further based on patch from jim knoble <jmknoble@pobox.com>
* Sat Nov 13 1999 Damien Miller <djm@mindrot.org>
- Added 'Obsoletes' directives
* Tue Nov 09 1999 Damien Miller <djm@ibs.com.au>
- Use make install
- Subpackages
* Mon Nov 08 1999 Damien Miller <djm@ibs.com.au>
- Added links for slogin
- Fixed perms on manpages
* Sat Oct 30 1999 Damien Miller <djm@ibs.com.au>
- Renamed init script
* Fri Oct 29 1999 Damien Miller <djm@ibs.com.au>
- Back to old binary names
* Thu Oct 28 1999 Damien Miller <djm@ibs.com.au>
- Use autoconf
- New binary names
* Wed Oct 27 1999 Damien Miller <djm@ibs.com.au>
- Initial RPMification, based on Jan "Yenya" Kasprzak's <kas@fi.muni.cz> spec.
