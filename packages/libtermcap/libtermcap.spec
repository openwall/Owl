# $Id: Owl/packages/libtermcap/libtermcap.spec,v 1.2 2000/09/08 18:26:22 solar Exp $

Summary: A basic system library for accessing the termcap database.
Name: libtermcap
Version: 2.0.8
Release: 2owl
Copyright: LGPL
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
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Requires: /etc/termcap
BuildPreReq: texinfo

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

If you need to develop programs which will access the termcap database,
you'll need to install this package.  You'll also need to install the
libtermcap package.

# Use %optflags_lib for this package if defined.
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

%build
make CFLAGS="$RPM_OPT_FLAGS -I."

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{usr/lib,usr/info,usr/include,etc,lib}

export PATH=/sbin:$PATH
make prefix=$RPM_BUILD_ROOT/usr install

install -m 644 termcap.info* $RPM_BUILD_ROOT/usr/info

cd $RPM_BUILD_ROOT
mv usr/lib/libtermcap.so* lib
ln -sf libtermcap.so.2.0.8 lib/libtermcap.so
ln -sf /lib/libtermcap.so.2.0.8 usr/lib/libtermcap.so
strip -R .comments --strip-unneeded lib/libtermcap.so.2.0.8
gzip -9nf usr/info/termcap.info*

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%trigger -- info >= 3.12
/sbin/install-info \
	--section="Libraries" --entry="* Termcap: (termcap).               The GNU termcap library." \
	--info-dir=/usr/info /usr/info/termcap.info.gz

%postun
if [ $1 = 0 ]; then
    /sbin/install-info --delete \
	--section="Libraries" --entry="* Termcap: (termcap).               The GNU termcap library." \
	--info-dir=/usr/info /usr/info/termcap.info.gz
fi
/sbin/ldconfig

%files
%defattr(-,root,root)
/usr/info/termcap.info*
/lib/libtermcap.so.2.0.8

%files devel
%defattr(-,root,root)
/usr/lib/libtermcap.a
/usr/lib/libtermcap.so
/usr/include/termcap.h

%changelog
* Fri Sep 08 2000 Solar Designer <solar@owl.openwall.com>
- %optflags_lib support.

* Wed Aug 02 2000 Solar Designer <solar@owl.openwall.com>
- Imported this spec file from RH, and changed it heavily.
