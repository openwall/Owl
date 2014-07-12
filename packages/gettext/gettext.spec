# $Owl: Owl/packages/gettext/gettext.spec,v 1.17 2014/07/12 13:51:40 galaxy Exp $

Summary: GNU libraries and utilities for producing multi-lingual messages.
Name: gettext
Version: 0.19.1
Release: owl1
License: GPLv3+/LGPLv2+
Group: Development/Tools
URL: http://www.gnu.org/software/gettext/
Source: ftp://ftp.gnu.org/gnu/%name/%name-%version.tar.xz
Patch0: %name-0.19.1-owl-tests-xterm.diff
Patch1: %name-0.19.1-alt-gettextize-quiet.diff
Patch2: %name-0.19.1-owl-alt-tmp.diff
Patch3: %name-0.19.1-alt-doc.diff
Requires(post,preun): /sbin/install-info
Provides: %name-devel = %version-%release
Provides: devel(libintl)
BuildRequires: automake, autoconf >= 2.62, libtool, bison, gcc-c++
# the following are provided by Owl and should be used:
# ncurses in Owl are old, so wait till it's updated
#BuildRequires: ncurses-devel >= 5.9
# the following are NOT provided by Owl, so gettext uses its own copy
# I think we need to package them since relying on supplied versions
# is risky.
#BuildRequires: expat-devel
#BuildRequires: libxml2-devel
#BuildRequires: glib2-devel
#BuildRequires: libcroco-devel
#BuildRequires: libunistring-devel
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

%{expand:%%define optflags %optflags -Wall}

%build
%configure \
	--disable-rpath \
	--enable-shared \
	--disable-static \
	--enable-nls \
	--enable-c++ \
	--enable-libasprintf \
	--disable-java \
		--disable-native-java \
	--disable-git \
	--disable-csharp \
	--disable-openmp \
	--disable-acl \
	--without-included-gettext \
	--without-emacs \
	'--with-listdir=%_datadir/emacs/site-lisp' \
	--without-included-glib \
	--with-included-libcroco \
	--with-included-libxml \
#

%__make

%check
%{expand:%%{!?_with_test: %%{!?_without_test: %%global _without_test --without-test}}}
%__make check

%install
[ '%buildroot' != '/' -a -d '%buildroot' ] && rm -rf -- '%buildroot'

%makeinstall

mkdir -p %buildroot%_datadir/%name/po
install -pm644 %name-runtime/po/Makefile.in.in %buildroot%_datadir/%name/po/

# Move documentation in the right place
%define docdir %_docdir/%name-%version
mkdir -p %buildroot%_docdir
mv %buildroot%_datadir/doc/%name %buildroot%docdir
mv %buildroot%_datadir/doc/libasprintf %buildroot%docdir/

%find_lang %name-runtime || :
touch '%name-runtime.lang'
%find_lang %name-tools || :
touch '%name-tools.lang'
cat %name-{runtime,tools}.lang > '%name.lang'
rm -- %name-{runtime,tools}.lang

# Remove unpackaged files
rm %buildroot%_infodir/dir %buildroot%_libdir/*.la

%post
/sbin/ldconfig
/sbin/install-info %_infodir/gettext.info %_infodir/dir
/sbin/install-info %_infodir/autosprintf.info %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/gettext.info %_infodir/dir
	/sbin/install-info --delete %_infodir/autosprintf.info %_infodir/dir
fi

%postun -p /sbin/ldconfig

%files -f %name.lang
%defattr(-,root,root)
%docdir
%_bindir/*
%_infodir/*.info*
%_includedir/*.h
%_mandir/man?/*
%_libdir/*
%_datadir/gettext
%_datadir/aclocal/*

%changelog
* Sat Jun 14 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 0.19.1-owl1
- Updated to 0.19.1.
- Replaced the deprecated PreReq tag with Requires(post,preun).
- Added %%find_lang.

* Wed Dec 05 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.14.6-owl1
- Updated to 0.14.6.

* Thu Apr 06 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 0.14.5-owl1
- Updated to 0.14.5.
- Imported a bunch of patches from ALT's gettext-0.14.5-alt2 package.
- Build gettext with libintl provided by glibc.

* Sat Sep 24 2005 Michail Litvak <mci-at-owl.openwall.com>  0.14.1-owl3
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
