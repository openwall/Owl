# $Id: Owl/packages/modutils/modutils.spec,v 1.2 2000/10/18 19:23:08 solar Exp $

Summary: 	Kernel module utilities.
Name: 		modutils
Version: 	2.3.17
Release: 	4owl
Copyright: 	GPL
Group: 		System Environment/Kernel
Source0: 	ftp://ftp.kernel.org/pub/linux/utils/kernel/modutils/v2.3/modutils-%{version}.tar.bz2
Patch1: 	modutils-2.3.17-owl-alias.diff
Patch2:		modutils-2.3.17-rh-systemmap.diff
Exclusiveos: 	Linux
Buildroot: 	/var/rpm-buildroot/%{name}-%{version}
Prereq: 	/sbin/chkconfig
Obsoletes: 	modules

%description
The modutils packages includes the various programs neeed for automatic
loading and unloading of modules under 2.2 and later kernels as well as
other module management programs.  Examples of loaded and unloaded
modules are device drivers and filesystems, as well as some other things.

%prep
%setup -q
%patch1 -p1 -b .alias
%patch2 -p1 -b .systemmap

%build
# To build kernel 2.0.x compatible modutils, change the compat-2-0 and
# kerneld --disable-* to --enable-* and uncomment
# %config /etc/rc.d/init.d/kerneld in the %files section and remove the %post
# section.
%configure --disable-compat-2-0 --disable-kerneld --enable-insmod-static \
	--exec_prefix=/
make dep all

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
mkdir -p $RPM_BUILD_ROOT/etc/cron.d
mkdir -p $RPM_BUILD_ROOT/sbin
%makeinstall sbindir=$RPM_BUILD_ROOT/sbin

rm -f $RPM_BUILD_ROOT/%{_mandir}/man8/{kdstat,kerneld}.8

# security hole, works poorly anyway
rm -f $RPM_BUILD_ROOT/sbin/request-route
find $RPM_BUILD_ROOT/sbin/ -type l -a -name '*.static' -exec rm {} \;
strip $RPM_BUILD_ROOT/sbin/* || :

%clean
rm -rf $RPM_BUILD_ROOT

%post
# get rid of the old installations on upgrade
if [ -x /etc/rc.d/init.d/kerneld ] ; then
    /sbin/chkconfig --del kerneld
fi
if [ -f /etc/conf.modules -a ! -f /etc/modules.conf ] ; then
    mv -f /etc/conf.modules /etc/modules.conf
fi

%files
%defattr(-,root,root)
/sbin/*
%{_mandir}/*/*
#%config /etc/rc.d/init.d/kerneld

%changelog
* Wed Oct 18 2000 Solar Designer <solar@owl.openwall.com>
- Removed /etc/cron.d/kmod

* Sun Oct  1 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import spec from RH 
- fix aliases
- v2.3.17

* Mon Aug 21 2000 Michael K. Johnson <johnsonm@redhat.com>
- Use %{_mandir} for removing kerneld-related man pages.

* Wed Aug  9 2000 Jakub Jelinek <jakub@redhat.com>
- fix build on SPARC

* Tue Aug  8 2000 Jakub Jelinek <jakub@redhat.com>
- update to 2.3.14

* Tue Jul 25 2000 Bill Nottingham <notting@redhat.com>
- update to 2.3.13
- turn psaux off again
- remove sound patch; it's obsolete

* Wed Jul 19 2000 Jakub Jelinek <jakub@redhat.com>
- rebuild to cope with glibc locale binary incompatibility

* Thu Jul 13 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.3.12
- fix up ia64

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jul  1 2000 Florian La Roche <laroche@redhat.com>
- add aliases for cipcb[0-3]

* Wed Jun 14 2000 Matt Wilson <msw@redhat.com>
- fix build on combined 32/64 bit sparc

* Thu Jun  1 2000 Bill Nottingham <notting@redhat.com>
- modules.confiscation

* Wed May 17 2000 Bill Nottingham <notting@redhat.com>
- add ia64 patch from Intel

* Wed May 17 2000 Jakub Jelinek <jakub@redhat.com>
- fix build with glibc 2.2

* Tue May 09 2000 Doug Ledford <dledford@redhat.com>
- Correct %description to reflect that we don't build kerneld by default

* Fri Apr 21 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.3.11

* Mon Apr  3 2000 Bill Nottingham <notting@redhat.com>
- fix net-pf-* aliases for ipx, appletalk

* Fri Mar 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.3.10

* Thu Feb 17 2000 Matt Wilson <msw@redhat.com>
- added alias for agpgart

* Mon Feb 14 2000 Bill Nottingham <notting@redhat.com>
- hardcode psaux alias to off everywhere

* Thu Feb  3 2000 Bill Nottingham <notting@redhat.com>
- add a symlink from conf.modules.5 to modules.conf.5

* Fri Jan 29 2000 Bill Nottingham <notting@redhat.com>
- fix breakage *correctly*

* Sat Jan 22 2000 Bill Nottingham <notting@redhat.com>
- fix breakage of our own cause w.r.t sound modules

* Thu Jan 06 2000 Jakub Jelinek <jakub@redhat.com>
- update to 2.3.9.
- port RH patches from 2.1.121 to 2.3.9 where needed.
- disable warning about conf.modules for now, in 7.0
  we should move to modules.conf.

* Wed Oct 13 1999 Jakub Jelinek <jakub@redhat.com>
- hardcode psaux alias on sparc to off.

* Tue Oct 05 1999 Bill Nottingham <notting@redhat.com>
- hardcode parport aliases....

* Mon Oct 04 1999 Cristian Gafton <gafton@redhat.com>
- rebuild against new glibc in the sparc tree

* Wed Sep 15 1999 Jakub Jelinek <jakub@redhat.com>
- rewrite sparckludge so that separate *64 binaries
  are not needed anymore.

* Sat Sep 11 1999 Cristian Gafton <gafton@redhat.com>
- apply the last patch in the %prep section (doh!)

* Mon Apr 19 1999 Cristian Gafton <gafton@redhat.com>
- add support for the ppp compression modules by default

* Tue Apr 13 1999 Michael K. Johnson <johnsonm@redhat.com>
- add cron.d file to run rmmod -as

* Fri Apr 09 1999 Cristian Gafton <gafton@redhat.com>
- take out kerneld

* Mon Apr 05 1999 Cristian Gafton <gafton@redhat.com>
- add patch to make all raid personalities recognized

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 7)

* Thu Mar 18 1999 Cristian Gafton <gafton@redhat.com>
- obsoletes modules
- get rid of the /lib/modules/preferred hack

* Mon Mar 15 1999 Bill Nottingham <notting@redhat.com>
- added support for /lib/modules/foo/pcmcia
- make kerneld initscript not start by default

* Tue Feb 23 1999 Matt Wilson <msw@redhat.com>
- added sparc64 support from UltraPenguin

* Tue Jan 12 1999 Cristian Gafton <gafton@redhat.com>
- call libtoolize to allow it to compile on the arm

* Wed Dec 23 1998 Jeff Johnson <jbj@redhat.com>
- search /lib/modules/preferred before defaults but after specified paths.

* Tue Nov 17 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to version 2.1.121

* Thu Nov 05 1998 Erik Troan <ewt@redhat.com>
- added -m, -i options

* Thu Oct 01 1998 Michael K. Johnson <johnsonm@redhat.com>
- fix syntax error I introduced when enhancing initscript

* Wed Sep 30 1998 Michael K. Johnson <johnsonm@redhat.com>
- enhance initscript

* Fri Aug 28 1998 Jeff Johnson <jbj@redhat.com>
- recompile statically linked binary for 5.2/sparc

* Tue Jul 28 1998 Jeff Johnson <jbj@redhat.com>
- pick up ultrapenguin patches (not applied for now).
- pre-generate keyword.c so gperf doesn't have to be present (not applied).
- util/sys_cm.c: fix create_module syscall (signed return on sparc too)

* Wed Jul 15 1998 Jeff Johnson <jbj@redhat.com>
- correct %postun typos

* Fri May 01 1998 Erik Troan <ewt@redhat.com>
- added /lib/modules/preferred to search path

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Apr 07 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.1.85
- actually make use of the BuildRoot

* Fri Apr  3 1998 Jakub Jelinek <jj@ultra.linux.cz>
- Fix sparc64, add modinfo64 on sparc.

* Wed Mar 23 1998 Jakub Jelinek <jj@ultra.linux.cz>
- Handle EM_SPARCV9, kludge to support both 32bit and 64bit kernels
  from the same package on sparc/sparc64.

* Fri Nov  7 1997 Michael Fulbright
- removed warning message when conf.modules exists and is a empty

* Tue Oct 28 1997 Erik Troan <ewt@redhat.com>
- patched to honor -k in options
- added modprobe.1
- added init script

* Thu Oct 23 1997 Erik Troan <ewt@redhat.com>
- removed bogus strip of lsmod (which is a script)

* Mon Oct 20 1997 Erik Troan <ewt@redhat.com>
- updated to 2.1.55
- builds in a buildroot

* Mon Aug 25 1997 Erik Troan <ewt@redhat.com>
- added insmod.static

* Sun Aug 24 1997 Erik Troan <ewt@redhat.com>
- built on Intel
- combined rmmod and insmod
