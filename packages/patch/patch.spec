# $Id: Owl/packages/patch/patch.spec,v 1.1 2000/11/17 13:01:15 mci Exp $

Summary: The GNU patch command, for modifying/upgrading files.
Name: patch
Version: 2.5.4
Release: 5owl
Copyright: GPL
Group: Development/Tools
Source: ftp://ftp.gnu.org/gnu/patch/patch-%{version}.tar.gz
Patch0: patch-2.5.4-mdk-sigsegv.diff
Patch1: patch-2.5.4-rh-stderr.diff
Prefix: %{_prefix}
Buildroot: /var/rpm-buildroot/%{name}-root

%description
The patch program applies diff files to originals.  The diff command
is used to compare an original to a changed file.  Diff lists the
changes made to the file.  A person who has the original file can then
use the patch command with the diff file to add the changes to their
original file (patching the file).

Patch should be installed because it is a common way of upgrading
applications.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
# (fg) Large file support can be disabled from ./configure - it is necessary at
# least on sparcs
%ifnarch sparc sparcv9 sparc64 alpha
%configure
%else
%configure --disable-largefile
%endif

make "CFLAGS=$RPM_OPT_FLAGS -D_GNU_SOURCE -W -Wall" LDFLAGS=-s

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc NEWS README AUTHORS ChangeLog
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Tue Nov 17 2000 Michail Litvak <mci@owl.openwall.com>
- import from RH and Mandrake 
- sigsegv patch from MDK, stderr from RH
 
* Tue Jul 25 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.5.4-7mdk
- Fix possible sigsev (deb).
- By default create empty backup files as readable !!!.

* Tue Jul 25 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.5.4-6mdk
- really move the strip (titiscks)
- BM

* Tue Jul 11 2000 Thierry Vignaud <tvignaud@mandrakesoft.com>  2.5.4-5mdk
- add alpha for largefile
- remove binaries stripping & {info,man}-pages compression because of
  spec-helper
- Stefan van der Eijk <s.vandereijk@chello.nl> :
	* makeinstall macro
	* macroszifications

* Sun Apr 02 2000 Adam Lebsack <adam@mandrakesoft.com> 2.5.4-4mdk
- Fixed powerpc by adding -D_GNU_SOURCE flag.

* Mon Jan 17 2000 Francis Galiegue <francis@mandrakesoft.com>

- No large file support for sparc - now done from ./configure

* Sun Nov  7 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- build release.

* Wed Sep 08 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- 2.5.4

* Fri Aug 06 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- 2.5.3

* Wed May 05 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Mon Mar 22 1999 Jeff Johnson <jbj@redhat.com>
- (ultra?) sparc was getting large file system support.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 7)

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Tue Sep  1 1998 Jeff Johnson <jbj@redhat.com>
- bump release to preserve newer than back-ported 4.2.

* Tue Jun 09 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr

* Tue Jun  9 1998 Jeff Johnson <jbj@redhat.com>
- Fix for problem #682 segfault.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Apr 07 1998 Cristian Gafton <gafton@redhat.com>
- added buildroot

* Wed Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- updated to 2.5

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
