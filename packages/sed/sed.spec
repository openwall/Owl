# $Id: Owl/packages/sed/sed.spec,v 1.1 2000/08/09 00:51:27 kad Exp $

Summary: A GNU stream text editor.
Name: 		sed
Version: 	3.02
Release: 	8owl
Copyright: 	GPL
Group: 		Applications/Text
Source0: 	ftp://ftp.gnu.org/pub/gnu/sed/sed-%{version}.tar.gz
Prereq: 	/sbin/install-info
Prefix: 	%{_prefix}
Buildroot: 	/var/rpm-buildroot/%{name}-root

%description
The sed (Stream EDitor) editor is a stream or batch (non-interactive)
editor.  Sed takes text as input, performs an operation or set of
operations on the text and outputs the modified text.  The operations
that sed performs (substitutions, deletions, insertions, etc.) can be
specified in a script file or from the command line.

%prep
%setup -q

%build

%configure
make

%install
rm -rf ${RPM_BUILD_ROOT}

%makeinstall

{ cd ${RPM_BUILD_ROOT}

%ifos linux
  mkdir -p ./bin
  mv .%{_bindir}/sed ./bin/sed
  rmdir .%{_bindir}
%endif

  gzip -9nf .%{_infodir}/sed.info*
  rm -f .%{_infodir}/dir
}

%post
/sbin/install-info %{_infodir}/sed.info.gz %{_infodir}/dir

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/sed.info.gz %{_infodir}/dir
fi

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc ANNOUNCE BUGS NEWS README TODO
%ifos linux
/bin/sed 
%else
%{_bindir}/sed
%endif
%{_infodir}/*.info*
%{_mandir}/man*/*

%changelog
* Sun Aug  6 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import spec from RH rawhide
- fix URL

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Mon Feb  7 2000 Jeff Johnson <jbj@redhat.com>
- compress man pages.

* Tue Jan 18 2000 Jakub Jelinek <jakub@redhat.com>
- rebuild with glibc 2.1.3 to fix an mmap64 bug in sys/mman.h

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Tue Aug 18 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.02

* Sun Jul 26 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.01

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- removed references to the -g option from the man page that we add

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups
- added BuildRoot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
