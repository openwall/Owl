# $Id: Owl/packages/diffstat/diffstat.spec,v 1.4 2003/01/12 00:27:13 mci Exp $

Summary: A utility which provides statistics based on the output of diff.
Name: diffstat
Version: 1.32
Release: owl1
Group: Development/Tools
License: distributable
Source: ftp://dickey.his.com/diffstat/%{name}-%{version}.tgz
Prefix: %{_prefix}
BuildRoot: /override/%{name}-%{version}

%description
The diff command compares files line by line.  Diffstat reads the
output of the diff command and displays a histogram of the insertions,
deletions and modifications in each file.  Diffstat is commonly used
to provide a summary of the changes in large, complex patch files.

%prep
%setup -q

%build
%configure
make CFLAGS="$RPM_OPT_FLAGS -Wall"

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall mandir=$RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README CHANGES
%{_bindir}/diffstat
%{_mandir}/*/*

%changelog
* Sun Jan 12 2003 Michail Litvak <mci@owl.openwall.com>
- 1.32

* Thu Jan 24 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Tue Jan 30 2001 Michail Litvak <mci@owl.openwall.com>
- add $RPM_OPT_FLAGS using for compiling

* Mon Jan 29 2001 Michail Litvak <mci@owl.openwall.com>
- imported spec from RH
- moved to new release
