# $Id: Owl/packages/which/which.spec,v 1.2 2000/11/19 10:46:49 mci Exp $

Summary: Displays where a particular program in your path is located.
Name: which
Version: 2.12
Release: 1owl
License: GPL
Group: Applications/System
Source0: ftp://ftp.gnu.org/gnu/which/%{name}-%{version}.tar.gz
Source1: which-2.sh
Source2: which-2.csh
Patch0: which-2.12-mdk-null_to_0.diff 
Prefix: %{_prefix}
Buildroot: /var/rpm-buildroot/%{name}-root

%description
The which command shows the full pathname of a specified program, if
the specified program is in your PATH.

%prep
%setup -q
%patch0 -p1

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall
mkdir -p $RPM_BUILD_ROOT/etc/profile.d
install -m 755 $RPM_SOURCE_DIR/which-2.sh $RPM_SOURCE_DIR/which-2.csh \
	$RPM_BUILD_ROOT/etc/profile.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc EXAMPLES README
%{_bindir}/*
%config /etc/profile.d/which-2.*
%{_mandir}/*/*

%changelog
* Sun Nov 19 2000 Michail Litvak <mci@owl.openwall.com>
- update to 2.12
- imported patch from MDK

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Than Ngo <than@redhat.de>
- FHS packaging.

* Sun May 21 2000 Ngo Than <than@redhat.de>
- put man pages in /usr/share/man/*

* Thu Apr 20 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.11
- change from root:bin -> root:root

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- rebuild to gzip man page

* Sun Jan 16 2000 Preston Brown <pbrown@redhat.com>
- newer stuff rom Carlo (2.10).  Author's email: carlo@gnu.org

* Thu Jan 13 2000 Preston Brown <pbrown@redhat.com>
- adopted Carlo's specfile.

* Fri Sep 24 1999 Carlo Wood <carlo@gnu.org>
- There should not be a reason anymore to include README.alias in the rpm docs.
- Don't install as root.root in RPM_BUILD_ROOT, in order to allow to build
  rpm as non-root.
- Bug fix
- Added /etc/profile.d for automatic alias inclusion.

* Wed Aug 25 1999 Carlo Wood <carlo@gnu.org>
- Added README.alias.

* Wed Aug 11 1999 Carlo Wood <carlo@gnu.org>
- Typo in comment.

* Thu May 27 1999 Carlo Wood <carlo@gnu.org>
- Typo fix
- Moved maintainer targets from makefile to Makefile.am.

* Tue May 18 1999 Carlo Wood <carlo@gnu.org>
- Typo in appended changelog.
- Appended the old change log of `which-2.0.spec' to (this) %changelog,
  which is generated from the CVS log of `which-2.0.spec.in'.
- Generate which-2.spec from which-2.spec.in with automatic VERSION
  and CHANGELOG substitution.

* Tue May 14 1999 Carlo Wood <carlo@gnu.org>
- Moved assignment of CFLAGS to the configure line, using RPM_OPT_FLAGS now.
- Corrected Source: line to point to ftp.gnu.org.

* Sat Apr 17 1999 Carlo Wood <carlo@gnu.org>
- Started to use automake and autoconf

* Fri Apr 09 1999 Carlo Wood <carlo@gnu.org>
- Renamed which-2.0.spec to which-2.spec

