# $Id: Owl/packages/bzip2/bzip2.spec,v 1.23 2005/05/20 23:22:43 ldv Exp $

Summary: An extremely powerful file compression utility.
Name: bzip2
Version: 1.0.3
Release: owl4
License: BSD
Group: Applications/File
URL: http://www.bzip.org
Source0: http://www.bzip.org/%version/%name-%version.tar.gz
Source1: bzip2.texi
Patch0: bzip2-1.0.3-alt-autotools.diff
Patch1: bzip2-1.0.3-owl-Makefile.diff
Patch2: bzip2-1.0.3-owl-tmp.diff
Patch3: bzip2-1.0.3-alt-progname.diff
Patch4: bzip2-1.0.3-alt-chmod-chown.diff
Patch5: bzip2-1.0.3-alt-owl-fopen.diff
Patch6: bzip2-1.0.3-alt-version.diff
PreReq: /sbin/ldconfig
Requires: mktemp >= 1:1.3.1
# Provide this soname for backwards compatibility
Provides: libbz2.so.0
BuildRoot: /override/%name-%version

%description
bzip2 is a freely available, patent-free, high quality data compressor.

bzip2 compresses files using the Burrows-Wheeler block sorting text
compression algorithm and Huffman coding.  Compression is generally
considerably better than that achieved by more conventional LZ77/LZ78-based
compressors (such as gzip), and approaches the performance of the PPM
family of statistical compressors.  bzip2 is by far not the fastest
compression utility, but it does strike a balance between speed and
compression capability.

%package devel
Summary: Header files and libraries for developing apps which will use bzip2.
Group: Development/Libraries
PreReq: /sbin/install-info
Requires: %name = %version-%release

%description devel
Header files and a static library of bzip2 functions, for developing apps
which will use the library.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
install -pm644 %_sourcedir/bzip2.texi .
chmod u+x samples.sh

%{expand:%%define optflags %optflags -Wall}

%build
autoreconf -fisv
%configure
make
make -k check

%install
rm -rf %buildroot

%makeinstall

# Provide this symlink for backwards compatibility
ln -s libbz2.so.%version %buildroot%_libdir/libbz2.so.0

# Remove unpackaged files
rm %buildroot{%_bindir,%_mandir/man1}/{bzcmp,bzdiff,bzgrep,bzfgrep,bzegrep,bzmore,bzless}*
rm %buildroot%_libdir/libbz2.la
rm -f %buildroot%_infodir/dir

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
/sbin/install-info %_infodir/bzip2.info %_infodir/dir

%preun devel
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/bzip2.info %_infodir/dir
fi

%files
%defattr(-,root,root)
%doc CHANGES LICENSE README Y2K_INFO
%_bindir/*
%_mandir/*/*
%_libdir/*.so.*

%files devel
%defattr(-,root,root)
%_includedir/*
%_libdir/*.a
%_libdir/*.so
%_infodir/bzip2.*

%changelog
* Fri May 20 2005 Dmitry V. Levin <ldv@owl.openwall.com> 1.0.3-owl4
- Relocated bzcmp, bzdiff, bz*grep, bzmore and bzless to gzip package
which provides better versions of these utilities now.

* Mon May 16 2005 Dmitry V. Levin <ldv@owl.openwall.com> 1.0.3-owl3
- Fixed double fclose bug in bunzip2 introduced in 1.0.3-owl1.

* Sat May 07 2005 Dmitry V. Levin <ldv@owl.openwall.com> 1.0.3-owl2
- Imported several patches from ALT: documentation in texinfo format,
autotools support, change of bzip2 -h/-L/-V options behaviour to
output to stdout instead of stderr and cause program exit (for -L/-V)
without processing any more options.
- Converted bunzip2, bzcat, bzcmp, bzegrep, bzfgrep, and bzless
utilities from hardlinks to symlinks.

* Fri May 06 2005 Solar Designer <solar@owl.openwall.com> 1.0.3-owl1
- Updated to 1.0.3.
- Re-worked the bzdiff temporary file handling patch according to our new
conventions and postponing the temporary file creation until it is certain
that the file is actually needed (idea from ALT).
- Imported several patches from ALT: the chmod/chown race condition fix
(use fchmod/fchown instead), use safe initial output file permissions in
bzip2recover, use program_invocation_short_name.

* Mon Feb 09 2004 Michail Litvak <mci@owl.openwall.com> 1.0.2-owl2
- Use RPM macros instead of explicit paths.

* Fri Feb 01 2002 Solar Designer <solar@owl.openwall.com> 1.0.2-owl1
- Updated to 1.0.2.
- Dropped Red Hat's autoconf/libtoolize patch.
- Use the new Makefile-libbz2_so for building the shared library.
- Package the bzip2 binary that is statically-linked against libbz2 for
better performance on register-starved architectures such as the x86.
- Patched bzdiff/bzcmp (new with 1.0.2) to use mktemp(1) instead of
"tempfile" and to remove the temporary file in all cases.
- Build with -Wall.

* Thu Jan 24 2002 Solar Designer <solar@owl.openwall.com>
- Patched a double-fclose() bug which could be triggered on certain
error conditions including running "bzip2 -f" on a directory (which
is the particular scenario reported to and dealt with by Red Hat).
- Enforce our new spec file conventions.
- Based the new package description on the man page.

* Wed Nov 29 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- bzip2 ver 0.x compat hack

* Sun Oct 01 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import spec from RH
- patch goes to repacked
