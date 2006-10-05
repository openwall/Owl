# $Owl: Owl/packages/openssh/openssh.spec,v 1.94 2006/10/05 04:13:43 solar Exp $

Summary: The OpenSSH implementation of SSH protocol versions 1 and 2.
Name: openssh
Version: 3.6.1p2
Release: owl19
License: BSD
Group: Applications/Internet
URL: http://www.openssh.com/portable.html
Source0: ftp://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%version.tar.gz
Source1: sshd.pam
Source2: sshd.init
Source3: ssh_config
Source4: sshd_config
Source5: sftp.control
Patch0: openssh-3.6.1p1-owl-warnings.diff
Patch1: openssh-3.6.1p1-owl-hide-unknown.diff
Patch2: openssh-3.6.1p2-owl-always-auth.diff
Patch3: openssh-3.6.1p1-owl-pam_userpass.diff
Patch4: openssh-3.6.1p1-owl-fatal_cleanups.diff
Patch5: openssh-3.6.1p1-owl-drop-groups.diff
Patch6: openssh-3.6.1p1-owl-logging.diff
Patch7: openssh-3.6.1p1-owl-mm.diff
Patch8: openssh-3.6.1p1-owl-password-changing.diff
Patch9: openssh-3.6.1p1-owl-openssl-version-check.diff
Patch10: openssh-3.6.1p1-owl-scp-sftp-stalltime.diff
Patch11: openssh-3.6.1p1-owl-ssh-agent-dumpable.diff
Patch12: openssh-3.6.1p2-cvs-20030603-UseDNS.diff
Patch13: openssh-3.6.1p2-cvs-20030916-buffer-channels-realloc.diff
Patch14: openssh-3.6.1p2-owl-realloc.diff
Patch15: openssh-3.6.1p2-cvs-20050727-scp-fixes.diff
Patch16: openssh-3.6.1p2-owl-sanitize-packet-types.diff
Patch17: openssh-3.6.1p2-cvs-20050725-ssh2-delayed-compression.diff
Patch18: openssh-3.6.1p2-owl-ssh2-delayed-compression-fix.diff
Patch19: openssh-3.6.1p2-cvs-20050921-ssh2-delayed-compression-root.diff
Patch20: openssh-3.6.1p2-cvs-20040205-grace_alarm_handler.diff
Patch21: openssh-3.6.1p2-cvs-20060131-scp-CVE-2006-0225.diff
Patch22: openssh-3.6.1p2-cvs-20060818-sigdie.diff
Patch23: openssh-3.6.1p2-cvs-20060916-deattack.diff
Patch24: openssh-3.6.1p2-cvs-20060919-packet_enable_delayed_compress.diff
Patch25: openssh-3.6.1p2-rh-sftp-memleaks.diff
PreReq: openssl >= 0.9.7, openssl < 0.9.8
Requires: pam >= 0:0.80-owl2
Obsoletes: ssh
BuildRequires: openssl-devel >= 0.9.7g-owl1
BuildRequires: pam-devel, pam_userpass-devel
BuildRequires: perl
BuildRequires: zlib-devel
BuildRequires: tcp_wrappers >= 7.6-owl3.2
BuildRoot: /override/%name-%version

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

%package clients
Summary: OpenSSH clients.
Group: Applications/Internet
Requires: %name = %version-%release
Obsoletes: ssh-clients

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

%package server
Summary: The OpenSSH server daemon.
Group: System Environment/Daemons
PreReq: %name = %version-%release
PreReq: /sbin/chkconfig, grep, shadow-utils, /dev/urandom
Requires: tcp_wrappers >= 7.6-owl3.2
Requires: owl-control >= 0.4, owl-control < 2.0
Requires: /var/empty, tcb, pam_userpass, pam_mktemp
Obsoletes: ssh-server

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
rm -r autom4te.cache
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
%patch13 -p0
%patch14 -p1
%patch15 -p0
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p0
%patch22 -p1
%patch23 -p1
%patch24 -p0
%patch25 -p1
bzip2 -9k ChangeLog

%{expand:%%define _sysconfdir %_sysconfdir/ssh}
%{expand:%%define _datadir %_datadir/ssh}
%{expand:%%define _libexecdir %_libexecdir/ssh}

%build
export LIBS="-lcrypt -lpam -lpam_misc -lpam_userpass"
%configure \
	--with-pam \
	--with-tcp-wrappers \
	--with-ipv4-default \
	--with-default-path=/bin:%_bindir:/usr/local/bin \
	--with-privsep-path=/var/empty \
	--with-privsep-user=sshd
%ifarch alphaev56 alphapca56 alphaev6 alphaev67
%__make deattack.o CFLAGS="%optflags -mcpu=ev5 -Wall"
%endif
%__make

%install
rm -rf %buildroot
%__make install DESTDIR=%buildroot

install -d %buildroot/etc/pam.d
install -d %buildroot/etc/rc.d/init.d
install -m 600 %_sourcedir/sshd.pam %buildroot/etc/pam.d/sshd
install -m 700 %_sourcedir/sshd.init %buildroot/etc/rc.d/init.d/sshd
install -m 644 %_sourcedir/ssh_config %buildroot/etc/ssh/
install -m 600 %_sourcedir/sshd_config %buildroot/etc/ssh/
mkdir -p %buildroot/etc/control.d/facilities
install -m 700 %_sourcedir/sftp.control \
	%buildroot/etc/control.d/facilities/sftp

rm %buildroot%_datadir/Ssh.bin

# create ghosts
touch %buildroot/etc/ssh/ssh_host_{,rsa_,dsa_}key{,.pub}

%pre server
grep -q ^sshd: /etc/group || groupadd -g 74 sshd
grep -q ^sshd: /etc/passwd || useradd -g sshd -u 74 -d / -s /bin/false -M sshd
rm -f /var/run/sshd.restart
if [ $1 -ge 2 ]; then
# XXX: "sshd -t" invoked at this point only validates the old configuration.
	if %_sbindir/sshd -t; then
		/etc/rc.d/init.d/sshd status && touch /var/run/sshd.restart || :
		/etc/rc.d/init.d/sshd stop || :
	fi
	%_sbindir/control-dump sftp
fi

%post server
if [ "$MAKE_CDROM" != yes ]; then
	/etc/rc.d/init.d/sshd keygen
fi
if [ $1 -ge 2 ]; then
	%_sbindir/control-restore sftp
fi
/sbin/chkconfig --add sshd
if [ -f /var/run/sshd.restart ]; then
	/etc/rc.d/init.d/sshd start
elif [ -f /var/run/sshd.pid ]; then
	/etc/rc.d/init.d/sshd restart
fi
rm -f /var/run/sshd.restart
if [ "`%_sbindir/control sftp`" = off ]; then
	echo -n "SFTP server not enabled by default, use "
	echo "\"control sftp on\" to enable"
fi

%preun server
if [ $1 -eq 0 ]; then
	/etc/rc.d/init.d/sshd stop || :
	/sbin/chkconfig --del sshd
fi

%files
%defattr(-,root,root)
%doc CREDITS ChangeLog.bz2 LICENCE README
%attr(0755,root,root) %_bindir/scp
%attr(0755,root,root) %_bindir/ssh-keygen
%attr(0644,root,root) %_mandir/man1/scp.1*
%attr(0644,root,root) %_mandir/man1/ssh-keygen.1*
%attr(0755,root,root) %dir /etc/ssh
%attr(0600,root,root) %config(noreplace) /etc/ssh/moduli
%attr(0755,root,root) %dir %_libexecdir

%files clients
%defattr(-,root,root)
%attr(0755,root,root) %_bindir/ssh
%attr(0755,root,root) %_bindir/ssh-add
%attr(0755,root,root) %_bindir/ssh-agent
%attr(0755,root,root) %_bindir/ssh-keyscan
%attr(0755,root,root) %_bindir/sftp
%attr(0700,root,root) %_libexecdir/ssh-keysign
%attr(0644,root,root) %_mandir/man1/ssh.1*
%attr(0644,root,root) %_mandir/man1/ssh-add.1*
%attr(0644,root,root) %_mandir/man1/ssh-agent.1*
%attr(0644,root,root) %_mandir/man1/ssh-keyscan.1*
%attr(0644,root,root) %_mandir/man1/sftp.1*
%attr(0644,root,root) %_mandir/man5/ssh_config.5*
%attr(0644,root,root) %_mandir/man8/ssh-keysign.8*
%attr(0644,root,root) %config(noreplace) /etc/ssh/ssh_config
%attr(-,root,root) %_bindir/slogin
%attr(-,root,root) %_mandir/man1/slogin.1*

%files server
%defattr(-,root,root)
%attr(0700,root,root) %_sbindir/sshd
%attr(0755,root,root) %_libexecdir/sftp-server
%attr(0644,root,root) %_mandir/man5/sshd_config.5*
%attr(0644,root,root) %_mandir/man8/sshd.8*
%attr(0644,root,root) %_mandir/man8/sftp-server.8*
%attr(0600,root,root) %config(noreplace) %verify(not size md5 mtime) /etc/ssh/sshd_config
%attr(0600,root,root) %config(noreplace) %ghost /etc/ssh/ssh_host*key
%attr(0644,root,root) %config(noreplace) %ghost /etc/ssh/ssh_host*key.pub
%attr(0600,root,root) %config(noreplace) /etc/pam.d/sshd
%attr(0700,root,root) %config /etc/rc.d/init.d/sshd
%attr(0700,root,root) /etc/control.d/facilities/sftp

%changelog
* Tue Oct 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.6.1p2-owl19
- Backported upstream fixes for:
sshd connection consumption vulnerability
(CVE-2004-2069: low, remote, active),
scp local arbitrary command execution vulnerability
(CVE-2006-0225: none to high, local, active),
sshd signal handler race condition
(CVE-2006-5051: none, remote, active),
CRC compensation attack detector DoS
(CVE-2006-4924: low, remote, active),
client NULL dereference on protocol error
(CVE-2006-4925: low, remote, passive).
- Applied RH patch to plug several sftp memory leaks.

* Thu Mar 30 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.6.1p2-owl18
- Added /etc/ssh/ssh_host_* to the server filelist as ghosts.

* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.6.1p2-owl17
- Compressed ChangeLog file.

* Sat Oct 29 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.6.1p2-owl16
- Changed PAM config file to include system-auth for PAM account,
password and session management.
- Stripped /lib/security/ prefix from PAM module names.

* Sat Sep 24 2005 Solar Designer <solar-at-owl.openwall.com> 3.6.1p2-owl15
- Another bugfix for delayed compression: set the authenticated flag for
root logins as well.  Thanks to Damien Miller.

* Thu Jul 28 2005 Solar Designer <solar-at-owl.openwall.com> 3.6.1p2-owl14
- Added delayed compression support for protocol 2 (a back-port of the
changes committed into the OpenBSD CVS recently, with a bugfix added),
enabled by default.  Thanks to Markus Friedl for working on this and for
bringing it to our attention.

* Sat Jun 25 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.6.1p2-owl13
- Rebuilt with libcrypto.so.5.

* Wed Jan 05 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.6.1p2-owl12
- Removed verify checks for sshd_config which is under owl-control.
- Cleaned up the spec a little.

* Wed Nov 03 2004 Solar Designer <solar-at-owl.openwall.com> 3.6.1p2-owl11
- Sanitize packet types early on.

* Thu Sep 09 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.6.1p2-owl10
- Rebuild with OpenSSL 0.9.7.

* Fri Jun 04 2004 Michail Litvak <mci-at-owl.openwall.com> 3.6.1p2-owl9
- Fixed directory traversal vulnerability in scp which allows remote malicious
servers to overwrite arbitrary files (CAN-2004-0175).

* Mon May 03 2004 Solar Designer <solar-at-owl.openwall.com> 3.6.1p2-owl8
- Bumped release to correctly reflect the rebuild against shared libwrap.

* Mon Nov 03 2003 Solar Designer <solar-at-owl.openwall.com> 3.6.1p2-owl7
- Always pass empty passwords into PAM to not produce failed authentication
warnings as empty passwords are tried automatically; this fixes the bug
introduced in the patch in 3.6.1p2-owl1.

* Fri Oct 24 2003 Solar Designer <solar-at-owl.openwall.com> 3.6.1p2-owl6
- Explain how to enable the SFTP server with control(8).
- Generate SSH host keys at startup if needed (for use with bootable CDs).

* Wed Oct 22 2003 Solar Designer <solar-at-owl.openwall.com> 3.6.1p2-owl5
- Set comments in SSH host keys to key type instead of to hostname as the
latter would leak the hostname when doing chrooted installs for other
systems.

* Mon Oct 20 2003 Solar Designer <solar-at-owl.openwall.com> 3.6.1p2-owl4
- Check the validity of sshd_config and host keys with "sshd -t" before
proceeding with a restart or reload.

* Wed Sep 17 2003 Solar Designer <solar-at-owl.openwall.com> 3.6.1p2-owl3
- Included the buffer and channels memory reallocation fixes from:
http://www.openssh.com/txt/buffer.adv (2nd revision).
- Reviewed all uses of *realloc(), resulting in four more fixes of this
nature.

* Mon Jul 21 2003 Solar Designer <solar-at-owl.openwall.com> 3.6.1p2-owl2
- Included a change from the CVS to deprecate VerifyReverseMapping and
replace it with a new option, UseDNS.  This should solve the client
address restriction circumvention attack discovered by Mike Harding.

* Mon Jun 02 2003 Solar Designer <solar-at-owl.openwall.com> 3.6.1p2-owl1
- Updated to 3.6.1p2.
- When we know we're going to fail authentication for reasons external
to PAM, pass there a hopefully incorrect password to have it behave the
same for correct and incorrect passwords.

* Thu May 29 2003 Solar Designer <solar-at-owl.openwall.com> 3.6.1p1-owl4
- write_to=tcb

* Fri Apr 18 2003 Solar Designer <solar-at-owl.openwall.com> 3.6.1p1-owl3
- Added back the now more complete patch to always run PAM with password
authentication, even for non-existent or not allowed usernames.
- Tell pam_tcb to not log failed authentication attempts when a blank
password is tried (blank_nolog) as this is attempted automatically.
- Pass prefix= and count= to pam_tcb also for authentication such that it
can use this information to reduce timing leaks.

* Tue Apr 08 2003 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.6.1p1-owl2
- Updated pam_userpass support: build with libpam_userpass.

* Tue Apr 08 2003 Solar Designer <solar-at-owl.openwall.com> 3.6.1p1-owl1
- Updated to 3.6.1p1.
- Make ssh-agent protect itself by setting prctl(PR_SET_DUMPABLE, 0) on
Linux 2.4+.

* Thu Dec 19 2002 Solar Designer <solar-at-owl.openwall.com>
- New release number for linking against tcp_wrappers with Steve Grubb's
error handling fix.

* Sun Nov 03 2002 Solar Designer <solar-at-owl.openwall.com>
- Dump/restore the owl-control setting for sftp on package upgrades.

* Thu Aug 29 2002 Solar Designer <solar-at-owl.openwall.com>
- Corrected the dependencies (many are specific to the server package).

* Sun Jul 28 2002 Solar Designer <solar-at-owl.openwall.com>
- Install the packet_close() cleanup for the client as well.

* Sun Jul 07 2002 Solar Designer <solar-at-owl.openwall.com>
- Install the packet_close() cleanup for root logins as well (which are
not privilege separated because that wouldn't make sense and thus were
handled by a different code path which I initially have missed).

* Sat Jul 06 2002 Solar Designer <solar-at-owl.openwall.com>
- Re-initialize logging after calls into PAM module stacks, make use of
log_reinit() where the original code needed that kind of functionality.
- Stack pam_limits for account management, not session setup, such that
its configuration file doesn't need to be world-readable with privsep.

* Fri Jul 05 2002 Solar Designer <solar-at-owl.openwall.com>
- Re-enable the password changing code (disabled in 3.3p1 and 3.4p1) for
non-privsep case, disallowing any forwardings (such that the session may
not be actually used while still not changing the expired password).
- Limit three of the cleanup functions to apply to just the proper sshd
processes, make sure session_pty_cleanup() happens before packet_close().

* Tue Jul 02 2002 Solar Designer <solar-at-owl.openwall.com>
- In the PAM conversation, queue any text messages appearing in initial
login mode for printing later, similarly to what the original code did.
This is needed to pass password expiration warnings on to the user.

* Sat Jun 29 2002 Solar Designer <solar-at-owl.openwall.com>
- Keep the /dev/log fd open and only close it before executing other
programs, to enable direct logging from chrooted child processes.

* Thu Jun 27 2002 Solar Designer <solar-at-owl.openwall.com>
- Updated to 3.4p1.
- Zero out the written-to pages in memory mapped areas when they're
destroyed to reduce the chances of sensitive data remaining on disk media
in a remotely-recoverable way while not wasting any extra physical pages
or filesystem blocks.

* Tue Jun 25 2002 Solar Designer <solar-at-owl.openwall.com>
- Fixed the dropping of supplementary groups now included in 3.3p1 rather
than adding our own version of the fix, to allow for running sshd as
non-root and to be fail-close whenever possible.

* Sun Jun 23 2002 Solar Designer <solar-at-owl.openwall.com>
- Updated to 3.3p1 with privilege separation.
- If MAP_ANON|MAP_SHARED fails (is unsupported on Linux 2.2), fallback
to using SysV shm, and, if that fails too (SysV shm is a compile-time
kernel option), to MAP_SHARED with sparse and unlinked swap files.
- pam_mktemp is now run during account management, not session setup,
as the latter is no longer done as root (possibly something to be
reverted in future versions).

* Sat Jun 08 2002 Solar Designer <solar-at-owl.openwall.com>
- Build deattack.c with -mcpu=ev5 when building for alphaev56+ to not
trigger a not fully debugged problem with the EV56+ code.

* Sun Mar 17 2002 Solar Designer <solar-at-owl.openwall.com>
- Updated to 3.1p1.

* Tue Mar 05 2002 Solar Designer <solar-at-owl.openwall.com>
- Patched a channel id check off by one bug discovered by Joost Pol.

* Tue Feb 05 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Wed Dec 12 2001 Solar Designer <solar-at-owl.openwall.com>
- Updated to 3.0.2p1.

* Fri Nov 16 2001 Solar Designer <solar-at-owl.openwall.com>
- Use pam_tcb.

* Sun Oct 07 2001 Solar Designer <solar-at-owl.openwall.com>
- Updates to appl_userpass.c to support building against Linux-PAM 0.74+.

* Sat Sep 29 2001 Solar Designer <solar-at-owl.openwall.com>
- Include post-2.9.9 fixes from the CVS, most importantly to restore the
order of reading for ~/.ssh/config and /etc/ssh_config.

* Thu Sep 27 2001 Solar Designer <solar-at-owl.openwall.com>
- Updated to 2.9.9p2.
- Patched the OpenSSL version check to ignore the patch and status bits.
- Drop supplementary groups at sshd startup such that they aren't inherited
by the PAM modules.

* Wed Jul 11 2001 Solar Designer <solar-at-owl.openwall.com>
- New release number for upgrades after building against OpenSSL 0.9.6b.

* Fri Jun 15 2001 Solar Designer <solar-at-owl.openwall.com>
- Prevent additional timing leaks with null passwords (when allowed),
updated patch from Rafal Wojtczuk <nergal at owl.openwall.com>.

* Mon Jun 11 2001 Solar Designer <solar-at-owl.openwall.com>
- Switch credentials when cleaning up temporary files and sockets to fix
the vulnerability reported by <zen-parse at gmx.net> on Bugtraq; the patch is
by Markus Friedl with a later OpenSSH CVS change added and two bugs fixed.

* Sun May 06 2001 Solar Designer <solar-at-owl.openwall.com>
- Updated to 2.9p1.
- Added sftp.control.

* Sun Apr 22 2001 Solar Designer <solar-at-owl.openwall.com>
- New release number for upgrades after building against OpenSSL 0.9.6a.

* Sun Apr 01 2001 Solar Designer <solar-at-owl.openwall.com>
- Patch from the CVS to not use AES/Rijndael against OpenSSH versions
with bigendian bug.

* Fri Mar 23 2001 Solar Designer <solar-at-owl.openwall.com>
- Updated to 2.5.2p2.
- Dropped two PAM patches (included in 2.5.2p2).

* Wed Mar 21 2001 Solar Designer <solar-at-owl.openwall.com>
- Updated to 2.5.2p1.
- Patched a potential uninitialized reference in do_pam_cleanup_proc().

* Mon Mar 19 2001 Solar Designer <solar-at-owl.openwall.com>
- Package files introduced with 2.5.0 (primes, sftp, ssh-keyscan).

* Sun Mar 18 2001 Solar Designer <solar-at-owl.openwall.com>
- Increased the STALLTIME for scp from 5 to 60 seconds (needed for large
windows and slow links).
- scp will now calculate ETA without account for possible stall time.

* Wed Feb 28 2001 Solar Designer <solar-at-owl.openwall.com>
- Updated to 2.5.1p1.
- Updated the don't-log-unknown-users and pam_userpass patches.
- Added a patch to always run PAM authentication, even for unknown users
(makes it less trivial to check for valid usernames; still easy, though).
- Dropped the traffic analysis patch (OpenSSH now includes an improved
version).
- Dropped the client version string NUL termination patch (fixed).

* Fri Jan 26 2001 Solar Designer <solar-at-owl.openwall.com>
- Added a patch to reduce the impact of traffic analysis by padding initial
login passwords for SSH-1 and simulating echo during interactive sessions.
(Thanks to Dug Song for updating the patch to current OpenSSH.)

* Wed Dec 20 2000 Solar Designer <solar-at-owl.openwall.com>
- Use pam_mktemp.

* Thu Dec 07 2000 Solar Designer <solar-at-owl.openwall.com>
- Updated sshd.init to use --pidfile and --expect-user.

* Fri Dec 01 2000 Solar Designer <solar-at-owl.openwall.com>
- Adjusted sshd.init for owl-startup.
- Restart sshd after package upgrades in an owl-startup compatible way.
- Corrected package descriptions.

* Mon Nov 20 2000 Solar Designer <solar-at-owl.openwall.com>
- Updated to 2.3.0p1.

* Fri Aug 04 2000 Solar Designer <solar-at-owl.openwall.com>
- Updated to 2.1.1p4.

* Sun Jul 23 2000 Solar Designer <solar-at-owl.openwall.com>
- Added dependencies on pam_userpass and /dev/urandom into openssh-server.

* Mon Jul 17 2000 Solar Designer <solar-at-owl.openwall.com>
- Added a patch to not log unknown usernames (someone could have typed
their password at the username prompt by mistake, even though there's no
such prompt with the "native" client).

* Wed Jul 12 2000 Solar Designer <solar-at-owl.openwall.com>
- Cleaned up the default ssh*_config.
- The config files are now declared as separate Source's in this spec.
- Moved this changelog to end of spec file.

* Sun Jul 09 2000 Solar Designer <solar-at-owl.openwall.com>
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
