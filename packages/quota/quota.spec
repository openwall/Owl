# $Id: Owl/packages/quota/quota.spec,v 1.5 2001/06/27 12:39:50 mci Exp $

Name: quota
Summary: System administration tools for monitoring users' disk usage.
Version: 2.00
Release: 2owl
Copyright: BSD
Source0: ftp://ftp.cistron.nl/pub/people/mvw/quota/%{name}-2.00.tar.gz
Group: System Environment/Base
Patch0: quota-2.00-pld-owl-man.diff
Patch1: quota-2.00-owl-install-no-root.diff
Patch2: quota-2.00-owl-tmp.diff
BuildRoot: /var/rpm-buildroot/%{name}-root
BuildPreReq: e2fsprogs-devel

%description
The quota package contains system administration tools for monitoring
and limiting users' and or groups' disk usage, per filesystem.

Install quota if you want to monitor and/or limit user/group disk
usage.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%configure
make

%install
rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/sbin
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man{1,2,3,8}

%makeinstall root_sbindir=${RPM_BUILD_ROOT}/sbin DEF_BIN_MODE=0555 

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%doc doc/*
%defattr(-,root,root)
/sbin/*
%{_bindir}/*
%{_sbindir}/edquota
%{_sbindir}/quotastats
%{_sbindir}/repquota
%{_sbindir}/setquota
%{_sbindir}/warnquota

%{_mandir}/man1/quota.1*
%{_mandir}/man2/quotactl.2*
%{_mandir}/man3/rquota.3*
%{_mandir}/man8/edquota.8*
%{_mandir}/man8/quotacheck.8*
%{_mandir}/man8/quotaon.8*
%{_mandir}/man8/repquota.8*
%{_mandir}/man8/setquota.8*

%changelog
* Sun Mon 27 2001 Michail Litvak <mci@owl.openwall.com>
- more fixes in mans and docs
- patch to catch error from mkstemp
- include doc/ subdir into package

* Sun Mon 25 2001 Michail Litvak <mci@owl.openwall.com>
- some spec cleanups
- patch to allow building to non-root user

* Sun Jun 24 2001 Michail Litvak <mci@owl.openwall.com>
- Imported from RH
- man patch from PLD 

* Mon Aug 21 2000 Jeff Johnson <jbj@redhat.com>
- add LABEL=foo support (#16390).

* Thu Jul 27 2000 Jeff Johnson <jbj@redhat.com>
- remote NFS quotas with different blocksize converted incorrectly (#11932).

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 15 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Wed May 10 2000 Jeff Johnson <jbj@redhat.com>
- apply patch5 (H.J. Lu)

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description
- man pages are compressed

* Tue Jan 18 2000 Preston Brown <pbrown@redhat.com>
- quota 2.00 series
- removed unnecessary patches

* Thu Aug  5 1999 Jeff Johnson <jbj@redhat.com>
- fix man page FUD (#4369).

* Thu May 13 1999 Peter Hanecak <hanecak@megaloman.sk>
- changes to allow non-root users to build too (Makefile patch, %attr)

* Tue Apr 13 1999 Jeff Johnson <jbj@redhat.com>
- fix for sparc64 quotas (#2147)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Mon Dec 28 1998 Cristian Gafton <gafton@redhat.com>
- don't install rpc.rquotad - we will use the one from the knfsd package
  instead

* Thu Dec 17 1998 Jeff Johnson <jbj@redhat.com>
- merge ultrapenguin 1.1.9 changes.

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- removed patch for mntent

* Fri Mar 27 1998 Jakub Jelinek <jj@ultra.linux.cz>
- updated to quota 1.66

* Tue Jan 13 1998 Erik Troan <ewt@redhat.com>
- builds rquotad
- installs rpc.rquotad.8 symlink

* Mon Oct 20 1997 Erik Troan <ewt@redhat.com>
- removed /usr/include/rpcsvc/* from filelist
- uses a buildroot and %attr

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Tue Mar 25 1997 Erik Troan <ewt@redhat.com>
- Moved /usr/sbin/quota to /usr/bin/quota
