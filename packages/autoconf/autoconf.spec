# $Id: Owl/packages/autoconf/autoconf.spec,v 1.1 2000/08/09 01:51:45 kad Exp $

Summary: A GNU tool for automatically configuring source code.
Name: 		autoconf
Version: 	2.13
Release:	9owl
Copyright: 	GPL
Group: 		Development/Tools
Source: 	ftp://ftp.gnu.org/pub/gnu/autoconf/autoconf-%{version}.tar.gz
Patch0: 	autoconf-2.12-rh-race.diff
Patch1: 	autoconf-2.13-rh-mawk.diff
Patch2:		autoconf-2.13-rh-notmp.diff
Prereq: 	/sbin/install-info
Requires: 	gawk, m4, mktemp, perl, textutils
BuildArchitectures: noarch
BuildRoot: 	/var/rpm-buildroot/%{name}-root

%description
GNU's Autoconf is a tool for configuring source code and Makefiles.
Using Autoconf, programmers can create portable and configurable
packages, since the person building the package is allowed to 
specify various configuration options.

You should install Autoconf if you are developing software and you'd
like to use it to create shell scripts which will configure your 
source code packages. If you are installing Autoconf, you will also
need to install the GNU m4 package.

Note that the Autoconf package is not required for the end user who
may be configuring software with an Autoconf-generated script; 
Autoconf is only required for the generation of the scripts, not
their use.

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
mkdir -p ${RPM_BUILD_ROOT}%{_infodir}

#make prefix=${RPM_BUILD_ROOT}%{_prefix} install
%makeinstall

gzip -9nf ${RPM_BUILD_ROOT}%{_infodir}/autoconf.info*

# We don't want to include the standards.info stuff in the package,
# because it comes from binutils...
rm -f ${RPM_BUILD_ROOT}%{_infodir}/standards*
cp install-sh ${RPM_BUILD_ROOT}%{_datadir}/autoconf

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/install-info %{_infodir}/autoconf.info.gz %{_infodir}/dir

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/autoconf.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
%{_bindir}/*
%{_infodir}/*.info*
%{_datadir}/autoconf

%changelog
* Sun Aug  6 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import spec from RH 
- fix URL

* Fri Jul 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- add textutils as a dependency (#14439)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Sun Mar 26 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- fix preun

* Fri Mar 26 1999 Cristian Gafton <gafton@redhat.com>
- add patch to help autoconf clean after itself and not leave /tmp clobbered
  with acin.* and acout.* files (can you say annoying?)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)
- use gawk, not mawk

* Thu Mar 18 1999 Preston Brown <pbrown@redhat.com>
- moved /usr/lib/autoconf to /usr/share/autoconf (with automake)

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Tue Jan 12 1999 Jeff Johnson <jbj@redhat.com>
- update to 2.13.

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Mon Oct 05 1998 Cristian Gafton <gafton@redhat.com>
- requires perl

* Thu Aug 27 1998 Cristian Gafton <gafton@redhat.com>
- patch for fixing /tmp race conditions

* Sun Oct 19 1997 Erik Troan <ewt@redhat.com>
- spec file cleanups
- made a noarch package
- uses autoconf
- uses install-info

* Thu Jul 17 1997 Erik Troan <ewt@redhat.com>
- built with glibc

