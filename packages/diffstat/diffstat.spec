# $Owl: Owl/packages/diffstat/diffstat.spec,v 1.15 2010/08/23 08:29:51 segoon Exp $

Summary: A utility which provides statistics based on the output of diff.
Name: diffstat
Version: 1.53
Release: owl1
Group: Development/Tools
License: distributable
URL: http://invisible-island.net/diffstat/
Source: ftp://dickey.his.com/diffstat/%name-%version.tgz
Patch0: diffstat-1.47-owl-man.diff
Patch1: diffstat-1.51-owl-tmp.diff
Prefix: %_prefix
BuildRoot: /override/%name-%version

%description
The diff command compares files line by line.  Diffstat reads the
output of the diff command and displays a histogram of the insertions,
deletions and modifications in each file.  Diffstat is commonly used
to provide a summary of the changes in large, complex patch files.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure --with-warnings
%__make

%check
%__make check

%install
rm -rf %buildroot
%makeinstall

%files
%defattr(-,root,root)
%doc README CHANGES
%_bindir/diffstat
%_mandir/man1/*

%changelog
* Fri Aug 21 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 1.53-owl1
- Updated to 1.53.

* Wed Nov 18 2009 Solar Designer <solar-at-owl.openwall.com> 1.51-owl1
- Updated to 1.51.
- Remove the temporary directory on error (introduced in 1.48+).
- Run the testsuite.

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
