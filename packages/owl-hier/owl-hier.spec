# $Owl: Owl/packages/owl-hier/owl-hier.spec,v 1.27 2010/03/30 17:28:24 solar Exp $

Summary: Initial directory hierarchy.
Name: owl-hier
Version: 0.9
Release: owl1
License: public domain
Group: System Environment/Base
Source: base
Requires: owl-etc
Provides: filesystem
Obsoletes: filesystem
BuildRequires: mtree
BuildArchitectures: noarch
BuildRoot: /override/%name-%version

%description
This package contains the initial directory hierarchy for Owl, and
its corresponding mtree specification.

%install
rm -rf %buildroot
mkdir -p %buildroot

# Create the directory hierarchy
cd %buildroot
sed \
	-e "s/\(uname=\)root /\1`id -un` /" \
	-e "s/\(uname=\)root$/\1`id -un`/" \
	-e "s/\(gname=\)root /\1`id -gn` /" \
	-e "s/\(gname=\)root$/\1`id -gn`/" \
	< %_sourcedir/base |
		%_sbindir/mtree -U
if [ %_lib != lib ]; then
	mkdir -m755 %_lib .%_libdir usr/X11R6/%_lib
	mv lib/security %_lib
fi
ln -s ../var/tmp usr/tmp
ln -s ../X11R6/bin .%_bindir/X11
ln -s ../X11R6/include/X11 .%_includedir/X11
ln -s ../X11R6/lib/X11 .%_libdir/X11
ln -s log var/adm
ln -s spool/mail var/mail
install -pm600 %_sourcedir/base etc/mtree/

# Build the filelist
cd $RPM_BUILD_DIR
find %buildroot -type d | sed \
	-e "s,^%buildroot,," \
	-e 's,^,%%dir ,' > filelist.mtree
find %buildroot -type f -o -type l | sed \
	-e "s,^%buildroot,," \
	-e 's,^.*/etc,%%config &,' >> filelist.mtree

# Specify some entries manually to set user/group when building as non-root
cat << EOF > filelist
%%defattr (-,root,root)
%%dir %%attr(555,root,proc) /proc
%%dir %%attr(755,sources,sources) /usr/src
%%dir %%attr(750,build,sources) /usr/src/world
%%dir %%attr(770,root,uucp) /var/lock/uucp
%%dir %%attr(1771,root,mail) /var/spool/mail
EOF

sed -n 's,^.* \(/[^ ]*\)$,\1,p' < filelist |
while read filename; do
	grep " $filename\$" filelist.mtree || :
	grep "^$filename\$" filelist.mtree || :
done | sort > filelist.remove

sort filelist.mtree |
comm -3 - filelist.remove >> filelist

%files -f filelist

%changelog
* Tue Mar 30 2010 Solar Designer <solar-at-owl.openwall.com> 0.9-owl1
- Added /etc/skel (it was created but not owned by another package) and
/etc/profile.d (moved from owl-etc).

* Tue Apr 04 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.8-owl3
- Added x86_64 support.

* Mon Jan 10 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 0.8-owl2
- Cleaned up the spec to use macros instead of hardcoded paths in some places.

* Mon Feb 16 2004 Michail Litvak <mci-at-owl.openwall.com> 0.8-owl1
- Add some directories for FHS 2.2 compatibility.

* Fri Jan 16 2004 Michail Litvak <mci-at-owl.openwall.com> 0.7-owl1
- Added /usr/local/include.

* Sat Oct 25 2003 Solar Designer <solar-at-owl.openwall.com> 0.6-owl1
- Renamed /etc/mtree/special to /etc/mtree/base; "special" is used on *BSD,
but its meaning is different.
- Added /usr/X11R6/lib/X11 such that /usr/lib/X11 is not a dangling symlink
(even though it gets used if one installs Red Hat's XFree86 packages).
- Make symlinks relative.

* Sun Jun 09 2002 Solar Designer <solar-at-owl.openwall.com> 0.5-owl1
- Don't list /dev/pts in here, it is a part of owl-dev.

* Thu Feb 07 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Tue Sep 25 2001 Solar Designer <solar-at-owl.openwall.com>
- Provide /var/empty, which is a better choice than /usr/share/empty as
/usr/share is intended to be NFS-(un)mountable.  /var/empty is going to
be available on OpenBSD as well.  /usr/share/empty is for Red Hat Linux
compatibility and should no longer be used by new Owl packages.
- Specify group proc for /proc such that it doesn't get reset when the
package is updated on a running system and gid= was used on mount.

* Sun Sep 02 2001 Solar Designer <solar-at-owl.openwall.com>
- 1771 for /var/spool/mail

* Sat Mar 31 2001 Solar Designer <solar-at-owl.openwall.com>
- Provide /usr/share/empty (an always-empty directory for chroots).

* Wed Dec 20 2000 Solar Designer <solar-at-owl.openwall.com>
- Obsoletes: and Provides: filesystem to permit for upgrades from RH.

* Wed Jul 26 2000 Solar Designer <solar-at-owl.openwall.com>
- Initial version.
