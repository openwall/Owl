# $Id: Owl/packages/console-tools/Attic/console-tools.spec,v 1.8 2000/12/18 15:17:24 kad Exp $

%define CTVER	0.3.3
%define	CDVER	1999.08.29
%define DATA 	console-data-%{CDVER}

Summary: 	Tools for configuring the console.
Name: 		console-tools
Version: 	19990829
Release: 	27owl
Group: 		Applications/System
Exclusiveos: 	Linux
Copyright: 	GPL
URL: 		http://www.altern.org/ydirson/en/lct/
Source0: 	ftp://lct.sourceforge.net/pub/lct/dev/console-tools-%{CTVER}.tar.gz
Source1: 	ftp://metalab.unc.edu/pub/Linux/system/keyboards/%{DATA}.tar.gz
Source2:	keytable.init
Source3: 	ftp://ftp.dementia.org/pub/linux/pc2sun.pl
Source4: 	console-tools-1998.08.11.add-ons-nosk.tar.gz
Source5: 	console-tools-0.3.3.sunfonts.tar.gz
Source6: 	kbd-1.03wip-turkish.tar.gz
Source7: 	kbd-ro.map.gz
Source8: 	kbd-sr.map.gz
Source9: 	ucw-fonts-1.1.1.tar.gz
Source10: 	kbd-0.96-latin0.tar.gz
Source11: 	kbd-0.96-amiga.tar.gz
Source12: 	sunt4-no-latin1.map.gz
Source13: 	lat2u-font.tar.gz
Source14: 	data-addon.tar.gz
Source15: 	console-fonts-cyr.tar.gz
Source16: 	keymaps-mdkre.tar.bz2
Source17:	setsysfont
Patch0: 	console-tools-1999.08.29-rh-sparc.diff
Patch1: 	console-tools-1999.08.29-rh-fonts.diff
# Euro support
Patch2: 	console-tools-1999.08.29-rh-euro.diff
# Allow consolechars & loadkeys to run from the root partition
Patch3: 	console-tools-1999.08.29-rh-rootpart.diff
# Add /etc/sysconfig/console (without subdirs) to the search path
Patch4: 	console-tools-1999.08.29-rh-searchpath.diff
Patch5: 	console-tools-1999.08.29-rh-resizecons.diff
# Fix acm handling. Duh.
Patch6: 	console-tools-1999.08.29-rh-acm.diff
# fix delete key behaviour on type4/5 keyboards on sun to match intel
Patch7: 	console-tools-1999.08.29-rh-fixdel.diff
Patch8: 	console-tools-1999.08.29-rh-unicyr.diff
# Fix psfgettable on BE
Patch9: 	console-tools-1999.08.29-rh-psfgettable.diff
# Fix setkeycodes parameter parsing
Patch10: 	console-tools-2000.07.05-rh-setkeycodes.diff
# Teach ACM reader to cope with glibc 2.2 /usr/share/i18n/charmaps format
Patch11: 	console-tools-1999.08.29-rh-readacm-glibc22.diff
Patch12: 	console-tools-1999.08.29-rh-jp106.diff
Patch13: 	console-tools-1999.08.29-rh-se-no-deadkeys.diff
# slovene charset fix
Patch14: 	console-tools-1999.08.29-rh-slovene.diff
# Russian keyboards fixes.
Patch15: 	console-tools-1999.08.29-bcl-russian-keyboards.diff
Prereq: 	/sbin/chkconfig fileutils sed
Obsoletes: 	kbd
Provides: 	kbd
BuildRoot: 	/var/rpm-buildroot/%{name}-root

%description
The console-tools package contains tools for managing a Linux
system's console's behavior, including the keyboard, the screen
fonts, the virtual terminals and font files.

%prep
%ifarch m68k
%setup -q -n console-tools-%{CTVER} -a 4 -a 6 -a 9 -a 10 -a 11 -a 13 -a 14 -a 15
%else
%setup -q -n console-tools-%{CTVER} -a 4 -a 6 -a 9 -a 10 -a 13 -a 14 -a 15
%endif
mv -f data %{DATA}
mv -f consolefonts/* %{DATA}/consolefonts
mv -f console-fonts-cyr/consolefonts/* %{DATA}/consolefonts
mv -f console-fonts-cyr/consoletrans/* %{DATA}/consoletrans
tar xzf %{SOURCE1}
mv -f %{DATA} data
tar xzf %{SOURCE5}
mv -f data %{DATA}

%ifarch sparc sparcv9 sparc64
%patch0 -p1
%endif

cd %{DATA}
%patch1 -p1
%patch2 -p1 -b .euro
cd ..
%patch3 -p1 -b .rootpart
%patch4 -p1 -b .searchpath
%patch5 -p1 -b .resizecons
%patch6 -p1 -b .acmpatch
%patch7 -p1 -b .fixdel
%patch8 -p1 -b .unicyr
%patch9 -p1 -b .psfgettable
%patch10 -p2 -b .setkeycodes
%patch11 -p1 -b .acmglibc22
%patch12 -p1 -b .jp106
%patch13 -p1 -b .keymaps
%patch14 -p1 -b .9630
%patch15 -p1 -b .bcl

%build
%ifarch %ix86
DISABLE_RESIZECONS=
%else
DISABLE_RESIZECONS=--disable-resizecons
%endif

cd %{DATA}
libtoolize --copy --force
CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -static" LDFLAGS="-static" ./configure \
	--prefix=/usr \
	--datadir='${prefix}/lib/kbd' \
	--enable-localdatadir=/etc/sysconfig/console \
	--mandir=$RPM_BUILD_ROOT%{_mandir} \
	$DISABLE_RESIZECONS
cd ..
libtoolize --copy --force
CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -static" LDFLAGS="-static" ./configure \
	--prefix=/usr \
	--datadir='${prefix}/lib/kbd' \
	--enable-localdatadir=/etc/sysconfig/console \
	--mandir=$RPM_BUILD_ROOT%{_mandir} \
	$DISABLE_RESIZECONS
cd %{DATA}
make CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE" LDFLAGS=-s prefix=/usr
cd ..
make CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE" LDFLAGS=-s prefix=/usr

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{usr,bin,etc/rc.d/init.d}

# Don't ship zero-length documentation
find doc %{DATA}/doc -size 0b -type f -print0 | xargs -0 rm -f --

cd %{DATA}
make install prefix=$RPM_BUILD_ROOT/usr
cd ..
make install prefix=$RPM_BUILD_ROOT/usr

# XXX hotwire some fonts on sun
%ifarch sparc sparcv9 sparc64
XXXFONTS="
	RUSCII_8x14.psf.gz RUSCII_8x16.psf.gz RUSCII_8x8.psf.gz
	koi8u-8x14.psf.gz koi8u-8x16.psf.gz koi8u-8x8.psf.gz
	lat2u-16.psf.gz lat5-12.psf.gz lat5-14.psf.gz lat5-16.psf.gz 
	ucw08.psf.gz  ucw11m.psf.gz ucw11z.psf.gz ucw16.psf.gz
"
make -C %{DATA}/consolefonts $XXXFONTS
for F in $XXXFONTS; do
	install -c -m 0644 %{DATA}/consolefonts/$F \
		$RPM_BUILD_ROOT/usr/lib/kbd/consolefonts/$F
done
%endif

strip $RPM_BUILD_ROOT/usr/bin/* || :

# don't give loadkeys SUID perms
chmod 755 $RPM_BUILD_ROOT/usr/bin/loadkeys

# other keymaps
for map in ro sr; do
	install -m 644 $RPM_SOURCE_DIR/kbd-$map.map.gz \
		$RPM_BUILD_ROOT/usr/lib/kbd/keymaps/i386/qwerty/$map.kmap.gz
done

tar Ixvf $RPM_SOURCE_DIR/keymaps-mdkre.tar.bz2 \
	-C $RPM_BUILD_ROOT/usr/lib/kbd/

install -m 644 $RPM_SOURCE_DIR/sunt4-no-latin1.map.gz \
	$RPM_BUILD_ROOT/usr/lib/kbd/keymaps/sun/sunt4-no-latin1.map.gz

install -m 700 $RPM_SOURCE_DIR/keytable.init \
	$RPM_BUILD_ROOT/etc/rc.d/init.d/keytable

pushd $RPM_BUILD_ROOT/usr/bin
for foo in loadkeys consolechars; do
	mv $foo ../../bin
	ln -s ../../bin/$foo
done
popd

%ifarch sparc sparcv9 sparc64
install -c -m 755 $RPM_SOURCE_DIR/pc2sun.pl $RPM_BUILD_ROOT/usr/lib/kbd/keytables
%endif

%ifnarch %ix86
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/resizecons.8
%endif

chmod +x $RPM_BUILD_ROOT/usr/lib/*.so*
strip --strip-unneeded -R .comments $RPM_BUILD_ROOT/usr/lib/*.so*

ln -sf lat0-sun16.psf.gz \
	$RPM_BUILD_ROOT/usr/lib/kbd/consolefonts/lat1-sun16.psf.gz
ln -sf lat0-sun16.psf.gz \
	$RPM_BUILD_ROOT/usr/lib/kbd/consolefonts/lat5-sun16.psf.gz
gzip -9 < %{DATA}/consolefonts/cyr-sun16.psf \
	> $RPM_BUILD_ROOT/usr/lib/kbd/consolefonts/cyr-sun16.psf.gz

install -c -m 755 %{SOURCE17} $RPM_BUILD_ROOT/sbin/setsysfont

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/sbin/chkconfig --add keytable
if [ -f /etc/sysconfig/keyboard ]; then
    . /etc/sysconfig/keyboard
    if [ -n "$KEYTABLE" ]; then
	KT=`echo $KEYTABLE | sed -e "s/.*\///g" | sed -e "s/\..*//g"`
	echo "KEYTABLE=$KT" > /etc/sysconfig/keyboard
    fi
fi
if [ -f /etc/sysconfig/i18n ]; then
    . /etc/sysconfig/i18n
    if [ -d /etc/sysconfig/console ]; then
	if [ -n "$SYSFONT" ]; then
	    cp -f /usr/lib/kbd/consolefonts/$SYSFONT* /etc/sysconfig/console
	fi
	if [ -n "$UNIMAP" ]; then
	    cp -f /usr/lib/kbd/consoletrans/$UNIMAP* /etc/sysconfig/console
	fi
	if [ -n "$SYSFONTACM" ]; then 
	    cp -f /usr/lib/kbd/consoletrans/$SYSFONTACM* /etc/sysconfig/console
	fi
    fi
fi

%preun
if [ $1 -eq 0 ]; then
	/sbin/chkconfig --del keytable
fi

%postun -p /sbin/ldconfig

%triggerpostun -- kbd
/sbin/chkconfig --add keytable

%triggerpostun -- console-tools <= 19990829-15
/sbin/chkconfig --add keytable

%files
%defattr(-,root,root)

%doc README NEWS RELEASE BUGS TODO
%doc doc/[cdf]* %{DATA}/doc/[cdf]* %{DATA}/doc/keymaps
%doc doc/README* %{DATA}/doc/README* doc/*.txt

%config /etc/rc.d/init.d/keytable
/sbin/setsysfont
/usr/lib/*
/bin/consolechars
/bin/loadkeys
/usr/bin/charset
/usr/bin/chvt
/usr/bin/openvt
/usr/bin/codepage
/usr/bin/consolechars
/usr/bin/deallocvt
/usr/bin/dumpkeys
/usr/bin/fgconsole
%ifarch %ix86
/usr/bin/fix_bs_and_del
%endif
/usr/bin/getkeycodes
/usr/bin/kbd_mode
/usr/bin/loadkeys
/usr/bin/loadunimap
/usr/bin/mk_modmap
/usr/bin/mapscrn
/usr/bin/psfaddtable
/usr/bin/psfgettable
/usr/bin/psfstriptable
%ifarch %ix86
/usr/bin/resizecons
%endif
/usr/bin/saveunimap
/usr/bin/screendump
/usr/bin/setfont
/usr/bin/setkeycodes
/usr/bin/setleds
/usr/bin/setmetamode
/usr/bin/setvesablank
/usr/bin/showcfont
/usr/bin/showkey
/usr/bin/unicode_start
/usr/bin/unicode_stop
/usr/bin/vcstime
/usr/bin/vt-is-UTF8
/usr/bin/writevt

%{_mandir}/man1/*
%{_mandir}/man4/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%changelog
* Fri Dec 15 2000 Solar Designer <solar@owl.openwall.com>
- More spec file and startup script cleanups.
- sparcv9

* Thu Dec 14 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import from BCL 7.0
- spec cleanup

* Thu Dec 14 2000 Leon Kanter <leon@blackcatlinux.com>
- russian keyboards fix

* Sun Dec 10 2000 Alexandr D. Kanevskiy <kad@blackcatlinux.com>
- import from RH
- spec cleanup

* Sun Aug 27 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- really fix up Swedish, Danish and Norwegian layout (Bug #15388)

* Mon Aug 14 2000 Preston Brown <pbrown@redhat.com>
- absolute --> relative symlinks (#16128)

* Wed Aug  9 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up slovene keymap (Bug #9630)

* Mon Aug  7 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix some more keys in Swedish, Danish and Norwegian layout (Bug #15388)

* Sat Aug 05 2000 Bill Nottingham <notting@redhat.com>
- take out condrestart; it's rather silly in this case

* Thu Aug  3 2000 Matt Wilson <msw@redhat.com>
- disable the windowskeys thing *again*, someone blew away my revert

* Thu Aug  3 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix some keys in Swedish, Danish and Norwegian layout (Bug #14566)

* Wed Jul 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add openvt (Bug #13231)
- Fix jp106 keymap (Bug #10831)

* Mon Jul 17 2000 Jakub Jelinek <jakub@redhat.com>
- make it parse new glibc 2.2 format of /usr/share/i18n/charmaps

* Sat Jul 15 2000 Bill Nottingham <notting@redhat.com>
- move initscript back

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Wed Jul  5 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix parameter handling in setkeycodes (Bug #13507)

* Mon Jun 25 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up initscript

* Mon Jun 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- FHSify
- update URL

* Tue May  2 2000 Bill Nottingham <notting@redhat.com>
- libtoolize tweaks for ia64

* Mon Mar  6 2000 Jakub Jelinek <jakub@redhat.com>
- New -sun16 fonts (cyr-sun16 plus a few modifications
  to lat0-sun16 and lat2-sun16; lat5-sun16 merged into lat0-sun16)
- koi8-r and koi8-u acm maps
- Fix an endianess bug in psfgettable

* Thu Mar  2 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Fix up support for Russian (Bugs #9898 and #9908)
  Seems console-tools can't handle gzip'ing on all file types.

* Tue Feb 29 2000 Preston Brown <pbrown@redhat.com>
- the delete key mapping on sun type 4/5 keyboards matches intel now.

* Fri Feb 25 2000 Cristian Gafton <gafton@redhat.com>
- update romanian keyboard

* Fri Feb 25 2000 Jakub Jelinek <jakub@redhat.com>
- Fix acm loading, so it is able to cope again with
  what previous console-tools were loading and not only
  wg-15 glibc format.
- Painted yet another Turkish font compatible with lat0-sun16.

* Thu Feb 24 2000 Matt Wilson <msw@redhat.com>
- updated Turkish font

* Thu Feb 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up support for Russian
  (fonts from leon@geon.donetsk.ua, Bug #9519)

* Fri Feb  4 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Rebuild to compress man pages
- strip libraries

* Wed Jan 11 2000 Bill Nottingham <notting@redhat.com>
- fix some of the old patches

* Fri Nov  5 1999 Bernhard Rosenkränzer <bero@redhat.com>
- Update to console-tools 0.3.3 and console-data 1999.08.29
- Euro support
- Support for Windoze keys (used to switch between ttys)

* Sun Sep  5 1999 Jeff Johnson <jbj@redhat.com>
- fix resizecons (#3986).
- consolechars can't handle gzipped old format koi8u2ruscii (#4022).

* Mon Aug 23 1999 Bill Nottingham <notting@redhat.com>
- a directory is not a keymap.

* Fri Aug 20 1999 Bill Nottingham <notting@redhat.com>
- triggerpostun on kbd so we don't lose our chkconfig links

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- initscript munging

* Thu Apr 15 1999 Bill Nottingham <notting@redhat.com>
- make keytable %post handle us.map better

* Thu Apr 15 1999 Jeff Johnson <jbj@redhat.com>
- hotwire sun fonts.

* Wed Apr 14 1999 Bill Nottingham <notting@redhat.com>
- %post changes; just copy the user's configured font/map/etc.

* Wed Apr 14 1999 Matt Wilson <msw@redhat.com>
- added fonts RUSCII_*, koi8u_*, and acm koi8u2ruscii from
  Leon Kanter <leon@geon.donetsk.ua>

* Mon Apr 12 1999 Bill Nottingham <notting@redhat.com>
- removed sh-utils from prereq.
- added sed to prereq

* Fri Apr  9 1999 Jeff Johnson <jbj@redhat.com>
- more latin2 fonts (Peter Ivanyi).

* Thu Apr  8 1999 Bill Nottingham <notting@redhat.com>
- added sh-utils to prereq.

* Mon Apr  5 1999 Bill Nottingham <notting@redhat.com>
- /etc/sysconfig/console support
- add setsysfont to init script

* Mon Mar 29 1999 Peter Ivanyi <ivanyi@internet.sk>
- more fixes.

* Thu Mar 25 1999 Peter Ivanyi <ivanyi@internet.sk>
- add ucw-fonts-1.1.tar.gz
- delete obsolete sk keymaps from console-tools-1998.08.11.add-ons.

* Mon Mar 22 1999 Preston Brown <pbrown@redhat.com>
- added norwegian sun4 keymap support

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Fri Mar 12 1999 Jeff Johnson <jbj@redhat.com>
- update to 1999.03.02.

* Tue Feb 16 1999 Jeff Johnson <jbj@redhat.com>
- repackage for Red Hat 6.0

* Wed Jan 30 1999 Alex deVries <puffin@redhat.com>
- added amiga support for Jes Sorensen

* Mon Dec 07 1998 Jakub Jelinek <jj@ultra.linux.cz>
- some keymaps were including "*.map", which has to be
  replaced by "*.kmap"

* Fri Dec 04 1998 Jakub Jelinek <jj@ultra.linux.cz>
- upgrade to console-tools, added new sun keymaps,
  new sun fonts for latin0/1 and latin2, iso15.acm
  and iso02+euro.acm.
- Print the verbose messages only if verbose was 
  specified on command line.

* Thu Oct 01 1998 Cristian Gafton <gafton@redhat.com>
- added Euro (latin0) support from Guylhem Aznar

* Sun Sep 27 1998 Cristian Gafton <gafton@redhat.com>
- fix the name the ro and sr maps are installed under
- slovak keymaps
- ro.map and sr.map are welcomed to the club
- enable turkish again

* Mon Aug 24 1998 Cristian Gafton <gafton@redhat.com>
- KEYTABLE should not have the full patch name (%post hack)

* Fri Aug 21 1998 Jeff Johnson <jbj@redhat.com>
- install keymaps on tty0 w/o using (non-installed) open(1).

* Tue Jul 14 1998 Jeff Johnson <jbj@redhat.com>
- updated to 0.96a.

* Thu Jun 11 1998 Mikael Hedin <micce@irf.se>
- specify VT0 in case we use a serial console

* Wed Jun 10 1998 Jeff Johnson <jbj@redhat.com>
- quotes permit multiple keytables in keytable.init (problem #675)

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu May 07 1998 Donnie Barnes <djb@redhat.com>
- added some extra turkish support

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- fixes for building on alpha
- completed buildroot usage

* Thu Apr 23 1998 Michael K. Johnson <johnsonm@redhat.com>
- enhanced initscript

* Wed Apr 08 1998 Erik Troan <ewt@redhat.com>
- updated to 0.95

* Wed Mar 25 1998 Erik Troan <ewt@redhat.com>
- fixed /tmp exploit

* Wed Nov 05 1997 Donnie Barnes <djb@redhat.com>
- added SPARC stuff (finally!), Thanks to eduardo@medusa.es for most of it.
- added buildroot
- cleaned up the file list
- moved to rev 5 because the contrib ver rel was 4

* Mon Oct 20 1997 Donnie Barnes <djb@redhat.com>
- updated from 0.91 to 0.94
- added chkconfig support
- spec file cleanups

* Tue Jun 17 1997 Erik Troan <ewt@redhat.com>
- built against glibc
