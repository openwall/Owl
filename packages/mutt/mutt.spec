# $Owl: Owl/packages/mutt/mutt.spec,v 1.29 2014/07/12 14:14:40 galaxy Exp $

Summary: A feature-rich text-based mail user agent.
Name: mutt
Version: 1.4.2.3
Release: owl3
License: GPL
Group: Applications/Internet
URL: http://www.mutt.org
# ftp://ftp.mutt.org/mutt/mutt-%version.tar.gz
Source0: mutt-%version.tar.bz2
Source1: Muttrc-color
Patch0: mutt-1.4-owl-no-sgid.diff
Patch1: mutt-1.4-owl-muttbug-tmp.diff
Patch2: mutt-1.4.2.1-owl-tmp.diff
Patch3: mutt-1.4.2.1-owl-bound.diff
Patch4: mutt-1.4.2.1-owl-man.diff
Patch5: mutt-1.4.2.3-alt-fixes.diff
Patch6: mutt-1.4.2.3-owl-autotools.diff
Requires: mktemp >= 1:1.3.1
Conflicts: mutt-us
Provides: mutt-i
BuildRequires: ncurses-devel
BuildRequires: openssl-devel >= 0.9.7g-owl1
BuildRequires: rpm-build >= 0:4
BuildRequires: autoconf >= 2.69
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
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

autoreconf -fis -I m4

%{expand:%%define optflags %optflags -fno-strict-aliasing}

%build
export LDFLAGS=-ltinfo
%configure \
	--with-docdir=%_docdir/mutt-%version \
	--enable-pop --enable-imap \
	--with-ssl \
	--disable-domain \
	--disable-flock --enable-fcntl \
	--without-wc-funcs
%__make

%install
[ '%buildroot' != '/' -a -d '%buildroot' ] && rm -rf -- '%buildroot'
%makeinstall \
	docdir=%buildroot%_docdir/mutt-%version

# We like GPG here.
cat contrib/gpg.rc %_sourcedir/Muttrc-color >> %buildroot/%_sysconfdir/Muttrc

%find_lang %name || :
touch '%name.lang'

%files -f %name.lang
%defattr(-,root,root)
%config %_sysconfdir/Muttrc
%doc doc/*.txt
%doc contrib/*.rc README* contrib/sample.* NEWS TODO
%doc COPYRIGHT doc/manual.txt contrib/language* mime.types
%_bindir/mutt
%_bindir/muttbug
%_bindir/flea
%_bindir/pgpring
%_bindir/pgpewrap
%_mandir/man1/flea.*
%_mandir/man1/mutt.*
%_mandir/man1/muttbug.*
%_mandir/man5/mbox.*
%_mandir/man5/muttrc.*
%exclude %_sysconfdir/mime.types
%exclude %_mandir/man1/mutt_dotlock.*

%changelog
* Fri Jun 20 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1.4.2.3-owl3
- Fixed the build with new autotools (autoconf 2.69, automake 1.14).

* Sun Jul 22 2012 Vasiliy Kulikov <segoon-at-owl.openwall.com> 1.4.2.3-owl2
- Added -ltinfo into LDFLAGS to fix build error under binutils >= 2.21.

* Wed May 30 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.4.2.3-owl1
- Updated to 1.4.2.3.  This release fixes msgid validation in APOP
authentication (CVE-2007-1558) and potential buffer overflow in passwd
gecos field parser (CVE-2007-2683).

* Tue Jun 27 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.4.2.1-owl6
- Applied upstream fix for potential stack-based buffer overflow
when processing an overly long namespace from IMAP server.
- Fixed build with new gcc compiler.

* Thu Aug 25 2005 Solar Designer <solar-at-owl.openwall.com> 1.4.2.1-owl5
- Introduced the buffer non-overflow hardening into convert_to_state() itself
rather than into only one of its callers.

* Tue Jul 19 2005 Solar Designer <solar-at-owl.openwall.com> 1.4.2.1-owl4
- Extra buffer non-overflow safety for handler.c: mutt_decode_xbit().
- Updated the SEE ALSO lists of all Mutt man pages according to Owl
specifics.
- Do package muttbug(1) (redirect to flea.1) and mbox(5) man pages.
- Use the configure macro instead of the ./prepare script, do not pass
obsolete settings into configure and makeinstall.

* Tue Jun 28 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.4.2.1-owl3
- Build this package without optimizations based on strict aliasing rules.

* Sat Jun 25 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.4.2.1-owl2
- Rebuilt with libssl.so.5.

* Fri Feb 13 2004 Michail Litvak <mci-at-owl.openwall.com> 1.4.2.1-owl1
- 1.4.2.1 (remove -cvs patch included into release)

* Fri Jan 30 2004 Michail Litvak <mci-at-owl.openwall.com> 1.4.1-owl3
- Patch (from Mutt's CVS) to fix Mutt crash on certain e-mails; this can
occur when an UTF-8 locale is used on wide (more than ~120 columns)
terminals, but Owl isn't affected with its current glibc because of the
lack of UTF-8 locales support.

* Mon Oct 20 2003 Solar Designer <solar-at-owl.openwall.com> 1.4.1-owl2
- Build without glibc's wide character functions due to the broken locales;
in particular, with koi8-r some control characters wouldn't be treated
as such after being passed through mbrtowc() and checked with iswcntrl().

* Sun Mar 23 2003 Jarno Huuskonen <jhuuskon-at-owl.openwall.com> 1.4.1-owl1
- 1.4.1

* Mon Jan 20 2003 Solar Designer <solar-at-owl.openwall.com>
- Improved the package description.
- Require the proper version of mktemp for our muttbug/flea patch.
- Initial commit into Owl.

* Wed Jan 15 2003 Jarno Huuskonen <jhuuskon-at-owl.openwall.com>
- use mkstemp when creating temporary files.
- include locales and flea

* Wed Sep 25 2002 Solar Designer <solar-at-owl.openwall.com>
- Updated to 1.4, the package is still non-public.
- Don't use slang.

* Tue Jan 08 2002 Solar Designer <solar-at-owl.openwall.com>
- Based this spec file on Red Hat's, dropped most patches for now.
