# $Id: Owl/packages/tar/tar.spec,v 1.8 2002/08/05 16:38:01 solar Exp $

Summary: A GNU file archiving program.
Name: tar
Version: 1.13.19
Release: owl2
License: GPL
Group: Applications/Archiving
Source0: ftp://alpha.gnu.org/pub/gnu/tar/tar-%{version}.tar.gz
Source1: tar.1
Patch0: tar-1.13.19-owl-verify-looping-fix.diff
Patch1: tar-1.13.19-mdk-Iy.diff
Patch2: tar-1.13.19-rh-fail.diff
Patch3: tar-1.13.19-rh-owl-unreadable-segfault.diff
Patch4: tar-1.13.19-rh-autoconf.diff
Patch5: tar-1.13.19-rh-owl-no-librt.diff
Patch6: tar-1.13.19-owl-info.diff
PreReq: /sbin/install-info, grep
BuildRoot: /override/%{name}-%{version}

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
%patch4 -p1
%patch5 -p1
%patch6 -p1

%{expand:%%define optflags %optflags -Wall -Dlint}

%build
rm doc/tar.info
unset LINGUAS || :
autoconf
%configure --bindir=/bin --libexecdir=/sbin
make LIBS=-lbsd

%install
rm -rf $RPM_BUILD_ROOT

make install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	bindir=$RPM_BUILD_ROOT/bin \
	libexecdir=$RPM_BUILD_ROOT/sbin \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	infodir=$RPM_BUILD_ROOT%{_infodir}
ln -s tar $RPM_BUILD_ROOT/bin/gtar

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -m 644 $RPM_SOURCE_DIR/tar.1 $RPM_BUILD_ROOT%{_mandir}/man1/

%clean
rm -rf $RPM_BUILD_ROOT

%post
# Get rid of an old, incorrect info entry when replacing older versions
# of the package.
if grep -q '^Tar: ' %{_infodir}/dir; then
	INFODIRFILE=%{_infodir}/dir
	if test -L $INFODIRFILE; then
		INFODIRFILE="`readlink $INFODIRFILE`"
	fi
	cp -p $INFODIRFILE $INFODIRFILE.rpmtmp &&
	grep -v '^Tar: ' $INFODIRFILE > $INFODIRFILE.rpmtmp &&
	mv $INFODIRFILE.rpmtmp $INFODIRFILE
fi

/sbin/install-info %{_infodir}/tar.info.gz %{_infodir}/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/tar.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
/bin/tar
/bin/gtar
%{_mandir}/man1/tar.1*
%{_infodir}/tar.info*
%{_prefix}/share/locale/*/LC_MESSAGES/*

%changelog
* Mon Aug 05 2002 Michail Litvak <mci@owl.openwall.com>
- Fixed incorrect dir entry in info file.

* Mon Feb 04 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Tue Jul 10 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 1.13.19.
- Fixed the looping on verify bug.
- Store the man page separately, not as a patch.
- Dropped obsolete patches (all of them, actually; checked the testcase
for RH bug #9201 to make sure it doesn't occur with the new version, so
the patch can really be dropped).
- Imported relevant patches from Rawhide and Mandrake (via Alt).

* Thu Sep 07 2000 Solar Designer <solar@owl.openwall.com>
- Fixed the passing of %optflags into configure.

* Sun Aug 06 2000 Alexandr D. Kanevsiy <kad@owl.openwall.com>
- import from RH
- fix URL
