# $Owl: Owl/packages/cvs/cvs.spec,v 1.30 2005/11/16 12:19:21 solar Exp $

Summary: A version control system.
Name: cvs
Version: 1.11.21
Release: owl1
License: GPL
Group: Development/Tools
URL: http://www.nongnu.org/cvs/
Source: ftp://ftp.gnu.org/non-gnu/cvs/source/stable/%version/cvs-%version.tar.bz2
Patch0: cvs-1.11.20-alt-remove-unused.diff
Patch1: cvs-1.11.21-owl-fixes.diff
Patch2: cvs-1.11.20-owl-info.diff
Patch3: cvs-1.11.21-alt-errno.diff
Patch4: cvs-1.11.20-owl-vitmp.diff
Patch5: cvs-1.11.20-owl-no-world-writables.diff
Patch6: cvs-1.11.20-alt-mdk-owl-canonicalize.diff
Patch7: cvs-1.11.20-alt-cvsbug-ypcat.diff
Patch8: cvs-1.11.20-owl-alt-tmp.diff
Patch9: cvs-1.11.20-deb-alt-doc.diff
Patch10: cvs-1.11.20-bsd-deb-local_branch_num.diff
Patch11: cvs-1.11.20-deb-normalize_cvsroot.diff
Patch12: cvs-1.11.20-deb-expand_keywords-alphanumeric.diff
Patch13: cvs-1.11.20-deb-server-wrapper.diff
Patch14: cvs-1.11.20-deb-fast-edit.diff
Patch15: cvs-1.11.20-alt-password_entry_operation.diff
Patch16: cvs-1.11.21-deb-alt-homedir.diff
Patch17: cvs-1.11.20-deb-alt-newlines.diff
Patch18: cvs-1.11.20-alt-cvsrc.diff
Patch19: cvs-1.11.20-alt-tagloginfo.diff
Patch20: cvs-1.11.20-alt-xasprintf.diff
Patch21: cvs-1.11.20-alt-env.diff
Patch22: cvs-1.11.20-alt-server-log.diff
Patch23: cvs-1.11.20-deb-alt-LocalKeyword-KeywordExpand.diff
Patch24: cvs-1.11.20-alt-noreadlock.diff
Patch25: cvs-1.11.20-alt-ssh.diff
Patch26: cvs-1.11.20-alt-testsuit-log.diff
PreReq: /sbin/install-info
Prefix: %_prefix
BuildRequires: mktemp >= 1:1.3.1, sed >= 4.1.1, zlib-devel
BuildRoot: /override/%name-%version

%description
Concurrent Versions System (CVS) is a version control system which can
record the history of your files (usually, but not always, source
code).  CVS only stores the differences between versions, instead of
every version of every file you've ever created.  CVS also keeps a log
of when and why changes occurred, and who made them.

CVS is very helpful for managing releases and controlling the
concurrent editing of source files among multiple authors.  Instead of
providing version control for a collection of files in a single
directory, CVS provides version control for a hierarchical collection
of directories consisting of revision controlled files.  These
directories and files can then be combined together to form a software
release.

%package doc
Summary: Additional documentation for CVS.
Group: Documentation
Requires: %name = %version-%release

%description doc
Additional documentation for the Concurrent Versions System (CVS).

%package contrib
Summary: Contributed scripts for CVS.
Group: Development/Tools
Requires: mktemp >= 1:1.3.1
Requires: %name = %version-%release

%description contrib
Additional scripts for the Concurrent Versions System (CVS).

%prep
%setup -q

# Remove useless/harmful stuff to ensure it will not be suddently used
rm -rf emx os2 windows-NT vms zlib
find -type f \( -name getopt\* -o -name regex.\* -o -name getdate.c \) -delete -print

# Fix DOS-style lines
r=$(printf '\r')
find contrib -type f -print0 |
	xargs -r0 grep -Zl "$r\$" -- |
	xargs -r0 sed -i "s/$r\$//g" --
unset r

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1

# Second part of the tmp handling fix
sed -i 's|${TMPDIR}/cvs-serv|${TMPDIR:-/tmp}/cvs-serv|g' src/sanity.sh

# Fix texinfo warnings
sed -i 's/@strong{Note:/@strong{Please notice:/' doc/cvs.texinfo

%{expand:%%define optflags %optflags -Wall -D_GNU_SOURCE}

%build
export ac_cv_func_mkstemp=yes \
	ac_cv_lib_nsl_main=no \
	ac_cv_path_CSH=/bin/csh \
	ac_cv_path_PERL=%__perl \
	ac_cv_path_PS2PDF=/usr/bin/ps2pdf \
	ac_cv_path_ROFF=/usr/bin/groff \
	ac_cv_path_SENDMAIL=/usr/sbin/sendmail \
	ac_cv_path_TEXI2DVI=/usr/bin/texi2dvi

autoreconf -fisv
%configure \
	--without-krb4 \
	--without-gssapi \
	--with-tmpdir=/tmp \
	--with-editor=/bin/vitmp

%__make LDFLAGS=-s
bzip2 -9 FAQ NEWS
%{?_enable_check:TMPDIR=/tmp %__make check}

%install
rm -rf %buildroot

%makeinstall

cd %buildroot
find .%_datadir/cvs -type f -print0 | xargs -r0 chmod -x --
chmod 755 .%_datadir/cvs/contrib/rcs2log

# Remove unpackaged files if any
rm -f %buildroot%_infodir/dir

%post
/sbin/install-info %_infodir/cvs.info %_infodir/dir
/sbin/install-info %_infodir/cvsclient.info %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/cvs.info %_infodir/dir
	/sbin/install-info --delete %_infodir/cvsclient.info %_infodir/dir
fi

%files
%defattr(-,root,root)
%_bindir/cvs*
%_mandir/*/*
%_infodir/*.info*

%files doc
%defattr(-,root,root)
%doc AUTHORS BUGS FAQ.bz2 MINOR-BUGS NEWS.bz2 PROJECTS TODO README
%doc doc/RCSFILES doc/*.pdf

%files contrib
%defattr(-,root,root)
%_bindir/rcs2log
%_datadir/cvs

%changelog
* Mon Nov 14 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.11.21-owl1
- Updated to 1.11.21.

* Thu Sep 29 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1.11.20-owl1
- Updated to 1.11.20.
- Reviewed Owl patches, removed obsolete ones.
- Imported a bunch of patches from ALT's cvs-1.11.20-alt2 package, including:
change of external program from rsh to ssh for :ext: access method;
LocalKeyword and KeywordExpand support like in cvs-1.12.x;
CVS_LOCAL_BRANCH_NUM variable support like in cvs-1.12.x;
global cvsrc file (/etc/cvs/cvsrc) support;
tagloginfo support;
- Corrected info files installation.

* Sat Sep 11 2004 Solar Designer <solar-at-owl.openwall.com> 1.11.5-owl8
- Use RPM's exclude macro on info dir file.

* Thu Jun 03 2004 Solar Designer <solar-at-owl.openwall.com> 1.11.5-owl7
- Added back-ports of further CVS security fixes to CAN-2004-0414,
CAN-2004-0416, CAN-2004-0417, CAN-2004-0418, and to some minor bugs which
didn't appear to deserve CVE names.  Thanks to Stefan Esser, Sebastian
Krahmer, and Derek Robert Price for finding and fixing these.

* Tue May 18 2004 Solar Designer <solar-at-owl.openwall.com> 1.11.5-owl6
- Added Derek Robert Price's fix for the CVS server heap-based buffer
overflow vulnerability in processing of malformed "Entry" lines in
combination with "Is-modified" and "Unchanged" discovered by Stefan Esser.

* Tue Apr 13 2004 Michail Litvak <mci-at-owl.openwall.com> 1.11.5-owl5
- Patch to fix CVS pserver client side remote exploit.
- Fixed that using the -p option to cvs checkout sidesteps the
check that verifies the path isn't outside the repository.

* Fri Dec 12 2003 Solar Designer <solar-at-owl.openwall.com> 1.11.5-owl4
- Back-ported a patch from CVS 1.11.10 to reject absolute module paths.

* Sat Jun 28 2003 Solar Designer <solar-at-owl.openwall.com> 1.11.5-owl3
- Updated the canonicalize patch to avoid using _GNU_SOURCE but rather
declare the prototype for canonicalize_file_name() explicitly.  With
_GNU_SOURCE, we could get function prototype conflicts on certain other
glibc functions that cvs overrides (this actually caused the package to
not build on Alpha).
- Handle the special case when the last path component doesn't yet exist
and thus can't be canonicalized.

* Thu May 01 2003 Solar Designer <solar-at-owl.openwall.com> 1.11.5-owl2
- BuildRequires: mktemp >= 1:1.3.1 (but don't yet require mktemp for the
package itself because it won't be needed for most uses; the scripts will
need to be moved to a subpackage).
- Don't let the cvsbug script unlink one of its temporary files and then
re-use its name.
- Moved the documentation and contributed scripts into subpackages.

* Thu May 01 2003 Solar Designer <solar-at-owl.openwall.com> 1.11.5-owl1
- Re-worked the temporary file handling patch to make it actually do what
it was supposed to and cover more scripts and the documentation.
- Force configure to use /tmp for the default temporary file directory,
and not pick and store $TMPDIR that was set at build time.
- Use vitmp with cvsbug, rcs-to-cvs, and cvs itself.
- Enable mkstemp explicitly, not rely on configure.
- Patched 47 gcc -Wall warnings (all of them), including some real bugs.
- Patched cvs to not create world-writable files (val-tags, dbm).
- Canonicalize paths to avoid a failed assertion on "cvs rdiff" and maybe
other commands if $CVSROOT contains symlinks.
- chmod -x most scripts in contrib/ to prevent bogus dependencies on perl
and csh.

* Mon Mar 24 2003 Simon B <simonb-at-owl.openwall.com> 1.11.5-owl0.1
- Pulled in mktemp fixes from ALT Linux
- Disable {Checkin,Update}-prog
- General tidying up based on suggestions from Solar Designer

* Fri Mar 14 2003 Simon B <simonb-at-owl.openwall.com>
- initial Owl spec file
- compile CVS dynamically against zlib instead of using the version
included with the CVS source.
