# $Owl: Owl/packages/libtermcap/libtermcap.spec,v 1.16 2006/02/03 22:31:15 ldv Exp $

Summary: A basic system library for accessing the termcap database.
Name: libtermcap
Version: 2.0.8
Release: owl7
License: LGPL
Group: System Environment/Libraries
Source: ftp://sunsite.unc.edu/pub/Linux/GCC/termcap-2.0.8.tar.gz
Patch0: termcap-2.0.8-owl-TERMCAP.diff
Patch1: termcap-2.0.8-owl-bound.diff
Patch2: termcap-2.0.8-rh-Makefile.diff
Patch3: termcap-2.0.8-rh-colon.diff
Patch4: termcap-2.0.8-rh-fix-tc.diff
Patch5: termcap-2.0.8-rh-glibc-2.1.diff
Patch6: termcap-2.0.8-rh-ignore-p.diff
Patch7: termcap-2.0.8-rh-xref.diff
Patch8: termcap-2.0.8-rh-glibc-2.2.diff
PreReq: /sbin/ldconfig
Requires: /etc/termcap
BuildRequires: texinfo
BuildRoot: /override/%name-%version

%description
The libtermcap package contains a basic system library needed to
access the termcap database.  The termcap library supports easy access
to the termcap database, so that programs can output character-based
displays in a terminal-independent manner.

%package devel
Summary: Development tools for programs which will access the termcap database.
Group: Development/Libraries
Requires: libtermcap

%description devel
This package includes the libraries and header files necessary for
developing programs which will access the termcap database.

# Use optflags_lib for this package if defined.
%{expand:%%define optflags %{?optflags_lib:%optflags_lib}%{!?optflags_lib:%optflags}}

%prep
%setup -q -n termcap-2.0.8
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
%__make CFLAGS="%optflags -I."

%install
rm -rf %buildroot
mkdir -p %buildroot/{usr/lib,usr/include,etc,lib}
mkdir -p %buildroot%_infodir

export PATH=/sbin:$PATH
%makeinstall

install -m 644 termcap.info* %buildroot%_infodir/

cd %buildroot
mv usr/lib/libtermcap.so* lib/
ln -sf libtermcap.so.2.0.8 lib/libtermcap.so.2
ln -sf ../../lib/libtermcap.so.2.0.8 usr/lib/libtermcap.so
strip -R .comments --strip-unneeded lib/libtermcap.so.2.0.8

%post -p /sbin/ldconfig

%trigger -- info >= 3.12
/sbin/install-info %_infodir/termcap.info %_infodir/dir \
	--entry="* Termcap: (termcap).                           The GNU termcap library."

%postun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/termcap.info %_infodir/dir \
		--entry="* Termcap: (termcap).                           The GNU termcap library."
fi
/sbin/ldconfig

%files
%defattr(-,root,root)
%_infodir/termcap.info*
/lib/libtermcap.so.2*

%files devel
%defattr(-,root,root)
/usr/lib/libtermcap.a
/usr/lib/libtermcap.so
/usr/include/termcap.h

%changelog
* Fri Feb 03 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.0.8-owl7
- Corrected info files installation.

* Fri Feb 27 2004 (GalaxyMaster) <galaxy-at-owl.openwall.com> 2.0.8-owl6
- Patched to compile properly under glibc 2.3.2

* Sat Oct 25 2003 Solar Designer <solar-at-owl.openwall.com> 2.0.8-owl5
- Make the /usr/lib/libtermcap.so symlink relative.

* Mon Aug 19 2002 Michail Litvak <mci-at-owl.openwall.com> 2.0.8-owl4
- Deal with info dir entries such that the menu looks pretty.

* Tue Feb 05 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions

* Sat Oct 28 2000 Solar Designer <solar-at-owl.openwall.com>
- Create /lib/libtermcap.so.2 before ldconfig.

* Fri Sep 08 2000 Solar Designer <solar-at-owl.openwall.com>
- optflags_lib support.

* Wed Aug 02 2000 Solar Designer <solar-at-owl.openwall.com>
- Imported this spec file from RH, and changed it heavily.
