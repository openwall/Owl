# $Id: Owl/packages/gettext/gettext.spec,v 1.6 2004/09/10 07:23:21 galaxy Exp $

Summary: GNU libraries and utilities for producing multi-lingual messages.
Name: gettext
Version: 0.14.1
Release: owl0.2
License: GPL
Group: Development/Tools
Source: ftp://alpha.gnu.org/pub/gnu/%name-%version.tar.gz
Patch0: gettext-0.14.1-alt-gettextize-quiet.diff
BuildRoot: /override/%name-%version

%description
The GNU gettext package provides a set of tools and documentation for
producing multi-lingual messages in programs.  Tools include a set of
conventions about how programs should be written to support message
catalogs, a directory and file naming organization for the message
catalogs, a runtime library which supports the retrieval of translated
messages, and stand-alone programs for handling the translatable and
the already translated strings.  gettext provides an easy to use
library and tools for creating, using, and modifying natural language
catalogs and is a powerful and simple method for internationalizing
programs.

%prep
%setup -q
%patch0 -p1

%build

unset LINGUAS || :
libtoolize --force --copy
aclocal
automake
autoconf
LDFLAGS="-L%buildsubdir/gettext-runtime/intl/.libs -L%buildsubdir/gettext-tools/lib/.libs -L%buildsubdir/gettext-tools/src/.libs $LDFLAGS" \
%configure --enable-shared --with-included-gettext --enable-relocatable
%__make aliaspath='%_libdir/X11/locale:%_datadir/locale'

%install
rm -rf %buildroot

# Fix busted no-emacs install for $lispdir/po-mode.el
%makeinstall lispdir=%buildroot%_datadir/emacs/site-lisp \
	aclocaldir=%buildroot%_datadir/aclocal \
	gettextsrcdir=%buildroot%_datadir/%name/intl

mv %buildroot%_datadir/%name/intl/{ABOUT-NLS,archive.tar.gz} \
	%buildroot%_datadir/%name/

mkdir -p %buildroot%_datadir/%name/po
install -p -m 644 %name-runtime/po/Makefile.in.in %buildroot%_datadir/%name/po/

# Move documentation in the right place
mkdir -p %buildroot%_docdir
mv %buildroot%_datadir/doc/%name %buildroot%_docdir/%name-%version
mv %buildroot%_datadir/doc/libasprintf %buildroot%_docdir/%name-%version/

# Remove unpackaged files
rm %buildroot%_infodir/dir
rm %buildroot%_datadir/locale/locale.alias
rm %buildroot%_includedir/libintl.h

%post
/sbin/install-info --info-dir=%_infodir %_infodir/gettext.info.gz

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete --info-dir=%_infodir %_infodir/gettext.info.gz
fi

%files
%defattr(-,root,root)
%doc %_docdir/%name-%version
%_bindir/*
%_infodir/*.info*
%_includedir/*.h
%_mandir/man?/*
%_libdir/*
%_datadir/gettext
%_datadir/locale/*/LC_MESSAGES/*
%_datadir/aclocal/*
#XXX: make install skips these -- (GM)
#%_datadir/emacs/site-lisp/*

%changelog
* Wed Sep 08 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 0.14-owl0.2
- Changed %%exclude to removing the file in %%install section. This will
allow build this package under RPM3

* Wed Mar 17 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 0.14-owl0.1
- Updated to 0.14
- Cleaned up the spec (removed unneeded patches, fixed a typo)

* Thu Feb 26 2004 (GalaxyMaster) <galaxy@owl.openwall.com> 0.11.5-owl0.1
- Updated to 0.11.5
- Temporarily we do not package libintl.h as it conflicts with one from glibc
- Some autotools magic to build this package under new autoconf
- Temporarily disabled packaging of emacs lisp files, must be investigated

* Sun Feb 03 2002 Michail Litvak <mci@owl.openwall.com> 0.10.35-owl24
- Enforce our new spec file conventions

* Thu Oct 19 2000 Solar Designer <solar@owl.openwall.com>
- Added a security patch for the (largely unused) libintl sources that
get installed into /usr/share/gettext/intl
- unset LINGUAS

* Sun Sep 24 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import spec from RH
- little sprintf/snprintf fix.
