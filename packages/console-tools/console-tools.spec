# $Id: Owl/packages/console-tools/Attic/console-tools.spec,v 1.12 2002/02/07 18:07:46 solar Exp $

%define CTVER 0.3.3
%define	CDVER 1999.08.29
%define DATA console-data-%{CDVER}

Summary: Tools for configuring the console.
Name: console-tools
Version: 19990829
Release: owl28
Group: Applications/System
License: GPL
URL: http://www.altern.org/ydirson/en/lct/
Source0: ftp://lct.sourceforge.net/pub/lct/dev/console-tools-%{CTVER}.tar.gz
Source1: ftp://metalab.unc.edu/pub/Linux/system/keyboards/%{DATA}.tar.gz
Source2: keytable.init
Source3: ftp://ftp.dementia.org/pub/linux/pc2sun.pl
Source4: console-tools-1998.08.11.add-ons-nosk.tar.gz
Source5: console-tools-0.3.3.sunfonts.tar.gz
Source6: kbd-1.03wip-turkish.tar.gz
Source7: kbd-ro.map.gz
Source8: kbd-sr.map.gz
Source9: ucw-fonts-1.1.1.tar.gz
Source10: kbd-0.96-latin0.tar.gz
Source11: kbd-0.96-amiga.tar.gz
Source12: sunt4-no-latin1.map.gz
Source13: lat2u-font.tar.gz
Source14: data-addon.tar.gz
Source15: console-fonts-cyr.tar.gz
Source16: keymaps-mdkre.tar.bz2
Source17: setsysfont
Patch0: console-tools-1999.08.29-rh-sparc.diff
Patch1: console-tools-1999.08.29-rh-fonts.diff
# Euro support
Patch2: console-tools-1999.08.29-rh-euro.diff
# Allow consolechars & loadkeys to run from the root partition
Patch3: console-tools-1999.08.29-rh-rootpart.diff
# Add /etc/sysconfig/console (without subdirs) to the search path
Patch4: console-tools-1999.08.29-rh-searchpath.diff
Patch5: console-tools-1999.08.29-rh-resizecons.diff
# Fix acm handling. Duh.
Patch6: console-tools-1999.08.29-rh-acm.diff
# fix delete key behaviour on type4/5 keyboards on sun to match intel
Patch7: console-tools-1999.08.29-rh-fixdel.diff
Patch8: console-tools-1999.08.29-rh-unicyr.diff
# Fix psfgettable on BE
Patch9: console-tools-1999.08.29-rh-psfgettable.diff
# Fix setkeycodes parameter parsing
Patch10: console-tools-2000.07.05-rh-setkeycodes.diff
# Teach ACM reader to cope with glibc 2.2 /usr/share/i18n/charmaps format
Patch11: console-tools-1999.08.29-rh-readacm-glibc22.diff
Patch12: console-tools-1999.08.29-rh-jp106.diff
Patch13: console-tools-1999.08.29-rh-se-no-deadkeys.diff
# slovene charset fix
Patch14: console-tools-1999.08.29-rh-slovene.diff
# Russian keyboards fixes.
Patch15: console-tools-1999.08.29-bcl-russian-keyboards.diff
PreReq: /sbin/ldconfig, /sbin/chkconfig
Provides: kbd
Obsoletes: kbd
BuildRoot: /override/%{name}-%{version}

%description
The console-tools package contains tools for managing a Linux system's
console's behavior, including the keyboard, the screen fonts, the virtual
terminals and font files.

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
%patch2 -p1
cd ..
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p2
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1

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
mkdir -p $RPM_BUILD_ROOT/{usr,bin,sbin,etc/rc.d/init.d}

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

%preun
if [ $1 -eq 0 ]; then
	/sbin/chkconfig --del keytable
fi

%postun -p /sbin/ldconfig

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
* Thu Jan 24 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.
- Dropped some Red Hat's backwards compatibility hacks.

* Sat Mar 31 2001 Solar Designer <solar@owl.openwall.com>
- setsysfont: pass multiple arguments to consolechars correctly.

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
