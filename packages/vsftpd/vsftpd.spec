# $Id: Owl/packages/vsftpd/vsftpd.spec,v 1.4 2002/02/07 10:07:26 solar Exp $

Summary: File Transfer Protocol (FTP) server.
Name: vsftpd
Version: 1.0.1
Release: owl1
License: GPL
Group: System Environment/Daemons
Source0: ftp://ferret.lmh.ox.ac.uk/pub/linux/%{name}-%{version}.tar.gz
Source1: vsftpd.pam
Source2: vsftpd.xinetd
Source3: vsftpd.logrotate
Patch0: vsftpd-1.0.1-owl-alt-defaults.diff
Patch1: vsftpd-1.0.1-owl-pam_userpass.diff
Patch2: vsftpd-1.0.1-owl-no-libcap.diff
Requires: xinetd, logrotate, pam_userpass, tcb, /var/empty
Provides: ftpserver
BuildRequires: pam-devel
BuildRoot: /override/%{name}-%{version}

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

%build
make CFLAGS="$RPM_OPT_FLAGS -Wall" LIBS="-lpam"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{usr/sbin,etc/{pam.d,xinetd.d,logrotate.d}}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man{5,8}
install -m 700 vsftpd $RPM_BUILD_ROOT/usr/sbin/
install -m 600 vsftpd.conf $RPM_BUILD_ROOT/etc/
install -m 644 vsftpd.conf.5 $RPM_BUILD_ROOT/%{_mandir}/man5/
install -m 644 vsftpd.8 $RPM_BUILD_ROOT/%{_mandir}/man8/
cd $RPM_SOURCE_DIR
install -m 600 vsftpd.pam $RPM_BUILD_ROOT/etc/pam.d/vsftpd
install -m 600 vsftpd.xinetd $RPM_BUILD_ROOT/etc/xinetd.d/vsftpd
install -m 600 vsftpd.logrotate $RPM_BUILD_ROOT/etc/logrotate.d/vsftpd
touch $RPM_BUILD_ROOT/etc/ftpusers

%clean
rm -rf $RPM_BUILD_ROOT

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
%doc README FAQ LICENSE
%doc README.security REWARD SECURITY/
%doc BENCHMARKS SPEED TUNING
%doc BUGS TODO
%doc Changelog
/usr/sbin/vsftpd
%config(noreplace) /etc/vsftpd.conf
%config(noreplace) /etc/pam.d/vsftpd
%config(noreplace) /etc/xinetd.d/vsftpd
%config(noreplace) /etc/logrotate.d/vsftpd
%ghost %config %attr(0600,root,root) /etc/ftpusers
%{_mandir}/man5/vsftpd.conf.5*
%{_mandir}/man8/vsftpd.8*

%changelog
* Sat Feb 02 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Sun Dec 16 2001 Solar Designer <solar@owl.openwall.com>
- Adjusted the default tunable settings, based some on those from ALT Linux.
- Patched in pam_userpass support.
- Wrote PAM and xinetd configuration files.
- Took vsftpd.logrotate from the ALT Linux package.
- Based this spec file on Seth Vidal's with heavy modifications.
