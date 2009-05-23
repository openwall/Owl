# $Owl: Owl/packages/diffstat/diffstat.spec,v 1.13 2009/05/23 20:23:05 mci Exp $

Summary: A utility which provides statistics based on the output of diff.
Name: diffstat
Version: 1.47
Release: owl1
Group: Development/Tools
License: distributable
URL: http://invisible-island.net/diffstat/
Source: ftp://dickey.his.com/diffstat/%name-%version.tgz
Patch: diffstat-1.47-owl-man.diff
Prefix: %_prefix
BuildRoot: /override/%name-%version

%description
The diff command compares files line by line.  Diffstat reads the
output of the diff command and displays a histogram of the insertions,
deletions and modifications in each file.  Diffstat is commonly used
to provide a summary of the changes in large, complex patch files.

%prep
%setup -q
%patch -p1

%build
%configure --with-warnings
%__make

%install
rm -rf %buildroot
%makeinstall

%files
%defattr(-,root,root)
%doc README CHANGES
%_bindir/diffstat
%_mandir/man1/*

%changelog
* Sat May 23 2009 Michail Litvak <mci-at-owl.openwall.com> 1.47-owl1
- Updated to 1.47.

* Wed Oct 17 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.45-owl1
- Updated to 1.45.

* Mon Dec 26 2005 Michail Litvak <mci-at-owl.openwall.com> 1.41-owl1
- 1.41
- Small man-page fix.

* Wed Jan 15 2003 Michail Litvak <mci-at-owl.openwall.com> 1.32-owl2
- Use configure --with-warnings instead our -Wall

* Sun Jan 12 2003 Michail Litvak <mci-at-owl.openwall.com>
- 1.32

* Thu Jan 24 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Tue Jan 30 2001 Michail Litvak <mci-at-owl.openwall.com>
- add $RPM_OPT_FLAGS using for compiling

* Mon Jan 29 2001 Michail Litvak <mci-at-owl.openwall.com>
- imported spec from RH
- moved to new release
