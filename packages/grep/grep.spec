# $Id: Owl/packages/grep/grep.spec,v 1.5 2002/02/04 17:13:24 solar Exp $

Summary: The GNU versions of grep pattern matching utilities.
Name: grep
Version: 2.4.2
Release: owl1
Epoch: 1
License: GPL
Group: Applications/Text
Source: ftp://ftp.gnu.org/gnu/grep/grep-%{version}.tar.gz
PreReq: /sbin/install-info
Prefix: %{_prefix}
BuildRoot: /override/%{name}-%{version}

%description
The GNU versions of commonly used grep utilities.  grep searches
through textual input for lines which contain a match to a specified
pattern and then prints the matching lines.  GNU's grep utilities
include grep, egrep and fgrep.

%prep
%setup -q

%build
unset LINGUAS || :
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall LDFLAGS=-s \
	prefix=${RPM_BUILD_ROOT}%{_prefix} exec_prefix=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/bin
mv $RPM_BUILD_ROOT%{_prefix}/bin/* $RPM_BUILD_ROOT/bin/
rm -rf $RPM_BUILD_ROOT%{_prefix}/bin

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/grep.info.gz %{_infodir}/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/grep.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
%doc ABOUT-NLS AUTHORS THANKS TODO NEWS README ChangeLog
/bin/*
%{_infodir}/*.info*
%{_mandir}/*/*
%{_prefix}/share/locale/*/*/grep.*

%changelog
* Sun Feb 03 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions

* Sun Jul 30 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- imported from RH
- locales fix
