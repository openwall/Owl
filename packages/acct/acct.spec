# $Id: Owl/packages/acct/acct.spec,v 1.7 2001/04/11 20:44:08 mci Exp $

Summary: Utilities for monitoring process activities.
Name: acct
Version: 6.3.5
Release: 4owl
Copyright: GPL
Group: Applications/System
Source0: ftp://ftp.red-bean.com/pub/noel/%{name}-%{version}.tar.gz
Source1: dump-acct.8
Source2: dump-utmp.8
Source3: acct.logrotate
Source4: acct.init
Provides: psacct
Obsoletes: psacct
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Prereq: /sbin/install-info

%description
The acct package contains several utilities for monitoring process
activities, including ac, lastcomm, accton and sa.  The ac command
displays statistics about how long users have been logged on.  The
lastcomm command displays information about previous executed commands.
The accton command turns process accounting on or off.  The sa command
summarizes information about previously executed commands.

Install the acct package if you'd like to use its utilities for
monitoring process activities on your system.

%prep
%setup -q

%build
autoconf
%configure
sed -e "s/\/\* #undef HAVE_LINUX_ACCT_H \*\//#define HAVE_LINUX_ACCT_H/" config.h > config.h.new
mv -f config.h.new config.h
touch texinfo.tex
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{/etc/{rc.d/init.d,logrotate.d},/sbin,%{_bindir},%{_mandir},%{_sbindir},%{_var}/account}
%{makeinstall}
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_mandir}/man8/
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_mandir}/man8/
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/acct
install -m 755 %{SOURCE4} $RPM_BUILD_ROOT/etc/rc.d/init.d/acct

# move accton to /sbin -- leave historical symlink
mv $RPM_BUILD_ROOT%{_sbindir}/accton $RPM_BUILD_ROOT/sbin/accton
ln -s ../../sbin/accton $RPM_BUILD_ROOT%{_sbindir}/accton

# Because of the last command conflicting with the one from SysVinit
mv $RPM_BUILD_ROOT/usr/bin/last $RPM_BUILD_ROOT/usr/bin/last-acct
mv $RPM_BUILD_ROOT%{_mandir}/man1/last.1 $RPM_BUILD_ROOT%{_mandir}/man1/last-acct.1

touch $RPM_BUILD_ROOT%{_var}/account/pacct
touch $RPM_BUILD_ROOT%{_var}/account/usracct
touch $RPM_BUILD_ROOT%{_var}/account/savacct

%clean
rm -rf $RPM_BUILD_ROOT

%post
# we need this hack to get rid of an old, incorrect accounting info entry.
grep -v '* accounting: (psacct)' < /etc/info-dir > /etc/info-dir.new
mv -f /etc/info-dir.new /etc/info-dir
/sbin/install-info %{_infodir}/accounting.info.gz %{_infodir}/dir --entry="* accounting: (accounting).            The GNU Process Accounting Suite."

for f in %{_var}/account/{pacct,usracct,savacct}; do
	test -e $f && continue || :
	touch $f
	chown root.root $f
	chmod 600 $f
done

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/accounting.info.gz %{_infodir}/dir --entry="* accounting: (accounting).            The GNU Process Accounting Suite."
fi

%files
%defattr(-,root,root)
%dir /var/account
%ghost %attr(0600,root,root) /var/account/pacct
%ghost %attr(0600,root,root) /var/account/usracct
%ghost %attr(0600,root,root) /var/account/savacct
%attr(0644,root,root) %config(noreplace) /etc/logrotate.d/*
%config /etc/rc.d/init.d/acct
/sbin/accton
%{_sbindir}/*
%{_bindir}/*
%{_mandir}/*/*
%{_infodir}/*

%changelog
* Wed Apr 11 2001 Michail Litvak <mci@owl.openwall.com>
- added chkconfig support in init script
- improved logrotate config
- more cleanups...

* Mon Apr 08 2001 Michail Litvak <mci@owl.openwall.com>
- spec cleanups
- acct.logrotate and acct.init was rewritten
- Obsoletes: psacct
- Use %ghost for /var/account/*

* Mon Apr 02 2001 Michail Litvak <mci@owl.openwall.com>
- Imported spec from RH (some parts from Mandrake)
- update to 6.3.5, fixed source location
- dump-acct, dump-utmp manpages from Debian
