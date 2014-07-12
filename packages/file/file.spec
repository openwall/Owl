# $Owl: Owl/packages/file/file.spec,v 1.28 2014/07/12 13:50:34 galaxy Exp $

Summary: A utility for determining file types.
Name: file
Version: 5.19
Release: owl1
License: distributable
Group: Applications/File
URL: http://www.darwinsys.com/file/
Source0: ftp://ftp.astron.com/pub/file/file-%version.tar.gz
Source1: magic.local
Patch0: %name-5.19-rh-alt-compress.diff
Patch1: %name-5.19-deb-owl-fixes.diff
Patch2: %name-5.19-alt-magic.diff
Patch3: %name-5.19-owl-deb-magic.diff
Patch4: %name-5.19-deb-owl-man.diff
Patch5: %name-5.19-fc-magic-warning.diff
Prefix: %_prefix
Requires: libmagic = %version-%release
BuildRequires: zlib-devel, automake, autoconf >= 2.69
BuildRoot: /override/%name-%version

%description
The file command is used to identify a particular file according to the
type of data contained by the file.  file can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

%package -n libmagic
Summary: Shared library for handling magic files.
Group: System Environment/Libraries

%description -n libmagic
This package contains shared library for handling magic files.

%package -n libmagic-devel
Summary: Development files to build applications that handle magic files.
Group: Development/Libraries
Requires: libmagic = %version-%release

%description -n libmagic-devel
This package contains development files to build applications that handle
magic files.

%prep
%setup -q

# if a patch touches the magic database, apply it without -b, otherwise
# the compilation of the database may (and likely will) fail.

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

# Patches can generate *.orig files, which can't stay in the magic dir,
# otherwise there will be problems with compiling magic file!
find magic/Magdir -type f -name '*.orig' -ls -delete

autoreconf -fis -I m4

%{expand:%%define optflags %optflags -D_GNU_SOURCE -Wall}

%build
%configure \
	--disable-rpath \
	--enable-fsect-man5 \
#

%__make

%install
rm -rf -- '%buildroot'
mkdir -p '%buildroot%_bindir'
mkdir -p '%buildroot%_mandir'/man{1,5}
mkdir -p '%buildroot%_datadir'

%makeinstall
install -p -D -m 644 '%_sourcedir/magic.local' '%buildroot%_sysconfdir/magic'

cat magic/Magdir/* > '%buildroot%_datadir/misc/magic'
ln -s misc/magic '%buildroot%_datadir/magic'

# remove unpackaged files
find '%buildroot%_libdir' -type f -name '*.la' -ls -delete

%check
%__make check

%post -n libmagic -p /sbin/ldconfig
%postun -n libmagic -p /sbin/ldconfig

%files
%defattr(0644,root,root,0755)
%doc COPYING ChangeLog README TODO
%config(noreplace) /etc/magic
%attr(0755,root,root) %_bindir/file
%_datadir/misc/magic*
%_datadir/magic
%_mandir/man1/file.1*
%_mandir/man5/magic.5*

%files -n libmagic
%defattr(0644,root,root,0755)
%_libdir/libmagic.so.*

%files -n libmagic-devel
%defattr(0644,root,root,0755)
%_libdir/libmagic.so
%_includedir/magic.h
%_mandir/man3/libmagic.3*

%changelog
* Mon Jun 16 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 5.19-owl1
- Updated to 5.19.
- Regenerated patches, dropped ones which were accepted upstream.
- Introduced the %%check section.
- Made filelists more specific, not to rely on upstream decided permissions.

* Thu Sep 02 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 5.04-owl2
- Silenced incorrect 'from' field message, patch from Fedora:
https://bugzilla.redhat.com/show_bug.cgi?id=599695
- Fixed segfault, patch from Fedora, additionally silenced a compiler warning:
https://bugzilla.redhat.com/show_bug.cgi?id=533245
- Do not trim 'from' field of core files, Debian patch:
https://bugzilla.redhat.com/show_bug.cgi?id=566305
http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=422524

* Wed Sep 01 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 5.04-owl1
- Updated to 5.04.
- Updated patches.
- Dropped patches rh-selinux, rh-alt-elf, owl-bound (fixed in upstream).
- Dropped patch rh-order.
- Imported patch from debian (doc-manpages-typo).

* Tue May 22 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.16-owl4
- Fixed integer overflow check in file_printf function, reported by
Colin Percival.

* Sun Mar 25 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.16-owl3
- Fixed potential heap corruption in file_printf function (CVE-2007-1536).
- Removed no longer required addition of "-D_FILE_OFFSET_BITS=64
-D_LARGEFILE_SOURCE" flags to %%optflags.

* Thu Mar 30 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 4.16-owl2
- Dropped LDFLAGS=-s from the %%build section, let's allow brp-* scripts
to do their work.
- Added the %%_datadir/file directory to the filelist (it was orphaned).

* Sun Oct 23 2005 Michail Litvak <mci-at-owl.openwall.com> 4.16-owl1
- 4.16
- Updated patches.
- New subpackages libmagic, libmagic-devel.

* Thu Feb 26 2004 Michail Litvak <mci-at-owl.openwall.com> 3.41-owl3
- Fixed building with new auto* tools.

* Tue Apr 29 2003 Michail Litvak <mci-at-owl.openwall.com> 3.41-owl2
- Patch to remove annoying message: "Using regular magic file..."

* Fri Mar 07 2003 Michail Litvak <mci-at-owl.openwall.com>
- 3.41
- Patch updates

* Thu Jan 31 2002 Michail Litvak <mci-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Wed Nov 29 2000 Michail Litvak <mci-at-owl.openwall.com>
- Imported from RH and updated to 3.33
- added some patches from Debian and RH
