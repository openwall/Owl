# $Id: Owl/packages/gzip/gzip.spec,v 1.3 2001/06/20 08:32:18 kad Exp $

Summary: The GNU data compression program.
Name: 		gzip
Version: 	1.3
Release: 	12.1owl
Copyright: 	GPL
Group: 		Applications/File
Source: 	ftp://alpha.gnu.org/gnu/gzip/gzip-%{version}.tar.gz
Patch2: 	gzip-1.3-rh-mktemp.diff
Patch3: 	gzip-1.2.4-rh-zforce.diff
Patch5: 	gzip-1.2.4a-rh-dirinfo.diff
Patch6:		gzip-1.3-rh-stderr.diff
Patch7:		gzip-1.3-rh-zgreppipe.diff

URL: 		http://www.gzip.org/
Prereq: 	/sbin/install-info
Requires: 	mktemp
Buildroot: 	/var/rpm-buildroot/gzip-%{version}-root

%description
The gzip package contains the popular GNU gzip data compression
program.  Gzipped files have a .gz extension.

Gzip should be installed on your Red Hat Linux system, because it is a
very commonly used data compression program.

%prep
%setup -q
%patch2 -p1 -b .mktemp
%patch3 -p1 -b .zforce
%patch5 -p1 -b .dirinfo
%patch6 -p1 -b .stderr
%patch7 -p1 -b .zgreppipe

%build
%configure  --bindir=/bin
make 
make gzip.info

%clean
rm -rf $RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall  bindir=$RPM_BUILD_ROOT/bin gzip.info
mkdir -p $RPM_BUILD_ROOT/usr/bin
ln -sf ../../bin/gzip $RPM_BUILD_ROOT/usr/bin/gzip
ln -sf ../../bin/gunzip $RPM_BUILD_ROOT/usr/bin/gunzip

for i in  zcmp zegrep zforce zless znew gzexe zdiff zfgrep zgrep zmore ; do
    mv $RPM_BUILD_ROOT/bin/$i $RPM_BUILD_ROOT/usr/bin/$i
done

gzip -9nf $RPM_BUILD_ROOT%{_infodir}/gzip.info*


cat > $RPM_BUILD_ROOT/usr/bin/zless <<EOF
#!/bin/sh
/bin/zcat "\$@" | /usr/bin/less
EOF
chmod 755 $RPM_BUILD_ROOT/usr/bin/zless

%post
/sbin/install-info %{_infodir}/gzip.info.gz %{_infodir}/dir 

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/gzip.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
%doc NEWS README AUTHORS ChangeLog THANKS TODO
/bin/*
/usr/bin/*
%{_mandir}/*/*
%{_infodir}/gzip.info*

%changelog
* Sat Jun 16 2001 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- sync mktemp patch from RH
- errors go to stderror
- add handler for SIGPIPE in zgrep

* Sun Aug  6 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 27 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild

* Wed Jun 07 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Use %%{_mandir}, %%{_infodir},  %%configure, %%makeinstall
  and %%{_tmppath}

* Fri May 12 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Add root as default owner of the files, permits building 
  as non-root user

* Wed May 10 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Build system handles stripping
- Don't do thing the system does, like creating directories
- use --bindir /bin
- Added URL
- skip unnecesarry sed step
- Include THANKS, AUTHORS, ChangeLog, TODO

* Mon Mar 20 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.3
- handle RPM_OPT_FLAGS

* Tue Feb 15 2000 Cristian Gafton <gafton@redhat.com>
- handle compressed man pages even better

* Tue Feb 08 2000 Cristian Gafton <gafton@redhat.com>
- adopt patch from Paul Eggert to fix detection of the improper tables in
  inflate.c(huft_build)
- the latest released version 1.2.4a, which provides documentation updates
  only. But it lets us use small revision numbers again
- add an dirinfo entry for gzip.info so we can get rid of the ugly --entry
  args to install-info

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Thu Feb 03 2000 Elliot Lee <sopwith@redhat.com>
- Fix bug #7970

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 14)

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- built against gliibc 2.1

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 09 1998 Cristian Gafton <gafton@redhat.com>
- added /usr/bin/gzip and /usr/bin/gunzip symlinks as some programs are too
  brain dead to figure out they should be at least trying to use $PATH
- added BuildRoot

* Wed Jan 28 1998 Erik Troan <ewt@redhat.com>
- fix /tmp races

* Sun Sep 14 1997 Erik Troan <ewt@redhat.com>
- uses install-info
- applied patch for gzexe

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Tue Apr 22 1997 Marc Ewing <marc@redhat.com>
- (Entry added for Marc by Erik) fixed gzexe to use /bin/gzip

