# $Id: Owl/packages/kbd/kbd.spec,v 1.3 2003/04/18 23:35:55 mci Exp $

Summary: Tools for configuring the console.
Name: kbd
Version: 1.08
Release: owl1
License: GPL
Group: System Environment/Base
Source0: ftp://ftp.kernel.org/pub/linux/utils/kbd/kbd-%{version}.tar.bz2
Source1: kbd-latsun-fonts.tar.bz2
Source2: keytable.init
Source3: setsysfont
Patch0: kbd-1.08-rh-compose.diff
Patch1: kbd-1.08-rh-other-vt.diff
Patch2: kbd-1.08-rh-sparc.diff
Patch3: kbd-1.08-rh-speakup.diff
Patch4: kbd-1.08-rh-terminal.diff
Patch5: kbd-1.08-rh-owl-install-no-root.diff
PreReq: /sbin/chkconfig, /sbin/ldconfig
Conflicts: util-linux < 2.11
Provides: console-tools
Obsoletes: console-tools
BuildRequires: bison, flex
BuildRoot: /override/%{name}-%{version}

%description
This package contains tools for managing a Linux system's console's
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

%build
./configure --prefix=$RPM_BUILD_ROOT \
	--datadir=/lib/kbd \
	--mandir=%{_mandir} \
	--disable-nls

make CFLAGS="$RPM_OPT_FLAGS" LDFLAGS=-s DATA_DIR=/lib/kbd

%install
rm -rf $RPM_BUILD_ROOT

make install BINDIR=$RPM_BUILD_ROOT%{_bindir}

# Obsolete
rm -fv $RPM_BUILD_ROOT%{_bindir}/resizecons

cd $RPM_BUILD_ROOT
for binary in setfont dumpkeys kbd_mode unicode_start unicode_stop; do
	mv .%{_bindir}/$binary bin/
done

mkdir -p {sbin,etc/rc.d/init.d}
install -m 700 $RPM_SOURCE_DIR/keytable.init etc/rc.d/init.d/keytable
install -m 755 $RPM_SOURCE_DIR/setsysfont sbin/setsysfont

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
%doc CHANGES CREDITS README
%doc doc/*.txt doc/kbd.FAQ*.html
%doc doc/font-formats/
%doc doc/utf/
%config /etc/rc.d/init.d/keytable
/sbin/setsysfont
/bin/*
%{_bindir}/*
%{_mandir}/man*/*
/lib/kbd/*

%changelog
* Thu Apr 17 2003 Michail Litvak <mci@owl.openwall.com>
- Obsoletes console-tools package, but derive kbdtable.init from it.
- spec based on RH
- spec files cleanups
