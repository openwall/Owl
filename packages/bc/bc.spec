# $Id: Owl/packages/bc/bc.spec,v 1.2 2000/12/05 09:24:37 mci Exp $

Summary: GNU's bc (a numeric processing language) and dc (a calculator).
Name: bc
Version: 1.06
Release: 1owl
Copyright: GPL
Group: Applications/Engineering
Source: ftp://ftp.gnu.org/gnu/bc/bc-%{version}.tar.gz
Patch0: bc-1.06-owl-no_info_dir.diff
Prereq: /sbin/install-info grep
Prefix: %{_prefix}
Buildroot: /var/rpm-buildroot/%{name}-root
BuildRequires: readline-devel

%description
The bc package includes bc and dc.  Bc is an arbitrary precision
numeric processing arithmetic language.  Dc is an interactive
arbitrary precision stack based calculator, which can be used as a
text mode calculator.

Install the bc package if you need its number handling capabilities or
if you would like to use its text mode calculator.

%prep
%setup -q 
%patch0 -p1

%build
#autoconf
%configure --with-readline
make 

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%post
# previous versions of bc put an improper entry into %{_infodir}/dir -- remove
# it
if grep 'dc: (bc)' %{_infodir}/dir > /dev/null; then
    grep -v 'The GNU RPN calculator' < %{_infodir}/dir > %{_infodir}/dir.$$
    mv -f %{_infodir}/dir.$$ %{_infodir}/dir
fi


/sbin/install-info %{_infodir}/dc.info.gz %{_infodir}/dir \
        --entry="* dc: (dc).                    The GNU RPN calculator."

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_infodir}/dc.info.gz %{_infodir}/dir \
        --entry="* dc: (dc).                      The GNU RPN calculator."
fi

%files
%defattr(-,root,root)
/usr/bin/dc
/usr/bin/bc
%{_mandir}/*/*
%{_infodir}/*

%changelog
* Mon Nov 21 2000 Michail Litvak <mci@owl.openwall.com>
- Updated to 1.06 version
- added patch to avoid creation of dir file

* Fri Jul 21 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use %%makeinstall, %%configure, %%{_mandir}, %%{_infodir}
  and %%{_tmppath}  

* Wed May 10 2000 Trond Eivind Glomsrød <teg@redhat.com>
- added URL
- let build system handle man page gzipping

* Thu Apr 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fixed bug 7145 (long commands -> coredump) 
- removed explicit stripping, it does this by itself anyway
- gzipped man-pages

* Thu Mar 30 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Rebuild with new readline (4.1)

* Fri Mar 24 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Rebuild with new readline (4.0)
- fix Source URL
- some spec file cleanups

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Thu Jan 21 1999 Jeff Johnson <jbj@redhat.com>
- use %configure

* Fri Sep 11 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.05a.

* Sun Jun 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Thu Jun 04 1998 Jeff Johnson <jbj@redhat.com>
- updated to 1.05 with build root.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Apr 21 1998 Erik Troan <ewt@redhat.com>
- got upgrades of info entry working (I hope)

* Sun Apr 05 1998 Erik Troan <ewt@redhat.com>
- fixed incorrect info entry

* Wed Oct 15 1997 Donnie Barnes <djb@redhat.com>
- added install-info support

* Thu Sep 11 1997 Donald Barnes <djb@redhat.com>
- upgraded from 1.03 to 1.04

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
