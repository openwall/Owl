# $Owl: Owl/packages/libnspr/libnspr.spec,v 1.2 2015/01/26 03:06:33 galaxy Exp $

Summary: Netscape Portable Runtime (NSPR) Library
Name: libnspr
Version: 4.10.7
Release: owl1
License: Mozilla
URL: https://developer.mozilla.org/en-US/docs/Mozilla/Projects/NSPR
Group: System/Libraries
BuildRoot: /override/%name-%version

Source: ftp://ftp.mozilla.org/pub/mozilla.org/nspr/releases/v%version/src/nspr-%version.tar.gz

%description
NSPR provides platform independence for non-GUI operating system 
facilities. These facilities include threads, thread synchronization, 
normal file and network I/O, interval timing and calendar time, basic 
memory management (malloc and free) and shared library linking.

%package devel
Summary: Development files for the %name package
Group: Development/Libraries/C and C++
Requires: %name = %version-%release

%description devel
This package provides header files to include, and libraries to link with, for
the Netscape Portable Runtime (NSPR).

%prep
%setup -q -n nspr-%version/nspr
%define _libdir /%_lib

%build
%configure \
	'--includedir=%_includedir/nspr' \
	--without-mozilla \
	--with-pthreads \
	--disable-ipv6 \
%ifarch x86_64 ia64 sparc64
	--enable-64bit \
%endif
# end of configure options

%__make

%install
[ '%buildroot' != '/' -a -d '%buildroot' ] && rm -rf -- '%buildroot'
%__make install DESTDIR='%buildroot'

# rm unpackaged files
rm '%buildroot%_bindir/compile-et.pl'
rm '%buildroot%_bindir/prerr.properties'
rm -r '%buildroot%_libdir/pkgconfig'

%check
# Run test suite.
perl pr/tests/runtests.pl 2>&1 | tee output.log

TEST_FAILURES=$(grep -c FAILED ./output.log) || :
if [ $TEST_FAILURES -ne 0 ]; then
  echo 'error: test suite returned failure(s)'
  exit 1
fi
echo 'test suite completed'

%clean
[ '%buildroot' != '/' -a -d '%buildroot' ] && rm -rf -- '%buildroot'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(0644,root,root,0755)
%_libdir/lib*.so

%files devel
%defattr(0644,root,root,0755)
%attr(0755,root,root) %_bindir/nspr-config
%_includedir/nspr
%_datadir/aclocal/nspr.m4
%_libdir/lib*.a

%changelog
* Fri Oct 10 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.10.7-owl1
- Updated to 4.10.7.

* Mon Jun 16 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.10.6-owl1
- Initial release for Owl.
- Relocated libplc4.so, libplds4.so, and libnspr4.so to /%%_lib since for
some reason Mozilla designed their NSS library in such a way that you
cannot produce a static copy of it, so any program using libnss will also
dynamically load NSPR's libraries.  Our newer RPM requires libnss and
we would like to have a rescue rpm binary in /bin, hence this compromise.

* Mon Jun 09 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.10.6-owlx0
- Updated to 4.10.6.

* Wed Feb 19 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.10.3-owlx0
- Created an initial package for Owl-extra.
