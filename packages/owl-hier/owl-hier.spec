# $Id: Owl/packages/owl-hier/owl-hier.spec,v 1.8 2001/09/25 16:39:56 solar Exp $

Summary: Initial directory hierarchy
Name: owl-hier
Version: 0.3
Release: 1owl
License: public domain
Group: System Environment/Base
Source: special
Buildroot: /var/rpm-buildroot/%{name}-%{version}
BuildPreReq: mtree
Requires: owl-etc
Obsoletes: filesystem
Provides: filesystem
BuildArchitectures: noarch

%description
This package contains the initial directory hierarchy for Owl, and
its corresponding mtree specification.

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT

# Create the directory hierarchy
cd $RPM_BUILD_ROOT
sed \
	-e "s/\(uname=\)root /\1`id -un` /" \
	-e "s/\(uname=\)root$/\1`id -un`/" \
	-e "s/\(gname=\)root /\1`id -gn` /" \
	-e "s/\(gname=\)root$/\1`id -gn`/" \
	< %{SOURCE0} |
		/usr/sbin/mtree -U
ln -s /var/tmp usr/tmp
ln -s ../X11R6/bin usr/bin/X11
ln -s ../X11R6/lib/X11 usr/lib/X11
ln -s log var/adm
ln -s spool/mail var/mail
cp %{SOURCE0} etc/mtree
chmod 600 etc/mtree/special

# Build the filelist
cd $RPM_BUILD_DIR
find $RPM_BUILD_ROOT -type d | sed \
	-e "s,^$RPM_BUILD_ROOT,," \
	-e 's,^,%dir ,' > filelist.mtree
find $RPM_BUILD_ROOT -type f -o -type l | sed \
	-e "s,^$RPM_BUILD_ROOT,," \
	-e 's,^.*/etc,%config &,' >> filelist.mtree

# Specify some entries manually to set user/group when building as non-root
cat << EOF > filelist
%defattr (-,root,root)
%dir %attr(755,sources,sources) /usr/src
%dir %attr(750,build,sources) /usr/src/world
%dir %attr(770,root,uucp) /var/lock/uucp
%dir %attr(1771,root,mail) /var/spool/mail
EOF

sed -n 's,^.* \(/[^ ]*\)$,\1,p' < filelist |
while read filename; do
	grep " $filename\$" filelist.mtree || :
	grep "^$filename\$" filelist.mtree || :
done | sort > filelist.remove

sort filelist.mtree |
comm -3 - filelist.remove >> filelist

%clean
rm -rf $RPM_BUILD_ROOT

%files -f filelist

%changelog
* Tue Sep 25 2001 Solar Designer <solar@owl.openwall.com>
- Provide /var/empty, which is a better choice than /usr/share/empty as
/usr/share is intended to be NFS-(un)mountable.  /var/empty is going to
be available on OpenBSD as well.  /usr/share/empty is for Red Hat Linux
compatibility and should no longer be used by new Owl packages.

* Sun Sep 02 2001 Solar Designer <solar@owl.openwall.com>
- 1771 for /var/spool/mail

* Sat Mar 31 2001 Solar Designer <solar@owl.openwall.com>
- Provide /usr/share/empty (an always-empty directory for chroots).

* Wed Dec 20 2000 Solar Designer <solar@owl.openwall.com>
- Obsoletes: and Provides: filesystem to permit for upgrades from RH.

* Wed Jul 26 2000 Solar Designer <solar@owl.openwall.com>
- Initial version.
