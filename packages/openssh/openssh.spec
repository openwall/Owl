# $Id: Owl/packages/openssh/openssh.spec,v 1.42 2002/07/01 20:15:57 solar Exp $

Summary: The OpenSSH implementation of SSH protocol versions 1 and 2.
Name: openssh
Version: 3.4p1
Release: owl1.3
License: BSD
Group: Applications/Internet
URL: http://www.openssh.com/portable.html
Source0: ftp://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz
Source1: sshd.pam
Source2: sshd.init
Source3: ssh_config
Source4: sshd_config
Source5: sftp.control
Patch0: openssh-3.4p1-owl-warnings.diff
Patch1: openssh-3.4p1-owl-hide-unknown.diff
Patch2: openssh-3.4p1-owl-always-auth.diff
Patch3: openssh-3.4p1-owl-pam_userpass.diff
Patch4: openssh-3.4p1-owl-drop-groups.diff
Patch5: openssh-3.4p1-owl-openssl-version-check.diff
Patch6: openssh-3.4p1-owl-scp-stalltime.diff
Patch7: openssh-3.4p1-owl-mm.diff
Patch8: openssh-3.4p1-owl-logging.diff
PreReq: openssl >= 0.9.6b-1owl
PreReq: openssl < 0.9.7
PreReq: /sbin/chkconfig, grep, shadow-utils
Requires: /var/empty, tcb, pam_userpass, pam_mktemp
Obsoletes: ssh
BuildRequires: openssl-devel >= 0.9.6b-1owl
BuildRequires: pam-devel
BuildRequires: perl
BuildRequires: zlib-devel
BuildRequires: tcp_wrappers
BuildRoot: /override/%{name}-%{version}

%package clients
Summary: OpenSSH clients.
Group: Applications/Internet
Requires: openssh = %{version}-%{release}
Obsoletes: ssh-clients

%package server
Summary: The OpenSSH server daemon.
Group: System Environment/Daemons
PreReq: openssh = %{version}-%{release}
PreReq: chkconfig >= 0.9, pam_userpass, /dev/urandom
Obsoletes: ssh-server

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
rm -r autom4te-*.cache
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%define _sysconfdir /etc/ssh
%{expand:%%define _datadir %{_datadir}/ssh}
%{expand:%%define _libexecdir %{_libexecdir}/ssh}

%build
export LIBS="-lcrypt -lpam -lpam_misc"
%configure \
	--with-pam \
	--with-tcp-wrappers \
	--with-ipv4-default \
	--with-default-path=/bin:/usr/bin:/usr/local/bin \
	--with-privsep-path=/var/empty \
	--with-privsep-user=sshd
%ifarch alphaev56 alphapca56 alphaev6 alphaev67
make deattack.o CFLAGS="$RPM_OPT_FLAGS -mcpu=ev5 -Wall"
%endif
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/pam.d
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -m 600 $RPM_SOURCE_DIR/sshd.pam $RPM_BUILD_ROOT/etc/pam.d/sshd
install -m 700 $RPM_SOURCE_DIR/sshd.init $RPM_BUILD_ROOT/etc/rc.d/init.d/sshd
install -m 644 $RPM_SOURCE_DIR/ssh_config $RPM_BUILD_ROOT/etc/ssh/
install -m 600 $RPM_SOURCE_DIR/sshd_config $RPM_BUILD_ROOT/etc/ssh/
mkdir -p $RPM_BUILD_ROOT/etc/control.d/facilities
install -m 700 $RPM_SOURCE_DIR/sftp.control \
	$RPM_BUILD_ROOT/etc/control.d/facilities/sftp

%clean
rm -rf $RPM_BUILD_ROOT

%pre server
grep -q ^sshd: /etc/group || groupadd -g 74 sshd
grep -q ^sshd: /etc/passwd || useradd -g sshd -u 74 -d / -s /bin/false -M sshd
rm -f /var/run/sshd.restart
if [ $1 -ge 2 ]; then
	/etc/rc.d/init.d/sshd status && touch /var/run/sshd.restart || :
	/etc/rc.d/init.d/sshd stop || :
fi

%post server
/sbin/chkconfig --add sshd
if [ ! -f /etc/ssh/ssh_host_key -o ! -s /etc/ssh/ssh_host_key ]; then
	/usr/bin/ssh-keygen -t rsa1 -f /etc/ssh/ssh_host_key -N '' >&2
fi
if [ ! -f /etc/ssh/ssh_host_dsa_key -o ! -s /etc/ssh/ssh_host_dsa_key ]; then
	/usr/bin/ssh-keygen -t dsa -f /etc/ssh/ssh_host_dsa_key -N '' >&2
fi
if [ ! -f /etc/ssh/ssh_host_rsa_key -o ! -s /etc/ssh/ssh_host_rsa_key ]; then
	/usr/bin/ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N '' >&2
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
%attr(0755,root,root) /usr/bin/scp
%attr(0755,root,root) /usr/bin/ssh-keygen
%attr(0644,root,root) %{_mandir}/man1/scp.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-keygen.1*
%attr(0755,root,root) %dir /etc/ssh
%attr(0600,root,root) %config(noreplace) /etc/ssh/moduli
%attr(0755,root,root) %dir %{_libexecdir}

%files clients
%defattr(-,root,root)
%attr(0755,root,root) /usr/bin/ssh
%attr(0755,root,root) /usr/bin/ssh-add
%attr(0755,root,root) /usr/bin/ssh-agent
%attr(0755,root,root) /usr/bin/ssh-keyscan
%attr(0755,root,root) /usr/bin/sftp
%attr(0700,root,root) %{_libexecdir}/ssh-keysign
%attr(0644,root,root) %{_mandir}/man1/ssh.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-add.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-agent.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-keyscan.1*
%attr(0644,root,root) %{_mandir}/man1/sftp.1*
%attr(0644,root,root) %{_mandir}/man5/ssh_config.5*
%attr(0644,root,root) %{_mandir}/man8/ssh-keysign.8*
%attr(0644,root,root) %config(noreplace) /etc/ssh/ssh_config
%attr(-,root,root) /usr/bin/slogin
%attr(-,root,root) %{_mandir}/man1/slogin.1*

%files server
%defattr(-,root,root)
%attr(0700,root,root) /usr/sbin/sshd
%attr(0755,root,root) %{_libexecdir}/sftp-server
%attr(0644,root,root) %{_mandir}/man5/sshd_config.5*
%attr(0644,root,root) %{_mandir}/man8/sshd.8*
%attr(0644,root,root) %{_mandir}/man8/sftp-server.8*
%attr(0600,root,root) %config(noreplace) /etc/ssh/sshd_config
%attr(0600,root,root) %config(noreplace) /etc/pam.d/sshd
%attr(0700,root,root) %config /etc/rc.d/init.d/sshd
%attr(0700,root,root) /etc/control.d/facilities/sftp

%changelog
* Tue Jul 02 2002 Solar Designer <solar@owl.openwall.com>
- In the PAM conversation, queue any text messages appearing in initial
login mode for printing later, similarly to what the original code did.
This is needed to pass password expiration warnings on to the user.

* Sat Jun 29 2002 Solar Designer <solar@owl.openwall.com>
- Keep the /dev/log fd open and only close it before executing other
programs, to enable direct logging from chrooted child processes.

* Thu Jun 27 2002 Solar Designer <solar@owl.openwall.com>
- Updated to 3.4p1.
- Zero out the written-to pages in memory mapped areas when they're
destroyed to reduce the chances of sensitive data remaining on disk media
in a remotely-recoverable way while not wasting any extra physical pages
or filesystem blocks.

* Tue Jun 25 2002 Solar Designer <solar@owl.openwall.com>
- Fixed the dropping of supplementary groups now included in 3.3p1 rather
than adding our own version of the fix, to allow for running sshd as
non-root and to be fail-close whenever possible.

* Sun Jun 23 2002 Solar Designer <solar@owl.openwall.com>
- Updated to 3.3p1 with privilege separation.
- If MAP_ANON|MAP_SHARED fails (is unsupported on Linux 2.2), fallback
to using SysV shm, and, if that fails too (SysV shm is a compile-time
kernel option), to MAP_SHARED with sparse and unlinked swap files.
- pam_mktemp is now run during account management, not session setup,
as the latter is no longer done as root (possibly something to be
reverted in future versions).

* Sat Jun 08 2002 Solar Designer <solar@owl.openwall.com>
- Build deattack.c with -mcpu=ev5 when building for alphaev56+ to not
trigger a not fully debugged problem with the EV56+ code.

* Sun Mar 17 2002 Solar Designer <solar@owl.openwall.com>
- Updated to 3.1p1.

* Tue Mar 05 2002 Solar Designer <solar@owl.openwall.com>
- Patched a channel id check off by one bug discovered by Joost Pol.

* Tue Feb 05 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Wed Dec 12 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 3.0.2p1.

* Fri Nov 16 2001 Solar Designer <solar@owl.openwall.com>
- Use pam_tcb.

* Sun Oct 07 2001 Solar Designer <solar@owl.openwall.com>
- Updates to appl_userpass.c to support building against Linux-PAM 0.74+.

* Sat Sep 29 2001 Solar Designer <solar@owl.openwall.com>
- Include post-2.9.9 fixes from the CVS, most importantly to restore the
order of reading for ~/.ssh/config and /etc/ssh_config.

* Thu Sep 27 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 2.9.9p2.
- Patched the OpenSSL version check to ignore the patch and status bits.
- Drop supplementary groups at sshd startup such that they aren't inherited
by the PAM modules.

* Wed Jul 11 2001 Solar Designer <solar@owl.openwall.com>
- New release number for upgrades after building against OpenSSL 0.9.6b.

* Fri Jun 15 2001 Solar Designer <solar@owl.openwall.com>
- Prevent additional timing leaks with null passwords (when allowed),
updated patch from Rafal Wojtczuk <nergal@owl.openwall.com>.

* Mon Jun 11 2001 Solar Designer <solar@owl.openwall.com>
- Switch credentials when cleaning up temporary files and sockets to fix
the vulnerability reported by zen-parse@gmx.net on Bugtraq; the patch is
by Markus Friedl with a later OpenSSH CVS change added and two bugs fixed.

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
