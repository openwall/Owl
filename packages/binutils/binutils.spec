# $Id: Owl/packages/binutils/binutils.spec,v 1.4 2001/01/17 23:52:24 solar Exp $

%define BUILD_HJL	'yes'

Summary: A GNU collection of binary utilities.
Name: binutils
Version: 2.10.1.0.4
Release: 1owl
Copyright: GPL
Group: Development/Tools
URL: http://sources.redhat.com/binutils/
%if "%{BUILD_HJL}"=="'yes'"
Source: ftp://ftp.valinux.com/pub/support/hjl/binutils/binutils-%{version}.tar.gz
%else
Source: ftp://ftp.gnu.org/pub/gnu/binutils/binutils-%{version}.tar.gz
%endif
Buildroot: /var/rpm-buildroot/%{name}-%{version}
ExcludeArch: ia64

%description
Binutils is a collection of binary utilities, including ar (for creating,
modifying and extracting from archives), nm (for listing symbols from
object files), objcopy (for copying and translating object files),
objdump (for displaying information from object files), ranlib (for
generating an index for the contents of an archive), size (for listing
the section sizes of an object or archive file), strings (for listing
printable strings from files), strip (for discarding symbols), c++filt
(a filter for demangling encoded C++ symbols), addr2line (for converting
addresses to file and line).

Install binutils if you need to perform any of these types of actions on
binary files.  Most programmers will want to install binutils.

%prep
%setup -q

%build
ADDITIONAL_TARGETS=""
%ifos linux
%ifarch sparc sparcv9
ADDITIONAL_TARGETS="--enable-targets=sparc64-linux"
%endif
%ifarch sparcv9
%define _target_platform sparc-%{_vendor}-%{_target_os}
%endif
%endif
%if "%{BUILD_HJL}"=="'yes'"
%define __libtoolize echo --
%endif
%configure --enable-shared $ADDITIONAL_TARGETS
make tooldir=%{_prefix}usr all info

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}
%makeinstall
make prefix=${RPM_BUILD_ROOT}%{_prefix} infodir=${RPM_BUILD_ROOT}%{_infodir} \
	install-info
strip ${RPM_BUILD_ROOT}%{_prefix}/bin/*
gzip -9nf ${RPM_BUILD_ROOT}%{_infodir}/*.info*
rm ${RPM_BUILD_ROOT}%{_mandir}/man1/nlmconv.1

install -m 644 include/libiberty.h ${RPM_BUILD_ROOT}%{_prefix}/include

chmod +x ${RPM_BUILD_ROOT}%{_prefix}/%{_lib}/lib*.so*

# This one comes from egcs
rm -f ${RPM_BUILD_ROOT}%{_prefix}/bin/c++filt

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/ldconfig
/sbin/install-info --info-dir=%{_infodir} %{_infodir}/as.info.gz
/sbin/install-info --info-dir=%{_infodir} %{_infodir}/bfd.info.gz
/sbin/install-info --info-dir=%{_infodir} %{_infodir}/binutils.info.gz
/sbin/install-info --info-dir=%{_infodir} %{_infodir}/gasp.info.gz
/sbin/install-info --info-dir=%{_infodir} %{_infodir}/gprof.info.gz
/sbin/install-info --info-dir=%{_infodir} %{_infodir}/ld.info.gz
/sbin/install-info --info-dir=%{_infodir} %{_infodir}/standards.info.gz

%preun
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/as.info.gz
  /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/bfd.info.gz
  /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/binutils.info.gz
  /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/gasp.info.gz
  /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/gprof.info.gz
  /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/ld.info.gz
  /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/standards.info.gz
fi

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README
%{_prefix}/bin/*
%{_mandir}/man1/*
%{_prefix}/include/*
%{_prefix}/%{_lib}/*
%{_infodir}/*info*

%changelog
* Thu Jan 18 2001 Solar Designer <solar@owl.openwall.com>
- 2.10.1.0.4 (due to the temporary file handling fix in objdump that is
not in the 2.10.1 release).

* Fri Nov 17 2000 Solar Designer <solar@owl.openwall.com>
- --enable-targets=sparc64-linux for sparcv9 as well as plain sparc.
- Pass plain sparc- target to configure when building for sparcv9, to
allow for the use of sparcv9 optflags while not confusing configure.

* Sat Jul 29 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- 2.10

* Tue Jul 18 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- 2.9.5.0.46
- import from spec from RH
