# $Id: Owl/packages/kbd/kbd.spec,v 1.14 2005/10/20 23:26:46 galaxy Exp $

Summary: Tools for configuring the console.
Name: kbd
Version: 1.12
Release: owl1
License: GPL
Group: System Environment/Base
Source0: ftp://ftp.kernel.org/pub/linux/utils/kbd/kbd-%version.tar.bz2
Source1: kbd-latsun-fonts.tar.bz2
Source2: keytable.init
Source3: setsysfont
Patch0: kbd-1.08-rh-compose.diff
Patch1: kbd-1.08-rh-rukbd.diff
Patch2: kbd-1.08-owl-rh-sparc.diff
Patch3: kbd-1.08-rh-speakup.diff
Patch4: kbd-1.08-rh-terminal.diff
Patch5: kbd-1.12-rh-alias.diff
Patch6: kbd-1.12-rh-dir.diff
Patch7: kbd-1.12-rh-setfont-man.diff
Patch8: kbd-1.12-rh-Meta_utf8.diff
Patch9: kbd-1.12-owl-install-fix.diff
Patch10: kbd-1.12-alt-cleanup.diff
Patch11: kbd-1.12-alt-plainletter-safer.diff
Patch12: kbd-1.12-deb-po-makefile.diff
Patch13: kbd-1.12-deb-man-pages.diff
Patch14: kbd-1.12-deb-kmap-suffix.diff
Patch15: kbd-1.12-deb-defkeymap.diff
Patch16: kbd-1.12-deb-uni-suffix.diff
Patch17: kbd-1.12-deb-canonical-syms.diff
Patch18: kbd-1.12-deb-main-argc.diff
Patch19: kbd-1.12-deb-kbdrate-notty.diff
Patch20: kbd-1.12-deb-charsets0.diff
PreReq: /sbin/chkconfig, /sbin/ldconfig
Conflicts: util-linux < 2.11
Provides: console-tools
Obsoletes: console-tools
BuildRequires: bison, flex, sed >= 4.0.9
BuildRoot: /override/%name-%version

%description
This package contains tools for managing a Linux system console's
behavior, including the keyboard, the screen fonts, the virtual terminals,
and font files.

%prep
%setup -q -a 1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1

# 7-bit maps are obsolete; so are non-euro maps
cd data/keymaps/i386

mv qwerty/fi.map qwerty/fi-old.map
cp qwerty/fi-latin9.map qwerty/fi.map
cp qwerty/pt-latin9.map qwerty/pt.map
cp qwerty/sv-latin1.map qwerty/sv.map

mv azerty/fr.map azerty/fr-old.map
cp azerty/fr-latin9.map azerty/fr.map
cp azerty/fr-latin9.map azerty/fr-latin0.map # legasy alias

cd ../../..

sed -i -e 's,LatArCyrHeb-16,latarcyrheb-san16,' src/unicode_start

%build

# It isn't a real GNU configure script, so won't use %%configure here.
./configure --prefix=%buildroot \
	--datadir=/lib/kbd \
	--mandir=%_mandir \
	--disable-nls
# XXX: What is the reason for disabling NLS here? We are incompatible with
#      RH and other distros -- (GM)

%__make CFLAGS="%optflags" LDFLAGS=

%install
rm -rf %buildroot

%__make install \
	DESTDIR=%buildroot \
	BINDIR=%_bindir \
	LOADKEYS_BINDIR=/bin
	
# Obsolete
rm -fv %buildroot%_bindir/resizecons
rm -fv %buildroot%_mandir/man8/resizecons.8*

cd %buildroot
for binary in setfont dumpkeys kbd_mode unicode_start unicode_stop; do
	mv .%_bindir/$binary bin/
done

mkdir -p {sbin,etc/rc.d/init.d}
install -m 700 %_sourcedir/keytable.init etc/rc.d/init.d/keytable
install -m 755 %_sourcedir/setsysfont sbin/setsysfont

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
%doc CHANGES CREDITS README
%doc doc/*.txt doc/kbd.FAQ*.html
%doc doc/font-formats/
%doc doc/utf/
%config /etc/rc.d/init.d/keytable
/sbin/setsysfont
/bin/*
%_bindir/*
%_mandir/man*/*
%dir /lib/kbd
/lib/kbd/*

%changelog
* Mon Oct 17 2005 (GalaxyMaster) <galaxy@owl.openwall.com> 1.12-owl1
- Updated to 1.12.
- Merged recent patches from several distributions.
- Fixed error in the description.
- Regenerated 1st hunk of kbdrate.c patch in -owl-rh-sparc.
- Added BuildRequire on sed >= 4.0.9 due to 'sed -i'.
- From now on, this package could be compiled with kernel 2.6 headers.

* Thu Jan 15 2004 Michail Litvak <mci@owl.openwall.com> 1.08-owl5
- Make /lib/kbd directory owned by this package.

* Tue Oct 21 2003 Solar Designer <solar@owl.openwall.com> 1.08-owl4
- Dropped support for console-tools' consolechars from the setsysfont script.

* Fri Aug 01 2003 Michail Litvak <mci@owl.openwall.com> 1.08-owl3
- Fixed building on sparc architecture.

* Thu Apr 17 2003 Michail Litvak <mci@owl.openwall.com> 1.08-owl2
- Don't install resizecons man page.

* Thu Apr 17 2003 Michail Litvak <mci@owl.openwall.com>
- Obsoletes console-tools package, but derive kbdtable.init from it.
- spec based on RH
- spec files cleanups
