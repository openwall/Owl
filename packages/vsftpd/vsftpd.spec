# $Id: Owl/packages/vsftpd/vsftpd.spec,v 1.11 2003/12/15 11:35:40 solar Exp $

Summary: File Transfer Protocol (FTP) server.
Name: vsftpd
Version: 1.2.1
Release: owl0.1
License: GPL
Group: System Environment/Daemons
URL: http://vsftpd.beasts.org
# The primary site for releases is ftp://ferret.lmh.ox.ac.uk/pub/linux/
Source0: ftp://ftp.beasts.org/users/cevans/vsftpd-%{version}pre1.tar.gz
Source1: vsftpd.eps.gz
Source2: vsftpd.pam
Source3: vsftpd.xinetd
Source4: vsftpd.logrotate
Patch0: vsftpd-1.2.1pre1-owl-alt-defaults.diff
Patch1: vsftpd-1.2.1pre1-owl-pam_userpass.diff
Patch2: vsftpd-1.2.1pre1-owl-warnings.diff
Requires: xinetd, logrotate, pam_userpass, tcb, /var/empty
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
install -p -m 644 $RPM_SOURCE_DIR/vsftpd.eps.gz .

%build
make CFLAGS="$RPM_OPT_FLAGS -Wall" LIBS="-lcap -lpam -lpam_userpass"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{usr/sbin,etc/{pam.d,xinetd.d,logrotate.d}}
mkdir -p $RPM_BUILD_ROOT%_mandir/man{5,8}
install -m 700 vsftpd $RPM_BUILD_ROOT/usr/sbin/
install -m 600 vsftpd.conf $RPM_BUILD_ROOT/etc/
install -m 644 vsftpd.conf.5 $RPM_BUILD_ROOT%_mandir/man5/
install -m 644 vsftpd.8 $RPM_BUILD_ROOT%_mandir/man8/
cd $RPM_SOURCE_DIR
install -m 600 vsftpd.pam $RPM_BUILD_ROOT/etc/pam.d/vsftpd
install -m 600 vsftpd.xinetd $RPM_BUILD_ROOT/etc/xinetd.d/vsftpd
install -m 600 vsftpd.logrotate $RPM_BUILD_ROOT/etc/logrotate.d/vsftpd
touch $RPM_BUILD_ROOT/etc/ftpusers

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
%doc README FAQ LICENSE COPYING
%doc README.security REWARD SECURITY/
%doc BENCHMARKS SPEED TUNING
%doc BUGS TODO
%doc EXAMPLE/
%doc Changelog
%doc vsftpd.eps.gz
/usr/sbin/vsftpd
%config(noreplace) /etc/vsftpd.conf
%config(noreplace) /etc/pam.d/vsftpd
%config(noreplace) /etc/xinetd.d/vsftpd
%config(noreplace) /etc/logrotate.d/vsftpd
%ghost %config %attr(0600,root,root) /etc/ftpusers
%_mandir/man5/vsftpd.conf.5*
%_mandir/man8/vsftpd.8*

%changelog
* Sun Oct 26 2003 Solar Designer <solar@owl.openwall.com> 1.2.1-owl0.1
- Updated to 1.2.1pre1.
- Let vsftpd use libcap now that we package it.
- Package the control flow diagram from our presentation slides; the dia
source to vsftpd.eps is available through the download link from
http://www.openwall.com/presentations/Owl/

* Thu Apr 17 2003 Solar Designer <solar@owl.openwall.com> 1.0.2-owl0.3
- Pass prefix= and count= to pam_tcb also for authentication such that it
can use this information to reduce timing leaks.

* Thu Apr 03 2003 Dmitry V. Levin <ldv@owl.openwall.com> 1.0.2-owl0.2
- Updated pam_userpass support: build with libpam_userpass.

* Tue Apr 02 2002 Solar Designer <solar@owl.openwall.com>
- Updated to 1.0.2pre3.
- Set hide_ids to YES.

* Sat Feb 02 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Sun Dec 16 2001 Solar Designer <solar@owl.openwall.com>
- Adjusted the default tunable settings, based some on those from ALT Linux.
- Patched in pam_userpass support.
- Wrote PAM and xinetd configuration files.
- Took vsftpd.logrotate from the ALT Linux package.
- Based this spec file on Seth Vidal's with heavy modifications.
