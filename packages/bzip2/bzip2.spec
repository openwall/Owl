# $Id: Owl/packages/bzip2/bzip2.spec,v 1.4 2000/11/29 15:15:42 kad Exp $

%define 	bz2libver	1.0.0

Summary: 	A file compression utility.
Name: 		bzip2
Version: 	1.0.1
Release: 	4owl
Copyright: 	BSD
Group:		Applications/File
URL: 		http://sources.redhat.com/bzip2/
Source0: 	ftp://sources.redhat.com/pub/bzip2/v100/bzip2-%{version}.tar.gz
Source1: 	bzgrep
Patch: 		bzip2-1.0.1-autoconflibtoolize.patch.gz
BuildRoot: 	/var/rpm-buildroot/%{name}-root

%description
Bzip2 is a freely available, patent-free, high quality data compressor.
Bzip2 compresses files to within 10 to 15 percent of the capabilities 
of the best techniques available.  However, bzip2 has the added benefit 
of being approximately two times faster at compression and six times 
faster at decompression than those techniques.  Bzip2 is not the 
fastest compression utility, but it does strike a balance between speed 
and compression capability.

Install bzip2 if you need a compression utility.

%package devel
Summary: Header files and libraries for developing apps which will use bzip2.
Group: Development/Libraries
Requires: bzip2 = %{version}

%description devel

Header files and a static library of bzip2 functions, for developing apps
which will use the library.

%prep
%setup -q 

%patch -p1
cp m4/largefile.m4 .
chmod a+x configure
touch ChangeLog

%build

%configure --enable-shared --enable-static 

# XXX avoid rerunning automake et al.
touch aclocal.m4

touch configure
chmod +x install-sh

make

%install
rm -rf ${RPM_BUILD_ROOT}

%makeinstall

cp %SOURCE1 ${RPM_BUILD_ROOT}%{_bindir}
chmod 0755 ${RPM_BUILD_ROOT}%{_bindir}/bzgrep

# Hack!
ln -s libbz2.so.%{bz2libver} ${RPM_BUILD_ROOT}%{_libdir}/libbz2.so.0

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING README README.COMPILATION.PROBLEMS Y2K_INFO NEWS ChangeLog
%{_bindir}/*
%{_mandir}/*/*
%{_libdir}/*so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*so

%changelog
* Wed Nov 29 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- bzip2 ver 0.x compat hack

* Sun Oct  1 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import spec from RH
- patch goes to repacked

* Fri Jul 21 2000 Trond Eivind Glomsrød <teg@redhat.com>
- new URL and source location

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jul 01 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 1.0.1
- ported my patch

* Tue Jun 13 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging to build on solaris2.5.1.
- remove config.cache from autoconf patch.
- sparc: use %%configure, but not the m4 macros.

* Tue Jun 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Use %%configure, %%makeinstall, %%{_manpath} and %%{_tmpdir}

* Wed May 17 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 1.0.0 - ported my 1.0pre8 libtoolizedautoconf patch

* Tue May 16 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use soft links, not hardlinks, for binaries
- mv .so to devel

* Mon May 15 2000 Trond Eivind Glomsrød <teg@redhat.com>
- autoconfed and libtoolized package 
- fixed Copyright (it's BSD, not GPL)
- dumped bzless (less works fine with bz2-files)
- rewrote build and install parts
- separated main package and devel package

* Mon May  8 2000 Bernhard Rosenkränzer <bero@redhat.com>
- 1.0pre8

* Fri Apr 14 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Add bzgrep (a version of zgrep hacked to do bzip2)

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Fri Dec 31 1999 Bernhard Rosenkränzer <bero@redhat.com>
- 0.9.5d
- Update download URL, add URL: tag in header

* Tue Aug 10 1999 Jeff Johnson <jbj@redhat.com>
- upgrade to 0.9.5c.

* Mon Aug  9 1999 Bill Nottingham <notting@redhat.com>
- install actual bzip2 binary, not libtool cruft.

* Sun Aug  8 1999 Jeff Johnson <jbj@redhat.com>
- run ldconfig to get shared library.

* Mon Aug  2 1999 Jeff Johnson <jbj@redhat.com>
- create shared libbz1.so.* library.

* Sun Apr  4 1999 Jeff Johnson <jbj@redhat.com>
- update to bzip2-0.9.0c.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Wed Sep 30 1998 Cristian Gafton <gafton@redhat.com>
- force compilation with egcs to avoid gcc optimization bug (thank God 
  we haven't been beaten by it)

* Wed Sep 09 1998 Cristian Gafton <gafton@redhat.com>
- version 0.9.0b

* Tue Sep 08 1998 Cristian Gafton <gafton@redhat.com>
- updated to 0.9.0

* Thu Apr 09 1998 Cristian Gafton <gafton@redhat.com>
- first build for Manhattan
