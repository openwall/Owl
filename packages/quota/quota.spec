# $Id: Owl/packages/quota/quota.spec,v 1.19 2004/09/10 07:29:20 galaxy Exp $

Summary: System administration tools for monitoring users' disk usage.
Name: quota
Version: 3.11
Release: owl1
License: BSD
Group: System Environment/Base
Source: http://prdownloads.sourceforge.net/linuxquota/quota-3.11.tar.gz
Patch0: quota-3.11-alt-bad-kernel-includes.diff
Patch1: quota-3.11-owl-man.diff
Patch2: quota-3.11-owl-tmp.diff
Patch3: quota-3.11-owl-vitmp.diff
Patch4: quota-3.11-rh-no-strip.diff
BuildRequires: e2fsprogs-devel
BuildRoot: /override/%name-%version

%description
The quota package contains system administration tools for monitoring
and limiting users' and or groups' disk usage, per filesystem.

%prep
%setup -q -n quota-tools
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
# XXX: really don't build rpc daemon
%configure --enable-rpc=no
make

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT{%_bindir,/sbin,%_sbindir,%_mandir/man{1,2,3,8}}

%makeinstall

# Move some utilities to traditional place.
mv $RPM_BUILD_ROOT%_sbindir/{convertquota,quotaon,quotaoff,quotacheck} \
	$RPM_BUILD_ROOT/sbin/

chmod -R u+w $RPM_BUILD_ROOT/

# XXX: (GM): Remove unpackaged files (check later)
rm %buildroot/etc/quotagrpadmins
rm %buildroot/etc/quotatab
rm %buildroot/etc/warnquota.conf
rm %buildroot%_includedir/rpcsvc/rquota.h
rm %buildroot%_includedir/rpcsvc/rquota.x
rm %buildroot%_datadir/locale/pl/LC_MESSAGES/quota.mo

%files
%defattr(-,root,root)
%doc doc/quotas.preformated
%doc Changelog
%doc warnquota.conf quotagrpadmins quotatab
/sbin/*
%_bindir/*
%_sbindir/*
%_mandir/man?/*

%changelog
* Sat Feb 28 2004 Michail Litvak <mci@owl.openwall.com> 3.11-owl1
- 3.11
- Regenerated patches, add patches from Alt and RH.

* Thu Apr 25 2002 Solar Designer <solar@owl.openwall.com> 2.00-owl8
- vitmp has been moved to /bin.

* Sun Apr 21 2002 Solar Designer <solar@owl.openwall.com>
- Use /usr/libexec/vitmp in edquota(8).

* Tue Feb 05 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Fri Jul 06 2001 Solar Designer <solar@owl.openwall.com>
- New release number for upgrades after building against glibc >= 2.1.3-17owl
which includes corrected declaration of struct dqstats in <sys/quota.h>.

* Sun Jul 01 2001 Michail Litvak <mci@owl.openwall.com>
- pack only *.html in doc/
- man pages fixes
- added TMPDIR support to edquota
- put warnquota.conf in doc

* Wed Jun 27 2001 Michail Litvak <mci@owl.openwall.com>
- more fixes in mans and docs
- patch to catch error from mkstemp
- include doc/ subdir into package

* Mon Jun 25 2001 Michail Litvak <mci@owl.openwall.com>
- some spec cleanups
- patch to allow building to non-root user

* Sun Jun 24 2001 Michail Litvak <mci@owl.openwall.com>
- Imported from RH
- man patch from PLD
