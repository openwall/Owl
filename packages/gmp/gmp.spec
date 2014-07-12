# $Owl: Owl/packages/gmp/gmp.spec,v 1.8 2014/07/12 13:52:04 galaxy Exp $

%define ver 6.0.0

Summary: The GNU multiple precision arithmetic library.
Name: gmp
Version: %{ver}a
Release: owl1
Epoch: 1
License: LGPLv3/GPLv2
Group: System Environment/Libraries
URL: http://gmplib.org
Source0: https://gmplib.org/download/%name/%name-%version.tar.xz
Source1: gmp.h
Source2: gmp-mparam.h
BuildRequires: autoconf >= 2.69, automake, libtool
BuildRoot: /override/%name-%version

%description
GMP is a free library for arbitrary precision arithmetic, operating on signed
integers, rational numbers, and floating point numbers.  There is no practical
limit to the precision except the ones implied by the available memory in the
machine GMP runs on.  GMP has a rich set of functions, and the functions have a
regular interface.

The main target applications for GMP are cryptography applications and
research, Internet security applications, algebra systems, computational
algebra research, etc.

GMP is carefully designed to be as fast as possible, both for small operands
and for huge operands.  The speed is achieved by using full machine words as
the basic arithmetic type, by using fast algorithms, with highly optimized
assembly code for the most common inner loops for a lot of CPUs, and by a
general emphasis on speed.

%package devel
Summary: Development files for the GMP library.
Group: Development/Libraries
Requires: %name = %epoch:%version-%release
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description devel
Header files, static libraries, and documentation for using the GNU multiple
precision arithmetic library in applications.

%prep
%setup -q -n %name-%ver

%build
# autoreconf produces lots of warnings about deprecated usage,
# but, as of 2.69, regenerates everything properly.
autoreconf -fis -I .

# GMP does not require an executable stack despite of its use of hand-written
# assembly sources.
%__as --help | grep -q execstack &&
	export CCAS="%__cc -c -Wa,--noexecstack"

# GMP's configure does not support --target, so here is a hack to still use
# RPM's %%configure macro (unfortunately, cannot break this long line :( )
%define gmp_configure %(printf '%s' '%{expand:%configure}'|sed 's#[[:space:]]--target=[^[:space:]]\\+##g')
%gmp_configure \
	--enable-shared \
	--disable-static \
	--enable-cxx \
	--enable-assembly \
	--enable-fft \
	--disable-old-fft-full \
	--disable-nails \
	--disable-profiling \
	--disable-fat \
	--disable-minithres \
	--disable-fake-cpuid \
	--with-readline \
#

# ensure that we are not hardcoding rpaths
perl -pi -e 's|hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=\"-L\\\$libdir\"|g;' libtool
export LD_LIBRARY_PATH=`pwd`/.libs
%__make

%install
[ '%buildroot' != '/' -a -d '%buildroot' ] && rm -rf -- '%buildroot'

export LD_LIBRARY_PATH=`pwd`/.libs
%makeinstall
%if 0
/sbin/ldconfig -n '%buildroot%_libdir'
ln -sf libgmpxx.so.4 '%buildroot%_libdir'/libgmpxx.so
ln -s libgmp.so.10 %buildroot%_libdir'/libgmp.so.3
%endif

# Rename gmp.h to gmp-<arch>.h and gmp-mparam.h to gmp-mparam-<arch>.h to
# avoid file conflicts on multilib systems, and install wrapper include files
# gmp.h and gmp-mparam.h.
basearch='%_arch'
# always use i386 for iX86
%ifarch %ix86
basearch=i386
%endif
# Rename files and install wrappers
mv -- '%buildroot/%_includedir/gmp.h' \
	'%buildroot/%_includedir'/gmp-${basearch}.h
%__install -p -m644 '%_sourcedir/gmp.h' '%buildroot/%_includedir/'
%__install -p -m644 gmp-mparam.h \
	'%buildroot/%_includedir'/gmp-mparam-${basearch}.h
install -p -m644 '%_sourcedir/gmp-mparam.h' '%buildroot/%_includedir/'

# remove unpackaged files
rm -- '%buildroot%_infodir'/dir
find '%buildroot' -name '*.la' -ls -delete

%check
export LD_LIBRARY_PATH=`pwd`/.libs
%__make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
/sbin/install-info %_infodir/gmp.info.gz %_infodir/dir || :

%preun devel
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/gmp.info.gz %_infodir/dir || :
fi

%files
%defattr(0644,root,root,0755)
%doc COPYING COPYING.LESSERv3 NEWS README
%_libdir/libgmp.so.*
%_libdir/libgmpxx.so.*

%files devel
%defattr(0644,root,root,0755)
%_libdir/libgmp.so
%_libdir/libgmpxx.so
%_includedir/*.h
%_infodir/gmp.info*

%changelog
* Mon Jun 16 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 6.0.0a-owl1
- Updated to 6.0.0a.
- Tried to bring the spec file closer to Owl standards.

* Thu Jan 23 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 5.1.3-owl1
- Updated to 5.1.3.

* Wed Oct 26 2011 Solar Designer <solar-at-owl.openwall.com> 5.0.2-owl2
- Re-pointed the libgmp.so.3 symlink (introduced in 5.0.2-owl1) from libgmp.so
(part of the -devel subpackage) to libgmp.so.10 (part of the main package).

* Mon Oct 24 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 5.0.2-owl1
- Updated to 5.0.2.
- Multilib support for gmp-devel.

* Fri Oct 21 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 4.3.2-owl1
- Initial import from Fedora.
