# $Id: Owl/packages/textutils/Attic/textutils.spec,v 1.12 2004/09/10 07:32:51 galaxy Exp $

# The texinfo documentation for fileutils, sh-utils, and textutils is
# currently provided by fileutils.
%define BUILD_INFO 0

Summary: A set of GNU text file modifying utilities.
Name: textutils
Version: 2.0.11
Release: owl3
License: GPL
Group: Applications/Text
Source: ftp://alpha.gnu.org/gnu/fetish/textutils-%version.tar.gz
Patch0: textutils-2.0.11-owl-tmp.diff
Patch1: textutils-2.0.11-owl-sort-size.diff
%if %BUILD_INFO
PreReq: /sbin/install-info
%endif
BuildRequires: libtool
BuildRoot: /override/%name-%version

%description
A set of GNU utilities for modifying the contents of files, including
programs for splitting, joining, comparing and modifying files.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%{expand:%%define optflags %optflags -Wall -Dlint}

%build
unset LINGUAS || :
export ac_cv_sys_long_file_names=yes \
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

cd $RPM_BUILD_ROOT
mkdir bin
mv .%_bindir/{cat,cut,sort} bin/
ln -s ../../bin/cut .%_bindir/
test -r .%_bindir/cut

# XXX: (GM): Remove unpackaged files (check later)
rm %buildroot%_infodir/dir
%if !%BUILD_INFO
rm %buildroot%_infodir/textutils.info*
%endif

%if %BUILD_INFO
%post
/sbin/install-info %_infodir/textutils.info.gz %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete \
		%_infodir/textutils.info.gz %_infodir/dir
fi
%else
%pre
/sbin/install-info --quiet --delete \
	%_infodir/textutils.info.gz %_infodir/dir
%endif

%files
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README THANKS TODO
/bin/*
%_bindir/*
%_mandir/*/*
%if %BUILD_INFO
%_infodir/textutils.info*
%endif
%_datadir/locale/*/*/*

%changelog
* Mon Aug 05 2002 Solar Designer <solar@owl.openwall.com> 2.0.11-owl3
- No longer provide texinfo documentation, it is now a part of fileutils.
- Use _*dir, configure, and makeinstall RPM macros.
- Moved cut(1) to /bin for compatibility with Red Hat Linux.

* Mon Feb 04 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Fri Jan 26 2001 Solar Designer <solar@owl.openwall.com>
- Patched the flawed memory allocation strategy in sort(1) introduced
with 2.0.11.

* Sat Jan 06 2001 Solar Designer <solar@owl.openwall.com>
- 2.0.11
- DoS attack fixes for tac and sort (O_EXCL -> mkstemp).

* Wed Oct 25 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- 2.0.8 (+sha1sum)

* Sun Jul 30 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- imported from RH
