# $Id: Owl/packages/textutils/Attic/textutils.spec,v 1.6 2002/02/04 08:34:57 solar Exp $

Summary: A set of GNU text file modifying utilities.
Name: textutils
Version: 2.0.11
Release: owl2
License: GPL
Group: Applications/Text
Source: ftp://alpha.gnu.org/gnu/fetish/textutils-%{version}.tar.gz
Patch0: textutils-2.0.11-owl-tmp.diff
Patch1: textutils-2.0.11-owl-sort-size.diff
PreReq: /sbin/install-info
BuildRequires: libtool
BuildRoot: /override/%{name}-%{version}

%description
A set of GNU utilities for modifying the contents of files, including
programs for splitting, joining, comparing and modifying files.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
unset LINGUAS || :
export ac_cv_sys_long_file_names=yes \
%configure
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/bin
mv $RPM_BUILD_ROOT/usr/bin/{cat,sort} $RPM_BUILD_ROOT/bin/

%post
/sbin/install-info %{_infodir}/textutils.info.gz %{_infodir}/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete \
		%{_infodir}/textutils.info.gz %{_infodir}/dir
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc NEWS README
/bin/*
/usr/bin/*
%{_mandir}/*/*
%{_infodir}/textutils.info*
/usr/share/locale/*/*/*

%changelog
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
