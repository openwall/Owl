# $Id: Owl/packages/diffstat/diffstat.spec,v 1.2 2001/01/30 10:19:15 mci Exp $

Summary: A utility which provides statistics based on the output of diff.
Name: diffstat
Version: 1.28
Release: 1owl
Group: Development/Tools
Copyright: distributable
Source: ftp://dickey.his.com/diffstat/%{name}-%{version}.tgz
Prefix: %{_prefix}
BuildRoot: /var/rpm-buildroot/%{name}-root 

%description
The diff command compares files line by line.  Diffstat reads the
output of the diff command and displays a histogram of the insertions,
deletions and modifications in each file.  Diffstat is commonly used
to provide a summary of the changes in large, complex patch files.

Install diffstat if you need a program which provides a summary of the
diff command's output.  You'll need to also install diffutils.

%prep
%setup -q

%build
%configure
make CFLAGS="$RPM_OPT_FLAGS -Wall"

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall mandir=$RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README CHANGES
%{_bindir}/diffstat
%{_mandir}/*/*

%changelog
* Tue Jan 30 2001 Michail Litvak <mci@owl.openwall.com>
- add $RPM_OPT_FLAGS using for compiling

* Mon Jan 29 2001 Michail Litvak <mci@owl.openwall.com>
- imported spec from RH
- moved to new release

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 06 2000 Than Ngo <than@redhat.de>
- use rpm macros

* Wed May 31 2000 Ngo Than <than@redhat.de>
- rebuild for 7.0
- put man page in /usr/share/man/*
- use %configure
- fix makefile.in
- cleanup specfile

* Thu Feb 03 2000 Preston Brown <pbrown@redhat.com>
- gzip man page.

* Fri Aug 27 1999 Preston Brown <pbrown@redhat.com>
- upgrade to 1.27, add URL tag.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 7)

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Tue Aug 11 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc
