# $Id: Owl/packages/acct/acct.spec,v 1.13 2002/03/23 21:22:27 solar Exp $

Summary: Utilities for monitoring process activities.
Name: acct
Version: 6.3.5
Release: owl8
License: GPL
Group: Applications/System
Source0: ftp://ftp.red-bean.com/pub/noel/%{name}-%{version}.tar.gz
Source1: dump-acct.8
Source2: dump-utmp.8
Source3: acct.init
Source4: acct.logrotate
Patch0: acct-6.3.5-owl-fixes.diff
PreReq: /sbin/install-info
Provides: psacct
Obsoletes: psacct
BuildRoot: /override/%{name}-%{version}

%description
The acct package contains several utilities for monitoring process
activities, including ac, lastcomm, accton and sa.  The ac command
displays statistics about how long users have been logged on.  The
lastcomm command displays information about previous executed commands.
The accton command turns process accounting on or off.  The sa command
summarizes information about previously executed commands.

%prep
%setup -q
rm accounting.info
%patch0 -p1

%build
autoconf
%configure
sed -e 's,/\* #undef HAVE_LINUX_ACCT_H \*/,#define HAVE_LINUX_ACCT_H,' \
	config.h > config.h.new
mv -f config.h.new config.h
touch texinfo.tex
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/{rc.d/init.d,logrotate.d}
mkdir -p $RPM_BUILD_ROOT{/sbin,%{_bindir},%{_sbindir},%{_mandir}}
mkdir -p $RPM_BUILD_ROOT%{_var}/account
%makeinstall
install -m 644 $RPM_SOURCE_DIR/dump-acct.8 $RPM_BUILD_ROOT%{_mandir}/man8/
install -m 644 $RPM_SOURCE_DIR/dump-utmp.8 $RPM_BUILD_ROOT%{_mandir}/man8/
install -m 755 $RPM_SOURCE_DIR/acct.init $RPM_BUILD_ROOT/etc/rc.d/init.d/acct
install -m 644 $RPM_SOURCE_DIR/acct.logrotate \
	$RPM_BUILD_ROOT/etc/logrotate.d/acct

# move accton to /sbin -- leave historical symlink
mv $RPM_BUILD_ROOT%{_sbindir}/accton $RPM_BUILD_ROOT/sbin/accton
ln -s ../../sbin/accton $RPM_BUILD_ROOT%{_sbindir}/accton

# Because of the last command conflicting with the one from SysVinit
mv $RPM_BUILD_ROOT/usr/bin/last $RPM_BUILD_ROOT/usr/bin/last-acct
mv $RPM_BUILD_ROOT%{_mandir}/man1/last.1 \
	$RPM_BUILD_ROOT%{_mandir}/man1/last-acct.1

touch $RPM_BUILD_ROOT%{_var}/account/pacct
touch $RPM_BUILD_ROOT%{_var}/account/usracct
touch $RPM_BUILD_ROOT%{_var}/account/savacct

%clean
rm -rf $RPM_BUILD_ROOT

%post
# We need this hack to get rid of an old, incorrect accounting info entry
# when installing over older versions of Red Hat Linux.
cp -p /etc/info-dir /etc/info-dir.new &&
grep -v '* accounting: (psacct)' < /etc/info-dir > /etc/info-dir.new &&
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
* Sun Mar 24 2002 Solar Designer <solar@owl.openwall.com>
- Heavy documentation corrections and cleanups (both man pages and texinfo).
- Minor spec file cleanups.

* Fri Mar 22 2002 Michail Litvak <mci@owl.openwall.com>
- fix sa to display real time in seconds not cpu seconds,
  also fix man and info pages
- fixes to build with -Wall cleanly

* Thu Jan 24 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Sat Apr 14 2001 Solar Designer <solar@owl.openwall.com>
- Preserve permissions of /etc/info-dir when modifying it in %post.

* Thu Apr 12 2001 Solar Designer <solar@owl.openwall.com>
- acct.logrotate: nocreate (we create the file from the postrotate script).

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
