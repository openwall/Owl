# $Owl: Owl/packages/vsftpd/vsftpd.spec,v 1.39 2011/03/02 08:25:33 solar Exp $

Summary: File Transfer Protocol (FTP) server.
Name: vsftpd
Version: 2.3.4
Release: owl1
License: GPL
Group: System Environment/Daemons
URL: http://vsftpd.beasts.org
Source0: ftp://vsftpd.beasts.org/users/cevans/vsftpd-%version.tar.gz
# Signature: ftp://vsftpd.beasts.org/users/cevans/vsftpd-%version.tar.gz.asc
Source1: vsftpd.eps.gz
Source2: vsftpd.pam
Source3: vsftpd.xinetd
Source4: vsftpd.logrotate
Patch0: vsftpd-2.2.2-owl-warnings.diff
Patch1: vsftpd-2.2.2-owl-pam_userpass.diff
Patch2: vsftpd-2.2.1-owl-alt-defaults.diff
Patch3: vsftpd-2.2.0-owl-man.diff
Requires: logrotate, pam >= 0:0.80-owl2, pam_userpass, tcb, xinetd, /var/empty
Provides: ftpserver
BuildRequires: pam-devel, pam_userpass-devel, libcap-devel
BuildRoot: /override/%name-%version

%description
vsftpd is a File Transfer Protocol (FTP) server.  The "vs" stands for
Very Secure.  Obviously this is not a guarantee, but a reflection that
the entire codebase has been written with security in mind, and the
program has been carefully designed to be resilient to attack.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
install -p -m 644 %_sourcedir/vsftpd.eps.gz .
bzip2 -9 Changelog

%build
make CFLAGS="%optflags -Wall -W -Wshadow" LIBS="-lcap -lpam -lpam_userpass"

%install
rm -rf %buildroot
mkdir -p %buildroot/{usr/sbin,etc/{pam.d,xinetd.d,logrotate.d}}
mkdir -p %buildroot%_mandir/man{5,8}
install -m 700 vsftpd %buildroot/usr/sbin/
install -m 600 vsftpd.conf %buildroot/etc/
install -m 644 vsftpd.conf.5 %buildroot%_mandir/man5/
install -m 644 vsftpd.8 %buildroot%_mandir/man8/
cd %_sourcedir
install -m 600 vsftpd.pam %buildroot/etc/pam.d/vsftpd
install -m 600 vsftpd.xinetd %buildroot/etc/xinetd.d/vsftpd
install -m 600 vsftpd.logrotate %buildroot/etc/logrotate.d/vsftpd
touch %buildroot/etc/ftpusers

%pre
grep -q ^vsftpd: /etc/group || groupadd -g 187 vsftpd
grep -q ^vsftpd: /etc/passwd ||
	useradd -g vsftpd -u 187 -d / -s /bin/false -M vsftpd
set noclobber
test -e /etc/ftpusers || echo root > /etc/ftpusers
chmod 600 /etc/ftpusers
mkdir -m 755 /home/ftp &> /dev/null || :

%files
%defattr(-,root,root)
%doc COPYING FAQ LICENSE README
%doc README.security REWARD SECURITY/
%doc BENCHMARKS SPEED TUNING
%doc BUGS TODO
%doc REFS
%doc EXAMPLE/
%doc Changelog.bz2
%doc vsftpd.eps.gz
# Not included on purpose: AUDIT INSTALL README.ssl SIZE
/usr/sbin/vsftpd
%config(noreplace) /etc/vsftpd.conf
%config(noreplace) /etc/pam.d/vsftpd
%config(noreplace) /etc/xinetd.d/vsftpd
%config(noreplace) /etc/logrotate.d/vsftpd
%ghost %config %attr(0600,root,root) /etc/ftpusers
%_mandir/man5/vsftpd.conf.5*
%_mandir/man8/vsftpd.8*

%changelog
* Wed Mar 02 2011 Solar Designer <solar-at-owl.openwall.com> 2.3.4-owl1
- Updated to 2.3.4.

* Mon Aug 30 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 2.3.2-owl1
- Updated to 2.3.2.

* Wed Nov 18 2009 Solar Designer <solar-at-owl.openwall.com> 2.2.2-owl1
- Updated to 2.2.2.

* Wed Nov 11 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.2.1-owl3
- Fixed regression in LFS support by activating LFS early.

* Tue Oct 27 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.2.1-owl2
- Made fixes for compilation warnings more portable.

* Sat Oct 24 2009 Solar Designer <solar-at-owl.openwall.com> 2.2.1-owl1
- Updated to 2.2.1.

* Tue Sep 22 2009 Solar Designer <solar-at-owl.openwall.com> 2.2.0-owl1
- Updated to 2.2.0 release.
- Fixed a couple of async signal safety issues in sysutil.c.

* Sun Jul 19 2009 Solar Designer <solar-at-owl.openwall.com> 2.2.0-owl0.2
- Re-wrote the config file comment on "listen" and "listen_ipv6" to recommend
the command line rather than a config file for overriding these options.
- Modified the vsftpd(8) man page to recommend the command line rather than a
config file for overriding "listen", with a related change to the example.
- In the default xinetd config file, also set "-olisten_ipv6=NO" (in addition
to "-olisten=NO").
- Corrected a newly introduced pam_get_item() call in sysdeputil.c not to
break C strict aliasing rules.

* Sat Jul 18 2009 Michail Litvak <mci-at-owl.openwall.com> 2.2.0-owl0.1
- Updated to 2.2.0pre4.
- Regenerated patches, dropped those for which equivalent functionality got
implemented upstream.

* Fri May 29 2009 Solar Designer <solar-at-owl.openwall.com> 2.1.1-owl2
- Re-worked the command-line options patch, allowing to specify multiple
"-o" options (like it can be done with ssh/sshd) and multiple config files,
and documenting this enhanced command-line syntax in the man page.
- Reverted the listen=... default to NO (same as in 2.0.6-owl1; the
previous two revisions of our package were never made public), overriding
upstream's change of default.
- Package the REFS documentation file (references to relevant RFCs).

* Thu May 28 2009 Michail Litvak <mci-at-owl.openwall.com> 2.1.1-owl1
- Updated to 2.1.1.
- Added a patch to support the new option "-o", which can be used to
specify configuration settings via the command line.
- Changed the xinetd config file to enable the inetd mode explicitly.

* Wed May 27 2009 Michail Litvak <mci-at-owl.openwall.com> 2.1.1-owl0.1
- Updated to 2.1.1pre1.

* Mon Jun 23 2008 Michail Litvak <mci-at-owl.openwall.com> 2.0.6-owl1
- Updated to 2.0.6.
- Regenerated patches.

* Tue Jun 06 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.0.4-owl1
- Updated to 2.0.4.
- Deal with compilation warnings generated by new gcc compiler.

* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.0.3-owl2
- Compressed Changelog file.

* Sun Nov 27 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.0.3-owl1
- Updated to 2.0.3.
- Fixed the problem with timezone in chroot.

* Sat Oct 29 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.2.1-owl0.3
- Changed PAM config file to include system-auth for PAM account and
session management.
- Stripped /lib/security/ prefix from PAM module names.

* Sat Jun 19 2004 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.2.1-owl0.2
- vsftpd.conf(5): note that session_support is disabled by default.
- vsftpd.pam: set proper session management entry.

* Sun Oct 26 2003 Solar Designer <solar-at-owl.openwall.com> 1.2.1-owl0.1
- Updated to 1.2.1pre1.
- Let vsftpd use libcap now that we package it.
- Package the control flow diagram from our presentation slides; the dia
source to vsftpd.eps is available through the download link from
http://www.openwall.com/presentations/Owl/

* Thu Apr 17 2003 Solar Designer <solar-at-owl.openwall.com> 1.0.2-owl0.3
- Pass prefix= and count= to pam_tcb also for authentication such that it
can use this information to reduce timing leaks.

* Thu Apr 03 2003 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.0.2-owl0.2
- Updated pam_userpass support: build with libpam_userpass.

* Tue Apr 02 2002 Solar Designer <solar-at-owl.openwall.com>
- Updated to 1.0.2pre3.
- Set hide_ids to YES.

* Sat Feb 02 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Sun Dec 16 2001 Solar Designer <solar-at-owl.openwall.com>
- Adjusted the default tunable settings, based some on those from ALT Linux.
- Patched in pam_userpass support.
- Wrote PAM and xinetd configuration files.
- Took vsftpd.logrotate from the ALT Linux package.
- Based this spec file on Seth Vidal's with heavy modifications.
