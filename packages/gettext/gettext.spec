# $Owl: Owl/packages/gettext/gettext.spec,v 1.13 2006/04/06 22:35:42 ldv Exp $

Summary: GNU libraries and utilities for producing multi-lingual messages.
Name: gettext
Version: 0.14.5
Release: owl1
License: GPL/LGPL
Group: Development/Tools
URL: http://www.gnu.org/software/gettext/
Source: ftp://ftp.gnu.org/gnu/gettext/%name-%version.tar.gz
Patch0: gettext-0.14.5-alt-gettextize-quiet.diff
Patch1: gettext-0.14.5-alt-m4.diff
Patch2: gettext-0.14.5-alt-tmp.diff
Patch3: gettext-0.14.5-alt-warnings.diff
Patch4: gettext-0.14.5-alt-doc.diff
PreReq: /sbin/install-info
Provides: %name-devel = %version-%release
Provides: devel(libintl)
BuildRequires: automake, autoconf, libtool, bison, gcc-c++
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
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%configure --enable-shared --without-included-gettext

%install
rm -rf %buildroot

# Fix busted no-emacs install for $lispdir/po-mode.el
%makeinstall lispdir=%buildroot%_datadir/emacs/site-lisp \
	aclocaldir=%buildroot%_datadir/aclocal \
	gettextsrcdir=%buildroot%_datadir/%name/intl

mv %buildroot%_datadir/%name/intl/{ABOUT-NLS,archive.tar.gz} \
	%buildroot%_datadir/%name/

mkdir -p %buildroot%_datadir/%name/po
install -pm644 %name-runtime/po/Makefile.in.in %buildroot%_datadir/%name/po/

# Move documentation in the right place
%define docdir %_docdir/%name-%version
mkdir -p %buildroot%_docdir
mv %buildroot%_datadir/doc/%name %buildroot%docdir
mv %buildroot%_datadir/doc/libasprintf %buildroot%docdir/

# Remove unpackaged files
rm %buildroot%_infodir/dir %buildroot%_libdir/*.la

%post
/sbin/install-info %_infodir/gettext.info %_infodir/dir
/sbin/install-info %_infodir/autosprintf.info %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/gettext.info %_infodir/dir
	/sbin/install-info --delete %_infodir/autosprintf.info %_infodir/dir
fi

%files
%defattr(-,root,root)
%docdir
%_bindir/*
%_infodir/*.info*
%_includedir/*.h
%_mandir/man?/*
%_libdir/*
%_datadir/gettext
%_datadir/aclocal/*
%_datadir/locale/*/LC_MESSAGES/*

%changelog
* Thu Apr 06 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.14.5-owl1
- Updated to 0.14.5.
- Imported a bunch of patches from ALT's gettext-0.14.5-alt2 package.
- Build gettext with libintl provided by glibc.

* Fri Sep 24 2005 Michail Litvak <mci-at-owl.openwall.com>  0.14.1-owl3
- Don't package .la files.

* Thu May 05 2005 Solar Designer <solar-at-owl.openwall.com> 0.14.1-owl2
- "Provide" gettext-devel and devel(libintl) for Fedora compatibility.
- Install autosprintf.info.
- Corrected the Source URL, License.
- Added URL.

* Wed Sep 08 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 0.14.1-owl1
- Changed %%exclude to removing the file in %%install section; this will
allow to build this package under RPM3.

* Wed Mar 17 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 0.14.1-owl0.1
- Updated to 0.14.1
- Cleaned up the spec (removed unneeded patches, fixed a typo)

* Thu Feb 26 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 0.11.5-owl0.1
- Updated to 0.11.5
- Temporarily we do not package libintl.h as it conflicts with one from glibc
- Some autotools magic to build this package under new autoconf
- Temporarily disabled packaging of emacs lisp files, must be investigated

* Sun Feb 03 2002 Michail Litvak <mci-at-owl.openwall.com> 0.10.35-owl24
- Enforce our new spec file conventions

* Thu Oct 19 2000 Solar Designer <solar-at-owl.openwall.com>
- Added a security patch for the (largely unused) libintl sources that
get installed into /usr/share/gettext/intl
- unset LINGUAS

* Sun Sep 24 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import spec from RH
- little sprintf/snprintf fix.
