# $Id: Owl/packages/mutt/mutt.spec,v 1.11 2004/02/12 23:38:58 mci Exp $

Summary: A feature-rich text-based mail user agent.
Name: mutt
Version: 1.4.2.1
Release: owl1
License: GPL
Group: Applications/Internet
URL: http://www.mutt.org
Source0: ftp://ftp.mutt.org/mutt/mutt-%{version}i.tar.gz
Source1: Muttrc-color
Patch0: mutt-1.4-owl-no-sgid.diff
Patch1: mutt-1.4-owl-muttbug-tmp.diff
Patch2: mutt-1.4.2.1-owl-tmp.diff
Requires: mktemp >= 1:1.3.1
Conflicts: mutt-us
Provides: mutt-i
BuildRoot: /override/%name-%version

%description
Mutt is a feature-rich text-based mail user agent.  Mutt supports local
and remote mail spools (POP3 and IMAP, including with SSL), MIME, OpenPGP
(PGP/MIME) with GnuPG and PGP, colored display, threading, and a lot of
customization including arbitrary message headers, key remapping, colors,
and more.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
CFLAGS="$RPM_OPT_FLAGS" ./prepare --prefix=%_prefix \
	--with-sharedir=/etc --sysconfdir=/etc \
	--with-docdir=%_docdir/mutt-%version \
	--with-mandir=%_mandir \
	--with-infodir=%_infodir \
	--enable-pop --enable-imap \
	--with-ssl \
	--disable-domain \
	--disable-flock --enable-fcntl \
	--without-wc-funcs
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall \
	sharedir=$RPM_BUILD_ROOT/etc \
	sysconfdir=$RPM_BUILD_ROOT/etc \
	docdir=$RPM_BUILD_ROOT%_docdir/mutt-%version \
	install

# We like GPG here.
cat contrib/gpg.rc $RPM_SOURCE_DIR/Muttrc-color >> $RPM_BUILD_ROOT/etc/Muttrc

%find_lang %name

%files -f %name.lang
%defattr(-,root,root)
%config /etc/Muttrc
%doc doc/*.txt
%doc contrib/*.rc README* contrib/sample.* NEWS TODO
%doc COPYRIGHT doc/manual.txt contrib/language* mime.types
%_bindir/mutt
%_bindir/muttbug
%_bindir/flea
%_bindir/pgpring
%_bindir/pgpewrap
%_mandir/man1/mutt.*
%_mandir/man5/muttrc.*
%_mandir/man1/flea.*

%changelog
* Fri Feb 13 2004 Michail Litvak <mci@owl.openwall.com> 1.4.2.1-owl1
- 1.4.2.1 (remove -cvs patch included into release)

* Fri Jan 30 2004 Michail Litvak <mci@owl.openwall.com> 1.4.1-owl3
- Patch (from Mutt's CVS) to fix Mutt crash on certain e-mails; this can
occur when an UTF-8 locale is used on wide (more than ~120 columns)
terminals, but Owl isn't affected with its current glibc because of the
lack of UTF-8 locales support.

* Mon Oct 20 2003 Solar Designer <solar@owl.openwall.com> 1.4.1-owl2
- Build without glibc's wide character functions due to the broken locales;
in particular, with koi8-r some control characters wouldn't be treated
as such after being passed through mbrtowc() and checked with iswcntrl().

* Sun Mar 23 2003 Jarno Huuskonen <jhuuskon@owl.openwall.com> 1.4.1-owl1
- 1.4.1

* Mon Jan 20 2003 Solar Designer <solar@owl.openwall.com>
- Improved the package description.
- Require the proper version of mktemp for our muttbug/flea patch.
- Initial commit into Owl.

* Wed Jan 15 2003 Jarno Huuskonen <jhuuskon@owl.openwall.com>
- use mkstemp when creating temporary files.
- include locales and flea

* Wed Sep 25 2002 Solar Designer <solar@owl.openwall.com>
- Updated to 1.4, the package is still non-public.
- Don't use slang.

* Tue Jan 08 2002 Solar Designer <solar@owl.openwall.com>
- Based this spec file on Red Hat's, dropped most patches for now.
