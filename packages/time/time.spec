# $Id: Owl/packages/time/time.spec,v 1.1 2000/11/18 13:05:46 mci Exp $

Summary: A GNU utility for monitoring a program's use of system resources.
Name: time
Version: 1.7
Release: 13owl
License: GPL
Group: Applications/System
Source: ftp://ftp.gnu.org/gnu/time/time-%{version}.tar.gz
Source1: time.1
Patch0: time-1.7-deb-make_quiet.diff
Patch1: time-1.7-mdk-info.diff
Patch2: time-1.7-deb-info_quiet.diff
Prefix: %{_prefix}
BuildRoot: /var/rpm-buildroot/%{name}-root

%description
The GNU time utility runs another program, collects information about
the resources used by that program while it is running and
displays the results.

Time can help developers optimize their programs.

%prep
%setup -q
%patch0 -p0
%patch1 -p1 
%patch2 -p1
 
%build

%configure
make LDFLAGS=-s

%install
rm -rf ${RPM_BUILD_ROOT}
%makeinstall

mkdir -p  ${RPM_BUILD_ROOT}%{_mandir}/man1/
install -m 444 ${RPM_SOURCE_DIR}/time.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/install-info %{_infodir}/time.info.gz %{_infodir}/dir \
	--entry="* time: (time).		GNU time Utility" 

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/time.info.gz %{_infodir}/dir \
	--entry="* time: (time).		GNU time Utility" 
fi

%files
%defattr(-,root,root)
%doc NEWS README
%{_bindir}/time
%{_infodir}/time.info.gz
%{_mandir}/*/*

%changelog
* Sat Nov 18 2000 Michail Litvak <mci@owl.openwall.com> 
- imported from RH, some patches from MDK, and Debian
- added --quiet options (deb)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 29 2000 Preston Brown <pbrown@redhat.com>
- using / as the file manifesto has weird results.

* Sun Jun  4 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 9)

* Mon Aug 10 1998 Erik Troan <ewt@redhat.com>
- buildrooted and defattr'd

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon Oct 27 1997 Cristian Gafton <gafton@redhat.com>
- fixed info handling

* Thu Oct 23 1997 Cristian Gafton <gafton@redhat.com>
- updated the spec file; added info file handling

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
