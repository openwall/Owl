# $Id: Owl/packages/autoconf/autoconf.spec,v 1.3 2002/02/04 17:13:23 solar Exp $

Summary: A GNU tool for automatically configuring source code.
Name: autoconf
Version: 2.13
Release: owl9
License: GPL
Group: Development/Tools
Source: ftp://ftp.gnu.org/gnu/autoconf/autoconf-%{version}.tar.gz
Patch0: autoconf-2.12-rh-race.diff
Patch1: autoconf-2.13-rh-mawk.diff
Patch2: autoconf-2.13-rh-notmp.diff
PreReq: /sbin/install-info
Requires: gawk, m4, mktemp, perl, textutils
BuildArchitectures: noarch
BuildRoot: /override/%{name}-%{version}

%description
Autoconf is a tool for producing shell scripts that automatically
configure software source code packages to adapt to many kinds of
Unix-like systems.  The configuration scripts produced by Autoconf
are independent of Autoconf when they are run, so their users do not
need to have Autoconf.  Using Autoconf, programmers can create
portable and configurable software.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_infodir}

%makeinstall

# We don't want to include the standards.info stuff in the package,
# because it comes from binutils...
rm -f ${RPM_BUILD_ROOT}%{_infodir}/standards*
cp install-sh ${RPM_BUILD_ROOT}%{_datadir}/autoconf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/autoconf.info.gz %{_infodir}/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/autoconf.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
%{_bindir}/*
%{_infodir}/*.info*
%{_datadir}/autoconf

%changelog
* Thu Jan 24 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.
- Based the new package description on the texinfo documentation.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import spec from RH
- fix URL
