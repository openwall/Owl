# $Id: Owl/packages/gettext/gettext.spec,v 1.5 2003/10/29 19:22:05 solar Exp $

Summary: GNU libraries and utilities for producing multi-lingual messages.
Name: gettext
Version: 0.10.35
Release: owl24
License: GPL
Group: Development/Tools
Source: ftp://alpha.gnu.org/pub/gnu/%name-%version.tar.gz
Patch0: gettext-0.10.35-owl-sanitize-environ.diff
Patch1: gettext-0.10.35-rh-getline.diff
Patch2: gettext-0.10.35-rh-hacks.diff
Patch3: gettext-0.10.35-rh-aclocaldir.diff
Patch4: gettext-0.10.35-rh-buildroot.diff
Patch5: gettext-0.10.35-rh-destdir.diff
Patch6: gettext-0.10.35-rh-verttab.diff
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
%patch5 -p0
%patch6 -p1

%build
unset LINGUAS || :
libtoolize --copy --force
aclocal
automake
autoconf
%configure --enable-shared --with-included-gettext
make

%install
rm -rf $RPM_BUILD_ROOT

# Fix busted no-emacs install for $lispdir/po-mode.el
%makeinstall lispdir=%buildroot/usr/share/emacs/site-lisp \
	aclocaldir=%buildroot/usr/share/aclocal

%post
/sbin/install-info %_infodir/gettext.info.gz %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/gettext.info.gz %_infodir/dir
fi

%files
%defattr(-,root,root)
%_bindir/*
%_infodir/*.info*
%_datadir/gettext
%_datadir/locale/*/LC_MESSAGES/*
%_datadir/aclocal/*
%_datadir/emacs/site-lisp/*

%changelog
* Sun Feb 03 2002 Michail Litvak <mci@owl.openwall.com> 0.10.35-owl24
- Enforce our new spec file conventions

* Thu Oct 19 2000 Solar Designer <solar@owl.openwall.com>
- Added a security patch for the (largely unused) libintl sources that
get installed into /usr/share/gettext/intl
- unset LINGUAS

* Sun Sep 24 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import spec from RH
- little sprintf/snprintf fix.
