# $Id: Owl/packages/gettext/gettext.spec,v 1.2 2000/10/18 23:46:50 solar Exp $

Summary: GNU libraries and utilities for producing multi-lingual messages.
Name: 	 gettext
Version: 0.10.35
Release: 24owl
License: GPL
Group: 	 Development/Tools
Source:  ftp://alpha.gnu.org/pub/gnu/%{name}-%{version}.tar.gz
Patch0:  gettext-0.10.35-owl-sanitize-environ.diff
Patch1:  gettext-0.10.35-rh-getline.diff
Patch2:  gettext-0.10.35-rh-hacks.diff
Patch3:  gettext-0.10.35-rh-aclocaldir.diff
Patch4:  gettext-0.10.35-rh-buildroot.diff
Patch5:  gettext-0.10.35-rh-destdir.diff
Patch6:  gettext-0.10.35-rh-verttab.diff
Buildroot: /var/rpm-buildroot/%{name}-root

%description
The GNU gettext package provides a set of tools and documentation for
producing multi-lingual messages in programs.  Tools include a set of
conventions about how programs should be written to support message
catalogs, a directory and file naming organization for the message
catalogs, a runtime library which supports the retrieval of translated
messages, and stand-alone programs for handling the translatable and
the already translated strings.  Gettext provides an easy to use
library and tools for creating, using, and modifying natural language
catalogs and is a powerful and simple method for internationalizing
programs.

If you would like to internationalize or incorporate multi-lingual
messages into programs that you're developing, you should install
gettext.

%prep
rm -rf %{buildroot}
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1 -b .buildroot
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
rm -rf %{buildroot}

# Fix busted no-emacs install for $lispdir/po-mode.el
%makeinstall lispdir=%{buildroot}/usr/share/emacs/site-lisp \
    aclocaldir=%{buildroot}/usr/share/aclocal

pushd %{buildroot}
rm -f .%{_infodir}/dir .%{_includedir}/libintl.h
gzip -9nf .%{_infodir}/*
strip .%{_bindir}/* || :
popd

%clean
rm -rf %{buildroot}

%post
/sbin/install-info %{_infodir}/gettext.info.gz %{_infodir}/dir

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/gettext.info.gz %{_infodir}/dir
fi
exit 0

%files
%defattr(-,root,root)
%{_bindir}/*
%{_infodir}/*
%{_datadir}/gettext
%{_datadir}/locale/*/LC_MESSAGES/*
%{_datadir}/aclocal/*
%{_datadir}/emacs/site-lisp/*

%changelog
* Thu Oct 19 2000 Solar Designer <solar@owl.openwall.com>
- Added a security patch for the (largely unused) libintl sources that
get installed into /usr/share/gettext/intl
- unset LINGUAS

* Sun Sep 24 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import spec from RH 
- little sprintf/snprintf fix.

* Wed Aug 23 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Added patch from Ulrich Drepper

* Fri Aug 04 2000 Trond Eivind Glomsrød <teg@redhat.com>
- update DESTDIR patch (#12072)

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul 10 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fix problems wrt to DESTDIR (#12072)

* Thu Jun 22 2000 Preston Brown <pbrown@redhat.com>
- use FHS paths
- add buildroot patch for .../intl/Makefile.in, was using abs. install path

* Fri Apr 28 2000 Bill Nottingham <notting@redhat.com>
- minor configure tweaks for ia64

* Sun Feb 27 2000 Cristian Gafton <gafton@redhat.com>
- add --comments to msghack

* Thu Feb 10 2000 Cristian Gafton <gafton@redhat.com>
- fix bug #9240 - gettextize has the right aclocal patch

* Wed Jan 12 2000 Cristian Gafton <gafton@redhat.com>
- add the --diff and --dummy options

* Wed Oct 06 1999 Cristian Gafton <gafton@redhat.com>
- add the --missing option to msghack

* Wed Sep 22 1999 Cristian Gafton <gafton@redhat.com>
- updated msghack not to merge in fuzzies in the master catalogs

* Thu Aug 26 1999 Cristian Gafton <gafton@redhat.com>
- updated msghack to understand --append

* Wed Aug 11 1999 Cristian Gafton <gafton@redhat.com>
- updated msghack to correctly deal with sorting files

* Thu May 06 1999 Cristian Gafton <gafton@redhat.com>
- msghack updates

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 8)

* Mon Mar 08 1999 Cristian Gafton <gafton@redhat.com>
- added patch for misc hacks to facilitate rpm translations

* Thu Dec 03 1998 Cristian Gafton <gafton@redhat.com>
- patch to allow to build on ARM

* Wed Sep 30 1998 Jeff Johnson <jbj@redhat.com>
- add Emacs po-mode.el files.

* Sun Sep 13 1998 Cristian Gafton <gafton@redhat.com>
- include the aclocal support files

* Fri Sep  3 1998 Bill Nottingham <notting@redhat.com>
- remove devel package (functionality is in glibc)

* Tue Sep  1 1998 Jeff Johnson <jbj@redhat.com>
- update to 0.10.35.

* Mon Jun 29 1998 Jeff Johnson <jbj@redhat.com>
- add gettextize.
- create devel package for libintl.a and libgettext.h.

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sun Nov 02 1997 Cristian Gafton <gafton@redhat.com>
- added info handling
- added misc-patch (skip emacs-lisp modofications)

* Sat Nov 01 1997 Erik Troan <ewt@redhat.com>
- removed locale.aliases as we get it from glibc now
- uses a buildroot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- Built against glibc
