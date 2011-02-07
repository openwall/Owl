# $Owl: Owl/packages/owl-etc/owl-etc.spec,v 1.78 2011/02/07 17:43:23 segoon Exp $

Summary: Initial set of configuration files.
Name: owl-etc
Version: 1.0
Release: owl2
License: public domain
Group: System Environment/Base
Source0: passwd
Source1: shadow
Source2: group
Source3: fstab
Source10: securetty
Source11: shells
Source12: host.conf
Source13: nsswitch.conf
Source20: protocols
Source21: services
Source22: mime.types
Source30: hosts.allow
Source31: hosts.deny
Source40: inputrc
Obsoletes: setup
Provides: setup
AutoReq: false
BuildRequires: fileutils >= 4.0.27, rpm >= 3.0.6-owl8
BuildArchitectures: noarch
BuildRoot: /override/%name-%version

%define shadow_initial_sha1 953f35a56fbea8d66ca1e458cbd51bc90d1d615b

%description
Initial set of configuration files to be placed into /etc.

%install
rm -rf %buildroot
mkdir -p %buildroot/{etc,var/log}
cd %buildroot
touch etc/motd var/log/lastlog
install -p %_sourcedir/{passwd,shadow,group,fstab} etc/
install -p %_sourcedir/{securetty,shells,host.conf,nsswitch.conf} etc/
install -p %_sourcedir/{protocols,services,mime.types,hosts.{allow,deny}} etc/
install -p %_sourcedir/inputrc etc/
touch etc/{group,passwd,shadow}-
touch etc/{hosts,mtab,resolv.conf}
mkdir etc/sysconfig

%triggerin -- shadow-utils
function pause()
{
	echo
	echo "Install will continue in 10 seconds..."
	sleep 10
}

# Determine whether the current /etc/shadow matches the initial version
# as provided by this package.
if [ -e /etc/shadow.rpmnew -o ! -e /etc/shadow ]; then
	SHADOW_INITIAL=no
elif [ "`sha1sum < /etc/shadow`" = "%shadow_initial_sha1  -" ]; then
	SHADOW_INITIAL=yes
else
	SHADOW_INITIAL=no
fi

# New install?
if [ $SHADOW_INITIAL = yes -a ! -e /etc/tcb -a \
    ! -e /etc/nsswitch.conf.rpmnew ]; then
	echo "No existing password shadowing found, will use /etc/tcb."
	/sbin/tcb_convert && rm /etc/shadow
# Updating an install that uses tcb?
elif [ \( $SHADOW_INITIAL = yes -o ! -e /etc/shadow \) -a -d /etc/tcb ]; then
	echo "OK, already using /etc/tcb."
	rm -f /etc/shadow
# Updating an install that uses shadow?
elif [ $SHADOW_INITIAL = no -a -f /etc/shadow -a ! -e /etc/tcb ]; then
	if [ -e /etc/nsswitch.conf.rpmnew ]; then
		cat << EOF
This system appears to be using /etc/shadow.  Conversion to /etc/tcb
is desired, but /etc/nsswitch.conf appears to have been modified locally
preventing automatic conversion.  You'll need to either convert this
system to /etc/tcb manually or knowingly keep it with /etc/shadow
(which is also non-default with a number of other configuration files).
Please refer to tcb_convert(8) for instructions.
EOF
	else
		cat << EOF
This system appears to be using /etc/shadow and will now be converted
to /etc/tcb.

EOF
		if /sbin/tcb_convert; then
			echo "tcb_convert succeeded"
			if [ "`%_sbindir/control passwd`" != restricted ]; then
				echo "Setting passwd(1) file modes for tcb"
				%_sbindir/control passwd tcb
				ls -l %_bindir/passwd
			fi
			rm -f /etc/shadow.rpmnew
			mv -v /etc/shadow /etc/shadow-pre-tcb
			chmod -v go-rwx /etc/shadow*
			cat << EOF

The old shadow file and any its backups have been left around - be sure
to remove them once you're positive the conversion has succeeded.
EOF
		else
			cat << EOF
tcb_convert FAILED

Your system may be in an inconsistent state now, please perform the
conversion to /etc/tcb manually.  See tcb_convert(8) for instructions.
EOF
		fi
	fi
	pause
# Updating a misconfigured install?
elif [ $SHADOW_INITIAL = no -a -e /etc/shadow -a -e /etc/tcb ]; then
	cat << EOF
This system appears to be misconfigured: both /etc/shadow and /etc/tcb
exist.  It may be in an inconsistent state now, please complete the
conversion to /etc/tcb manually.  See tcb_convert(8) for instructions.
EOF
	pause
# Possible other misconfigurations.
else
	cat << EOF
This system's local user authentication appears to be misconfigured.
You might need to convert it to /etc/tcb manually, see tcb_convert(8)
for instructions.
EOF
	pause
fi

rm -f /etc/{passwd,shadow,group}.rpmnew

%files
%defattr(644,root,root)
%verify(not md5 size mtime) %config(noreplace) /etc/passwd
%verify(not md5 size mtime) %config(noreplace,missingok) %attr(400,root,root) /etc/shadow
%verify(not md5 size mtime) %config(noreplace) /etc/group
%verify(not md5 size mtime) %config(noreplace) /etc/fstab
%config(noreplace) %attr(600,root,root) /etc/securetty
%config(noreplace) /etc/shells
%config(noreplace) /etc/host.conf
%config(noreplace) /etc/nsswitch.conf
%config /etc/protocols
%config /etc/services
%config /etc/mime.types
%config(noreplace) /etc/hosts.allow
%config(noreplace) /etc/hosts.deny
%config /etc/inputrc
%config(noreplace) /etc/motd
%ghost /var/log/lastlog
%ghost /etc/*-
%attr(0644,root,root) %config(noreplace,missingok) %ghost /etc/hosts
%attr(0644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/mtab
%attr(0644,root,root) %config(noreplace) %ghost /etc/resolv.conf
%dir %attr(755,root,root) /etc/sysconfig

%changelog
* Mon Feb 07 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 1.0-owl2
- Added "usbfs" entry in fstab (for lsusb).

* Tue Feb 01 2011 Solar Designer <solar-at-owl.openwall.com> 1.0-owl1
- Added group _icmp.

* Mon Jul 26 2010 Solar Designer <solar-at-owl.openwall.com> 0.34-owl1
- Added default fstab lines for tmpfs and for sysfs (the latter with noauto).

* Tue Mar 30 2010 Solar Designer <solar-at-owl.openwall.com> 0.33-owl1
- Moved profile, bashrc, csh.login, and csh.cshrc from owl-etc to the bash and
tcsh packages as appropriate.
- Moved profile.d to owl-hier.

* Mon Jan 25 2010 Solar Designer <solar-at-owl.openwall.com> 0.32-owl1
- Added /etc/mime.types (from Apache httpd 2.2.14 with minor changes).

* Tue Jan 08 2008 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.31-owl3
- Removed %%ghost attribute from /etc/mtab file.

* Thu Mar 30 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 0.31-owl2
- A minor change to include ghost files (/etc/hosts, /etc/mtab, and
/etc/resolv.conf).
- Added /etc/sysconfig directory, since it was orphaned.

* Wed Oct 19 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 0.31-owl1
- Changed 'xntpd' in passwd/group to 'ntpd'.

* Sat Sep 24 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.30-owl1
- named user/group.

* Fri Jan 14 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 0.29-owl3
- Let RPM know that /etc/shadow may be missing.
- Include /etc/{group,passwd,shadow}- (backup copies - with the trailing
"minus") into this package as "ghosts".

* Tue Nov 02 2004 Solar Designer <solar-at-owl.openwall.com> 0.29-owl2
- Do install all sources explicitly (and do not pick anything else which
might happen to be in RPM's source dir).

* Sun Oct 26 2003 Solar Designer <solar-at-owl.openwall.com> 0.29-owl1
- nmap user/group.

* Tue Sep 09 2003 Solar Designer <solar-at-owl.openwall.com> 0.28-owl1
- dhcp user/group.

* Thu May 29 2003 Solar Designer <solar-at-owl.openwall.com> 0.27-owl1
- tcb is now the default and automatic conversion to it is attempted.

* Tue May 27 2003 Solar Designer <solar-at-owl.openwall.com> 0.26-owl1
- When updating an install that uses tcb, don't install the initial
/etc/shadow (rm it on a trigger).
- Don't install /etc/{passwd,shadow,group}.rpmnew files (rm -f them),
the post-install scripts of our other packages take care of creating
any additional pseudo-users.

* Fri May 23 2003 Solar Designer <solar-at-owl.openwall.com> 0.25-owl1
- Moved /etc/nsswitch.conf from glibc to owl-etc package.

* Tue Apr 15 2003 Solar Designer <solar-at-owl.openwall.com> 0.24-owl1
- Added /usr/local/sbin to the default PATH.

* Thu Aug 22 2002 Solar Designer <solar-at-owl.openwall.com> 0.23-owl2
- Made more files noreplace.

* Sun Jun 23 2002 Solar Designer <solar-at-owl.openwall.com>
- sshd user/group.

* Sun May 19 2002 Solar Designer <solar-at-owl.openwall.com>
- screen group.

* Wed Feb 06 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Sun Dec 16 2001 Solar Designer <solar-at-owl.openwall.com>
- vsftpd user/group.

* Sun Nov 25 2001 Solar Designer <solar-at-owl.openwall.com>
- telnetd user/group.
- auth group.

* Thu Nov 01 2001 Solar Designer <solar-at-owl.openwall.com>
- audio, video and radio groups to manage access to devices.

* Wed Oct 10 2001 Solar Designer <solar-at-owl.openwall.com>
- Use "proc" and "devpts" as fstab keywords for /proc and /dev/pts as
"none" could cause confusing messages from umount(8).

* Mon Oct 08 2001 Solar Designer <solar-at-owl.openwall.com>
- syslogd user/group.

* Sat Jul 28 2001 Solar Designer <solar-at-owl.openwall.com>
- Corrected the use of *'s and x's in the default passwd.

* Thu Jul 12 2001 Solar Designer <solar-at-owl.openwall.com>
- xntpd user/group.
- scanlogd user/group.

* Wed Mar 28 2001 Solar Designer <solar-at-owl.openwall.com>
- Disable coredumps with the soft rlimit only.

* Thu Mar 08 2001 Solar Designer <solar-at-owl.openwall.com>
- chkpwd group.

* Sun Feb 25 2001 Solar Designer <solar-at-owl.openwall.com>
- utempter group.

* Sat Feb 10 2001 Solar Designer <solar-at-owl.openwall.com>
- shadow group.

* Mon Feb 05 2001 Solar Designer <solar-at-owl.openwall.com>
- Add /usr/X11R6/bin to the default PATH when applicable.
- Changed the default csh prompts to be the same as they are with bash.
- Mention that /etc/profile.d/local.* is the place for local additions.
- No longer disable bash history by default.
- Source /etc/bashrc from /etc/profile unless ~/.bashrc exists.

* Wed Jan 31 2001 Solar Designer <solar-at-owl.openwall.com>
- Changed some more pseudo-user home directories to / to avoid certain
attacks via group write permissions.

* Fri Jan 26 2001 Solar Designer <solar-at-owl.openwall.com>
- Install /etc/fstab world-readable as it is used by sysconf(3) in glibc
to find the mount point of procfs (which sounds broken enough for me).

* Thu Jan 18 2001 Solar Designer <solar-at-owl.openwall.com>
- Don't expire the initial (disabled) password of root and the pseudo-users.

* Wed Dec 20 2000 Solar Designer <solar-at-owl.openwall.com>
- Obsoletes: setup (yes, we can upgrade to this from RH).
- Provide default hosts.allow and hosts.deny with useful comments.
- Provide /var/log/lastlog as a ghost just so that it doesn't get removed
when upgrading from Red Hat's "setup" package; the actual file is created
by owl-startup.

* Sat Dec 16 2000 Solar Designer <solar-at-owl.openwall.com>
- Provide initial fstab here.
- proc group.

* Mon Dec 11 2000 Solar Designer <solar-at-owl.openwall.com>
- Conflicts: setup

* Wed Dec 06 2000 Solar Designer <solar-at-owl.openwall.com>
- popa3d user/group.

* Mon Dec 04 2000 Solar Designer <solar-at-owl.openwall.com>
- utmp group.
- Keep the initial shadow file here rather than use pwconv.

* Tue Nov 21 2000 Solar Designer <solar-at-owl.openwall.com>
- More pseudo-users/groups: klogd, postfix, postdrop, postman.

* Sun Aug 20 2000 Solar Designer <solar-at-owl.openwall.com>
- crontab user/group.

* Thu Jul 27 2000 Solar Designer <solar-at-owl.openwall.com>
- Initial version.
