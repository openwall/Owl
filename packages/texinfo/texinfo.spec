# $Id: Owl/packages/texinfo/texinfo.spec,v 1.3 2001/01/03 08:05:57 solar Exp $

Summary: Tools needed to create Texinfo format documentation files.
Name: 		texinfo
Version: 	4.0
Release: 	11owl
Copyright: 	GPL
Group: 		Applications/Publishing
Source0: 	ftp://ftp.gnu.org/gnu/texinfo/texinfo-%{version}.tar.gz
Source1: 	info-dir
Patch0:		texinfo-4.0-owl-tmp.diff
Patch1: 	texinfo-3.12h-rh-data_size_fix.diff
Patch2: 	texinfo-4.0-rh-zlib.diff
Prereq: 	/sbin/install-info
Prefix: 	%{_prefix}
Buildroot: 	/var/rpm-buildroot/%{name}-root

%define __spec_install_post /usr/lib/rpm/brp-strip \; /usr/lib/rpm/brp-strip-comment-note

%description
Texinfo is a documentation system that can produce both online
information and printed output from a single source file.  The GNU
Project uses the Texinfo file format for most of its documentation.

Install texinfo if you want a documentation system for producing both
online and print documentation from the same source file and/or if you
are going to write documentation for the GNU Project.

%package -n info
Summary: A stand-alone TTY-based reader for GNU texinfo documentation.
Group: System Environment/Base
# By making info prereq bash, other packages which have triggers based on
# info don't run those triggers until bash is in place as well. This is an
# ugly method of doing it (triggers which fire on set intersection would
# be better), but it's the best we can do for now. Talk to Erik before
# removing this.
Prereq: bash 

%description -n info
The GNU project uses the texinfo file format for much of its
documentation. The info package provides a standalone TTY-based
browser program for viewing texinfo files.

You should install info, because GNU's texinfo documentation is a
valuable source of information about the software on your system.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
unset LINGUAS || :
%configure --mandir=%{_mandir} --infodir=%{_infodir}
make

rm util/install-info
make -C util LIBS=%{_prefix}/lib/libz.a

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/{etc,sbin}

%makeinstall

cd ${RPM_BUILD_ROOT}
gzip -n -9f .%{_infodir}/*info*
install -m 644 $RPM_SOURCE_DIR/info-dir ./etc/info-dir
ln -sf /etc/info-dir ${RPM_BUILD_ROOT}%{_infodir}/dir
for i in makeinfo texindex info install-info; do
	strip .%{_prefix}/bin/$i
done
mv -f .%{_prefix}/bin/install-info ./sbin

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/install-info %{_infodir}/texinfo.gz %{_infodir}/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/texinfo.gz %{_infodir}/dir
fi

%post -n info
/sbin/install-info %{_infodir}/info-stnd.info.gz %{_infodir}/dir

%preun -n info
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/info-stnd.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog INSTALL INTRODUCTION NEWS README TODO
%doc info/README
%{_prefix}/bin/makeinfo
%{_prefix}/bin/texindex
%{_prefix}/bin/texi2dvi
%{_infodir}/texinfo*
%{_prefix}/share/locale/*/*/*

%files -n info
%defattr(-,root,root)
#%config(missingok) /etc/X11/applnk/Utilities/info.desktop
%config(noreplace) /etc/info-dir
%config(noreplace) %{_infodir}/dir
%{_prefix}/bin/info
%{_infodir}/info.info*
%{_infodir}/info-stnd.info*
/sbin/install-info

%changelog
* Wed Jan 03 2001 Solar Designer <solar@owl.openwall.com>
- Patch to create temporary files safely.
- Give offline sorting in texindex a chance to work (fixed a bug in there;
did anyone ever test that code, it certainly looks like not).

* Wed Aug 09 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
- FHS build

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Wed Jun 28 2000 Bill Nottingham <notting@redhat.com>
- fix build wackiness with info page compressing

* Fri Jun 16 2000 Bill Nottingham <notting@redhat.com>
- fix info-dir symlink

* Thu May 18 2000 Preston Brown <pbrown@redhat.com>
- use FHS paths for info.

* Fri Mar 24 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- rebuild with current ncurses

* Wed Feb 09 2000 Preston Brown <pbrown@redhat.com>
- wmconfig -> desktop

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix descriptions

* Wed Jan 26 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- move info-stnd.info* to the info package, /sbin/install-info it
  in %post (Bug #6632)

* Thu Jan 13 2000 Jeff Johnson <jbj@redhat.com>
- recompile to eliminate ncurses foul-up.

* Tue Nov  9 1999 Bernhard Rosenkränzer <bero@redhat.com>
- 4.0
- handle RPM_OPT_FLAGS

* Tue Sep 07 1999 Cristian Gafton <gafton@redhat.com>
- import version 3.12h into 6.1 tree from HJLu

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Wed Mar 17 1999 Erik Troan <ewt@redhat.com>
- hacked to use zlib to get rid of the requirement on gzip

* Wed Mar 17 1999 Matt Wilson <msw@redhat.com>
- install-info prerequires gzip

* Thu Mar 11 1999 Cristian Gafton <gafton@redhat.com>
- version 3.12f
- make /usr/info/dir to be a %config(noreplace)
* Wed Nov 25 1998 Jeff Johnson <jbj@redhat.com>
- rebuild to fix docdir perms.

* Thu Sep 24 1998 Cristian Gafton <gafton@redhat.com>
- fix allocation problems in install-info

* Wed Sep 23 1998 Jeff Johnson <jbj@redhat.com>
- /sbin/install-info should not depend on /usr/lib/libz.so.1 -- statically
  link with /usr/lib/libz.a.

* Fri Aug 07 1998 Erik Troan <ewt@redhat.com>
- added a prereq of bash to the info package -- see the comment for a
  description of why that was done

* Tue Jun 09 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Tue Jun  9 1998 Jeff Johnson <jbj@redhat.com>
- add %attr to permit non-root build.

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sun Apr 12 1998 Cristian Gafton <gafton@redhat.com>
- added %clean
- manhattan build

* Wed Mar 04 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to version 3.12
- added buildroot

* Sun Nov 09 1997 Donnie Barnes <djb@redhat.com>
- moved /usr/info/dir to /etc/info-dir and made /usr/info/dir a
  symlink to /etc/info-dir.

* Wed Oct 29 1997 Donnie Barnes <djb@redhat.com>
- added wmconfig entry for info

* Wed Oct 01 1997 Donnie Barnes <djb@redhat.com>
- stripped /sbin/install-info

* Mon Sep 22 1997 Erik Troan <ewt@redhat.com>
- added info-dir to filelist

* Sun Sep 14 1997 Erik Troan <ewt@redhat.com>
- added patch from sopwith to let install-info understand gzip'ed info files
- use skeletal dir file from texinfo tarball (w/ bash entry to reduce
  dependency chain) instead (and install-info command everywhere else)
- patches install-info to handle .gz names correctly

* Tue Jun 03 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Tue Feb 25 1997 Erik Troan <ewt@redhat.com>
- patched install-info.c for glibc.
- added /usr/bin/install-info to the filelist

* Tue Feb 18 1997 Michael Fulbright <msf@redhat.com>
- upgraded to version 3.9.
