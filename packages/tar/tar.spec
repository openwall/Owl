# $Id: Owl/packages/tar/tar.spec,v 1.3.2.2 2001/07/10 13:16:05 solar Exp $

Summary: A GNU file archiving program.
Name: 		tar
Version:	1.13.17
Release: 	8owl
Copyright: 	GPL
Group: 		Applications/Archiving
Source: 	ftp://alpha.gnu.org/pub/gnu/tar/tar-%{version}.tar.gz
Patch0: 	tar-1.13.14-rh-manpage.diff
Patch1: 	tar-1.13.17-rh-fnmatch.diff
Patch2: 	tar-1.3.17-rh-excluded_name.diff
Patch3:		tar-1.13.17-owl-verify-looping-fix.diff
Prereq: 	/sbin/install-info
Buildroot: 	/var/rpm-buildroot/%{name}-root

%description
The GNU tar program saves many files together into one archive and can
restore individual files (or all of the files) from the archive.  tar
can also be used to add supplemental files to an archive and to update
or list files in the archive.  tar includes multivolume support,
automatic archive compression/decompression, the ability to perform
remote archives and the ability to perform incremental and full
backups.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build

%ifos linux
unset LINGUAS || :
CFLAGS="%optflags -DHAVE_STRERROR -D_GNU_SOURCE" \
%configure --bindir=/bin --libexecdir=/sbin
make LIBS=-lbsd
%else
%configure
make
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ifos linux
make prefix=${RPM_BUILD_ROOT}%{_prefix} \
    bindir=${RPM_BUILD_ROOT}/bin \
    libexecdir=${RPM_BUILD_ROOT}/sbin \
    mandir=${RPM_BUILD_ROOT}%{_mandir} \
    infodir=${RPM_BUILD_ROOT}%{_infodir} \
	install
ln -s tar ${RPM_BUILD_ROOT}/bin/gtar
%else
make prefix=${RPM_BUILD_ROOT}%{_prefix} \
    localedir=${RPM_BUILD_ROOT}%{_prefix}/share/locale \
    mandir=${RPM_BUILD_ROOT}%{_mandir} \
    infodir=${RPM_BUILD_ROOT}%{_infodir} \
	install
%endif

( cd $RPM_BUILD_ROOT
  for dir in ./bin ./sbin .%{_prefix}/bin .%{_prefix}/libexec
  do
    [ -d $dir ] || continue
    strip $dir/* || :
  done
  gzip -9nf .%{_infodir}/tar.info*
  rm -f .%{_infodir}/dir
)

mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
install -c -m644 tar.1 ${RPM_BUILD_ROOT}%{_mandir}/man1

%post
/sbin/install-info %{_infodir}/tar.info.gz %{_infodir}/dir

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/tar.info.gz %{_infodir}/dir
fi

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%ifos linux
/bin/tar
/bin/gtar
%{_mandir}/man1/tar.1*
%else
%{_prefix}/bin/*
%{_prefix}/libexec/*
%{_mandir}/man*/*
%endif

%{_infodir}/tar.info*
%{_prefix}/share/locale/*/LC_MESSAGES/*

%changelog
* Tue Jul 10 2001 Solar Designer <solar@owl.openwall.com>
- Fixed the looping on verify bug.

* Thu Sep 07 2000 Solar Designer <solar@owl.openwall.com>
- Fixed the passing of %optflags into configure.

* Sun Aug 06 2000 Alexandr D. Kanevsiy <kad@owl.openwall.com>
- import from RH
- fix URL
