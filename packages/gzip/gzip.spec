# $Id: Owl/packages/gzip/gzip.spec,v 1.4 2001/09/28 01:25:50 solar Exp $

Summary: The GNU data compression program.
Name: gzip
Version: 1.3
Release: 13owl
License: GPL
Group: Applications/File
Source: ftp://alpha.gnu.org/gnu/gzip/gzip-%{version}.tar.gz
Patch0: gzip-1.3-openbsd-owl-tmp.diff
Patch1: gzip-1.2.4-rh-zforce.diff
Patch2: gzip-1.2.4a-rh-dirinfo.diff
Patch3: gzip-1.3-rh-stderr.diff
Patch4: gzip-1.3-rh-zgreppipe.diff
URL: http://www.gzip.org
Prereq: /sbin/install-info
Requires: mktemp >= 1:1.0
Buildroot: /var/rpm-buildroot/gzip-%{version}-root

%description
The gzip package contains the popular GNU gzip data compression
program and its associated scripts to manage compressed files.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%configure --bindir=/bin
make
make gzip.info

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall bindir=$RPM_BUILD_ROOT/bin gzip.info
mkdir -p $RPM_BUILD_ROOT/usr/bin
ln -sf ../../bin/gzip $RPM_BUILD_ROOT/usr/bin/gzip
ln -sf ../../bin/gunzip $RPM_BUILD_ROOT/usr/bin/gunzip

for i in zcmp zegrep zforce zless znew gzexe zdiff zfgrep zgrep zmore; do
	mv $RPM_BUILD_ROOT/bin/$i $RPM_BUILD_ROOT/usr/bin/$i
done

gzip -9nf $RPM_BUILD_ROOT%{_infodir}/gzip.info*

cat > $RPM_BUILD_ROOT/usr/bin/zless <<EOF
#!/bin/sh
/bin/zcat "\$@" | /usr/bin/less
EOF
chmod 755 $RPM_BUILD_ROOT/usr/bin/zless

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/gzip.info.gz %{_infodir}/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/gzip.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
%doc NEWS README AUTHORS ChangeLog THANKS TODO
/bin/*
/usr/bin/*
%{_mandir}/*/*
%{_infodir}/gzip.info*

%changelog
* Fri Sep 28 2001 Solar Designer <solar@owl.openwall.com>
- Patched unsafe temporary file handling in gzexe, zdiff, and znew based
on work by Todd Miller of OpenBSD.
- Dropped Red Hat's patch which attempted to fix some of the same issues
for gzexe but was far from sufficient.

* Sat Jun 16 2001 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- sync mktemp patch from RH
- errors go to stderror
- add handler for SIGPIPE in zgrep

* Sun Aug  6 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from RH
