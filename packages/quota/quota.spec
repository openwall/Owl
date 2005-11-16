# $Owl: Owl/packages/quota/quota.spec,v 1.25 2005/11/16 13:31:51 solar Exp $

Summary: System administration tools for monitoring users' disk usage.
Name: quota
Version: 3.13
Release: owl1
License: BSD
Group: System Environment/Base
URL: http://sourceforge.net/projects/linuxquota/
Source: http://prdownloads.sourceforge.net/linuxquota/quota-%version.tar.gz
Patch0: quota-3.11-alt-bad-kernel-includes.diff
Patch1: quota-3.11-owl-man.diff
Patch2: quota-3.11-owl-tmp.diff
Patch3: quota-3.11-owl-vitmp.diff
Patch4: quota-3.11-rh-no-strip.diff
Patch5: quota-3.13-mdk-alt-warnquota.diff
Patch6: quota-3.13-alt-getprivs.diff
Patch7: quota-3.13-alt-get_loop_device_name.diff
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
%patch5 -p1
%patch6 -p1
%patch7 -p1

%{expand:%%define optflags %optflags -Wall}

%build
# XXX: really don't build rpc daemon
%configure --enable-rpc=no --enable-rootsbin
%__make CC="%__cc" CPP="%__cpp"
bzip2 -9fk Changelog

%install
rm -rf %buildroot

mkdir -p %buildroot{%_bindir,/sbin,%_sbindir,%_mandir/man{1,2,3,8}}

%__make install ROOTDIR=%buildroot
chmod -R u+w %buildroot/
ln -s quotaon.8.gz %buildroot%_mandir/man8/quotaoff.8.gz

# XXX: (GM): Remove unpackaged files (check later)
rm %buildroot/etc/quotagrpadmins
rm %buildroot/etc/quotatab
rm %buildroot/etc/warnquota.conf
rm %buildroot%_includedir/rpcsvc/rquota.h
rm %buildroot%_includedir/rpcsvc/rquota.x
rm %buildroot%_datadir/locale/*/LC_MESSAGES/quota.mo

%files
%defattr(-,root,root)
%doc doc/quotas.preformated
%doc Changelog.bz2
%doc warnquota.conf quotagrpadmins quotatab
/sbin/*
%_bindir/*
%_sbindir/*
%_mandir/man?/*

%changelog
* Sat Nov 12 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 3.13-owl1
- Updated to 3.13.
- Imported few patches from ALT's quota package.

* Tue Jan 11 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 3.11-owl2
- Used %%__cc and %%__cpp macros.

* Sat Feb 28 2004 Michail Litvak <mci-at-owl.openwall.com> 3.11-owl1
- 3.11
- Regenerated patches, add patches from ALT and RH.

* Thu Apr 25 2002 Solar Designer <solar-at-owl.openwall.com> 2.00-owl8
- vitmp has been moved to /bin.

* Sun Apr 21 2002 Solar Designer <solar-at-owl.openwall.com>
- Use /usr/libexec/vitmp in edquota(8).

* Tue Feb 05 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Fri Jul 06 2001 Solar Designer <solar-at-owl.openwall.com>
- New release number for upgrades after building against glibc >= 2.1.3-17owl
which includes corrected declaration of struct dqstats in <sys/quota.h>.

* Sun Jul 01 2001 Michail Litvak <mci-at-owl.openwall.com>
- pack only *.html in doc/
- man pages fixes
- added TMPDIR support to edquota
- put warnquota.conf in doc

* Wed Jun 27 2001 Michail Litvak <mci-at-owl.openwall.com>
- more fixes in mans and docs
- patch to catch error from mkstemp
- include doc/ subdir into package

* Mon Jun 25 2001 Michail Litvak <mci-at-owl.openwall.com>
- some spec cleanups
- patch to allow building to non-root user

* Sun Jun 24 2001 Michail Litvak <mci-at-owl.openwall.com>
- Imported from RH
- man patch from PLD
