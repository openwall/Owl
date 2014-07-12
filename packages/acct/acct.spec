# $Owl: Owl/packages/acct/acct.spec,v 1.43 2014/07/12 14:08:05 galaxy Exp $

Summary: Utilities for monitoring process activities.
Name: acct
Version: 6.5.4
Release: owl2
License: GPLv3+
Group: Applications/System
Source0: ftp://ftp.gnu.org/gnu/acct/%name-%version.tar.gz
Source1: dump-acct.8
Source2: %name.init
Source3: %name.logrotate
Patch0: %name-6.5.4-owl-doc.diff
Patch1: %name-6.5.4-owl-devpts.diff
Patch2: %name-6.5.4-owl-sa-help.diff
Patch3: %name-6.5.4-owl-info.diff
Patch4: %name-6.5.4-alt-time_t.diff
Patch5: %name-6.5.4-alt-program_name.diff
Patch6: %name-6.5.4-alt-owl-warnings.diff
Patch7: %name-6.5.4-owl-gettext.diff
Patch8: %name-6.5.4-owl-texi.diff
Requires(pre): /sbin/install-info
Requires: grep, coreutils >= 5.3.0, sed >= 4.0.9
Provides: psacct
Obsoletes: psacct
BuildRequires: sed >= 4.0.9, texinfo
BuildRoot: /override/%name-%version

%description
The acct package contains several utilities for monitoring process
activities, including ac, lastcomm, accton and sa.  The ac command
displays statistics about how long users have been logged on.  The
lastcomm command displays information about previous executed commands.
The accton command turns process accounting on or off.  The sa command
summarizes information about previously executed commands.

%prep
%setup -q
rm *.info
sed -i 's/\<getopt[1]\?\.[hc]\>//g' Makefile.am
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
autoreconf -fis
%configure
%__make

%install
rm -rf %buildroot
mkdir -p %buildroot/etc/{rc.d/init.d,logrotate.d}
mkdir -p %buildroot{/sbin,%_bindir,%_sbindir,%_mandir}
mkdir -p %buildroot%_var/account
%makeinstall
install -m 644 %_sourcedir/dump-acct.8 %buildroot%_mandir/man8/
install -m 755 %_sourcedir/acct.init %buildroot/etc/rc.d/init.d/acct
install -m 644 %_sourcedir/acct.logrotate \
	%buildroot/etc/logrotate.d/acct

# Move accton to /sbin -- leave historical symlink
mv %buildroot%_sbindir/accton %buildroot/sbin/accton
ln -s ../../sbin/accton %buildroot%_sbindir/accton

# Because of the last command conflicting with the one from SysVinit
mv %buildroot%_bindir/last %buildroot%_bindir/last-acct
mv %buildroot%_mandir/man1/last.1 \
	%buildroot%_mandir/man1/last-acct.1

touch %buildroot%_var/account/{pacct,usracct,savacct}

# Remove unpackaged files
rm %buildroot%_infodir/dir

%post
# We need this hack to get rid of an old, incorrect accounting info entry
# when installing over older versions of Red Hat Linux.
INFODIRFILE=%_infodir/dir
if grep -q '^\* accounting: (psacct)' $INFODIRFILE; then
	INFODIRFILE="$(readlink -e $INFODIRFILE)"
	sed -i '/^\* accounting: (psacct)/d' "$INFODIRFILE"
fi

/sbin/install-info %_infodir/accounting.info %_infodir/dir

umask 177
for f in %_var/account/{pacct,usracct,savacct}; do
	test -e $f && continue || :
	touch $f
	chown root:root $f
	chmod 600 $f
done

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/accounting.info %_infodir/dir
fi

%files
%defattr(-,root,root)
%ghost %attr(0600,root,root) %_var/account/pacct
%ghost %attr(0600,root,root) %_var/account/usracct
%ghost %attr(0600,root,root) %_var/account/savacct
%attr(0644,root,root) %config(noreplace) /etc/logrotate.d/*
%config /etc/rc.d/init.d/acct
/sbin/accton
%_sbindir/*
%_bindir/*
%_mandir/*/*
%_infodir/*

%changelog
* Sat Jun 28 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 6.5.4-owl2
- Regenerated the owl-info patch since it was fuzzy.

* Wed Sep 01 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 6.5.4-owl1
- Updated to 6.5.4.
- Updated patches.
- Commented out unrecognized autoconf directives.

* Sun Oct 07 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 6.4-owl0.5
- Fixed compilation warnings.

* Tue Aug 08 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 6.4-owl0.4
- Fixed "/etc/rc.d/init.d/acct stop" to really turn off accounting.

* Fri Jun 16 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 6.4-owl0.3
- Adjusted the logrotate configuration file to redirect stdout to /dev/null.

* Sun May 21 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 6.4-owl0.2
- Added @dircategory and @direntry to texinfo file, simplified info
file installation.
- Fixed casts to (time_t *).
- Enforced build with system getopt.

* Fri May 19 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 6.4-owl0.1
- Updated to 6.4-pre1.
- Re-generated patches.

* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 6.3.5-owl15
- Corrected info files installation.

* Wed Jan 05 2005 (GalaxyMaster) <galaxy-at-owl.openwall.com> 6.3.5-owl14
- /var/account is owned by owl-hier and uses more restrictive permissions,
so I've removed it from this package.
- Cleaned up the spec for consistency.

* Wed Jul 21 2004 Michail Litvak <mci-at-owl.openwall.com> 6.3.5-owl13
- Use sed -i.

* Thu Feb 26 2004 Michail Litvak <mci-at-owl.openwall.com> 6.3.5-owl12
- Don't call autoconf.

* Mon May 05 2003 Solar Designer <solar-at-owl.openwall.com> 6.3.5-owl11
- Added a patch from Denis Ducamp to support /dev/pts in lastcomm(1).

* Mon Aug 19 2002 Michail Litvak <mci-at-owl.openwall.com>
- Deal with info dir entries such that the menu looks pretty.

* Mon Aug 05 2002 Solar Designer <solar-at-owl.openwall.com>
- Use a more generic script to remove the obsolete info dir entry.

* Sun Mar 24 2002 Solar Designer <solar-at-owl.openwall.com>
- Heavy documentation corrections and cleanups (both man pages and texinfo).
- Minor spec file cleanups.

* Fri Mar 22 2002 Michail Litvak <mci-at-owl.openwall.com>
- Fixed sa(8) to properly report real time in minutes or seconds.
- Fixes to build with -Wall cleanly.

* Thu Jan 24 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Sat Apr 14 2001 Solar Designer <solar-at-owl.openwall.com>
- Preserve permissions of /etc/info-dir when modifying it in %post.

* Thu Apr 12 2001 Solar Designer <solar-at-owl.openwall.com>
- acct.logrotate: nocreate (we create the file from the postrotate script).

* Wed Apr 11 2001 Michail Litvak <mci-at-owl.openwall.com>
- added chkconfig support in init script
- improved logrotate config
- more cleanups...

* Sun Apr 08 2001 Michail Litvak <mci-at-owl.openwall.com>
- spec cleanups
- acct.logrotate and acct.init was rewritten
- Obsoletes: psacct
- Use %%ghost for /var/account/*

* Mon Apr 02 2001 Michail Litvak <mci-at-owl.openwall.com>
- Imported spec from RH (some parts from Mandrake)
- update to 6.3.5, fixed source location
- dump-acct, dump-utmp manpages from Debian
