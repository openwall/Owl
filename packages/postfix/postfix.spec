# $Id: Owl/packages/postfix/postfix.spec,v 1.19 2003/10/30 21:15:47 solar Exp $

Summary: Postfix mail system.
Name: postfix
%define original_date 19991231
%define original_pl pl13
%define original_version %original_date-%original_pl
%define package_version %{original_date}_%original_pl
Version: %package_version
Release: owl7
License: IBM Public License
Group: System Environment/Daemons
Source0: ftp://ftp.sunet.se/pub/unix/mail/postfix/official/%name-%original_version.tar.gz
Source1: aliases
Source2: postfix.init
Source3: postfix.control
Patch0: postfix-19991231-pl10-owl-classless.diff
Patch1: postfix-19991231-pl10-owl-sparse-hack.diff
Patch2: postfix-19991231-pl13-snapshot-20011217-safe-opens.diff
Patch3: postfix-19991231-pl13-owl-locking.diff
Patch4: postfix-19991231-pl13-owl-postalias-no-hostname.diff
Patch10: postfix-19991231-pl13-owl-postfix-script.diff
Patch20: postfix-19991231-pl10-owl-INSTALL.diff
Patch21: postfix-19991231-pl10-owl-config.diff
PreReq: /sbin/chkconfig, grep, shadow-utils
Requires: owl-control >= 0.4, owl-control < 2.0
Conflicts: sendmail, qmail
Provides: MTA, smtpd, smtpdaemon
Obsoletes: sendmail-cf, sendmail-doc
BuildRoot: /override/%name-%version

%description
Postfix is Wietse Venema's attempt to provide an alternative to the
widely-used Sendmail program.  Postfix attempts to be fast, easy to
administer, and hopefully secure, while at the same time being sendmail
compatible enough to not upset your users.

%prep
%setup -q -n %name-%original_version
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch10 -p1
%patch20 -p1
%patch21 -p1

%build
make OPT="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT

yes '' | {
	function chowngrp()
	{
		local list mode

		list=$1
		shift
		mode=$1
		while shift; do
			echo "$1 $mode" |
			sed -n "s,^$RPM_BUILD_ROOT,,p" >> $list
		done
	}

	function chown()
	{
		chowngrp filelist.user $*
	}

	function chgrp()
	{
		chowngrp filelist.group $*
	}

	rm -f filelist.* flag.*
	. INSTALL.sh
	touch flag.$?
}

test -f flag.0

pushd $RPM_BUILD_ROOT

rm etc/postfix/{install.cf,postfix-script-{diff,*sgid}}

install -m 644 $RPM_SOURCE_DIR/aliases etc/postfix/
ln -s postfix/aliases{,.db} etc/

mkdir -p etc/rc.d/init.d
install -m 700 $RPM_SOURCE_DIR/postfix.init etc/rc.d/init.d/postfix

mkdir -p etc/control.d/facilities
install -m 700 $RPM_SOURCE_DIR/postfix.control etc/control.d/facilities/postfix

mkdir -p usr/lib
ln -s ../sbin/sendmail usr/lib/sendmail

# Shorten the symlinks
rm usr/bin/{mailq,newaliases}
ln -s ../sbin/sendmail usr/bin/mailq
ln -s ../sbin/sendmail usr/bin/newaliases

chmod go-r usr/sbin/postdrop

popd

cat > filelist << EOF
%defattr (-,root,root)
%doc 0README BEWARE COMPATIBILITY DEBUG_README HISTORY LICENSE RELEASE_NOTES
%doc RESTRICTION_CLASS TODO UUCP_README
%doc examples html
EOF

cat filelist.{user,group} | sed 's/ .*$//' | sort -u > filelist.plain

while read filename; do
	test -e ${RPM_BUILD_ROOT}${filename}
	user="`sed -n "s,^$filename \(.*\)\$,\1,p" < filelist.user`"
	test -n "$user" || user=root
	group="`sed -n "s,^$filename \(.*\)\$,\1,p" < filelist.group`"
	test -n "$group" || group=root
	if [ -d ${RPM_BUILD_ROOT}${filename} ]; then
		echo "%dir %attr(-,$user,$group) $filename"
	else
		echo "%attr(-,$user,$group) $filename"
	fi
done < filelist.plain >> filelist

find $RPM_BUILD_ROOT -type d |
	sed "s,^$RPM_BUILD_ROOT,," |
	sort |
	comm -23 - filelist.plain |
	grep '/postfix$' |
	sed 's,^,%dir ,' >> filelist

find $RPM_BUILD_ROOT ! -type d |
	sed "s,^$RPM_BUILD_ROOT,," |
	sort |
	comm -23 - filelist.plain |
	sed -e 's,^/etc,%config &,' -e 's,/usr/man/.*$,&*,' >> filelist

%pre
grep -q ^postdrop: /etc/group || groupadd -g 161 postdrop
grep -q ^postdrop: /etc/passwd ||
	useradd -g postdrop -u 161 -d / -s /bin/false -M postdrop
grep -q ^postfix: /etc/group || groupadd -g 182 postfix
grep -q ^postfix: /etc/passwd ||
	useradd -g postfix -u 182 -d / -s /bin/false -M postfix
grep -q ^postman: /etc/group || groupadd -g 183 postman
grep -q ^postman: /etc/passwd ||
	useradd -g postman -u 183 -d / -s /bin/false -M postman
rm -f /var/run/postfix.restart
if [ $1 -ge 2 ]; then
	/usr/sbin/postfix stop && touch /var/run/postfix.restart || :
	/usr/sbin/control-dump postfix
fi

%post
/usr/sbin/postalias /etc/postfix/aliases
/usr/sbin/postfix check
if [ $1 -ge 2 ]; then
	/usr/sbin/control-restore postfix
fi
/sbin/chkconfig --add postfix
test -f /var/run/postfix.restart && /usr/sbin/postfix start || :
rm -f /var/run/postfix.restart
if [ "`/usr/sbin/control postfix`" = local ]; then
	echo -n "SMTP server not enabled by default, use "
	echo "\"control postfix server\" to enable"
fi

%preun
if [ $1 -eq 0 ]; then
	/usr/sbin/postfix stop || :
	/sbin/chkconfig --del postfix
	sleep 1
	/usr/sbin/postfix drain &> /dev/null || :
	rm -f /etc/postfix/aliases.db
	find /var/spool/postfix \( -type p -o -type s \) -delete
	rm -f /var/spool/postfix/{pid,etc,lib}/*
	rmdir /var/spool/postfix/[^m]*
fi

%files -f filelist

%changelog
* Fri Oct 24 2003 Solar Designer <solar@owl.openwall.com> 19991231_pl13-owl7
- Explain how to enable the SMTP server with control(8).

* Wed Oct 22 2003 Solar Designer <solar@owl.openwall.com> 19991231_pl13-owl6
- Hack: in postalias, don't set YP_MASTER_NAME as that would leak the
hostname when doing chrooted installs for other systems.

* Sun Nov 03 2002 Solar Designer <solar@owl.openwall.com> 19991231_pl13-owl5
- Dump/restore the owl-control setting for SMTP server on package upgrades.

* Sun Oct 13 2002 Solar Designer <solar@owl.openwall.com>
- Use fcntl locking, not flock.

* Tue Sep 03 2002 Solar Designer <solar@owl.openwall.com>
- Conflicts: qmail

* Sun Jul 07 2002 Solar Designer <solar@owl.openwall.com>
- Use grep -q in %pre.

* Thu Feb 07 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Wed Dec 26 2001 Solar Designer <solar@owl.openwall.com>
- Additional postfix-script fail-closeness.

* Sat Dec 22 2001 Solar Designer <solar@owl.openwall.com>
- Hardening of the Postfix queue file permissions and access methods,
in case someone compromises the postfix account.  The fixes are by
Wietse Venema and have been back-ported from the 20011217 snapshot.
Thanks to Michael Tokarev for his help in handling these issues.
- Updated to 19991231-pl13.

* Sun Mar 18 2001 Solar Designer <solar@owl.openwall.com>
- Fixed a copy/paste bug in the restart script.

* Sun Dec 24 2000 Solar Designer <solar@owl.openwall.com>
- Obsoletes: sendmail-cf, sendmail-doc

* Mon Dec 04 2000 Solar Designer <solar@owl.openwall.com>
- Ignore missing source files when updating the chroot jail (this may
happen during system installation).

* Fri Dec 01 2000 Solar Designer <solar@owl.openwall.com>
- Simplified postfix.init for use with owl-startup.
- Restart on package upgrades.

* Wed Nov 22 2000 Solar Designer <solar@owl.openwall.com>
- Restrict relaying to the host's own addresses only by default.
- Ignore sparse .forward files on filesystems which allow for this.
- /var/spool/postfix/pid/ is now only writable by root.
- Run whatever possible chroot'ed (many of the processes keep root
privileges in their real and/or saved IDs and pseudo-user postfix
is shared with non-chroot'ed processes, so this is breakable).
- Wrote postfix.control to enable/disable the SMTP server.

* Tue Nov 21 2000 Solar Designer <solar@owl.openwall.com>
- Wrote this spec file.
- Took postfix.init from Simon J Mudd's package with minor changes.
- SMTP server is now disabled by default.
