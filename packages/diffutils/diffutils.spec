# $Owl: Owl/packages/diffutils/diffutils.spec,v 1.23 2010/08/25 06:23:19 segoon Exp $

Summary: A GNU collection of diff utilities.
Name: diffutils
Version: 3.0
Release: owl3
License: GPL
Group: Applications/Text
URL: http://www.gnu.org/software/diffutils/
# ftp://ftp.gnu.org/gnu/%name/%name-%version.tar.gz
Source: %name-%version.tar.bz2
Patch0: diffutils-2.8.7-owl-info.diff
Patch1: diffutils-3.0-owl-nanoseconds.diff
PreReq: /sbin/install-info
Prefix: %_prefix
BuildRequires: texinfo
BuildRequires: rpm-build >= 0:4
BuildRoot: /override/%name-%version

%description
diffutils includes four utilities: diff, cmp, diff3, and sdiff.  diff
compares two files and shows the differences, line by line.  The cmp
command shows the offset and line numbers where two files differ, or
cmp can show the characters that differ between the two files.  The
diff3 command shows the differences between three files.  diff3 can be
used when two people have made independent changes to a common
original; diff3 can produce a merged file that contains both sets of
changes and warnings about conflicts.  The sdiff command can be used
to merge two files interactively.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
# Disable nanoseconds in diff output.
#export ac_cv_struct_st_mtim_nsec=no ac_cv_search_clock_gettime='none required'
# Predefine location of the pr utility.
export PR_PROGRAM=%_bindir/pr
%configure
make

%check
make check

%install
rm -rf %buildroot
%makeinstall

# Remove unpackaged files
rm %buildroot%_infodir/dir

%post
/sbin/install-info %_infodir/diff.info %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/diff.info %_infodir/dir
fi

%files
%defattr(-,root,root)
%doc AUTHORS NEWS README THANKS
%_bindir/*
%_mandir/*/*
%_infodir/diff.info*
%_datadir/locale/*/LC_MESSAGES/diffutils.mo

%changelog
* Wed Aug 25 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 3.0-owl3
- Do not use nanoseconds in diffs.

* Wed Aug 24 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 3.0-owl2
- Packaged diff.1 again (man-pages doesn't provide it anymore).

* Wed Aug 18 2010 Vasiliy Kulikov <segoon-at-owl.openwall.com> 3.0-owl1
- Updated to 3.0.
- Dropped -alt-i18n and -rh-warnings patches (fixed in upstream).
- Dropped -alt-backup_suffix patch.

* Tue May 17 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 2.8.7-owl1
- Updated to 2.8.7.
- Imported a bunch of patches from ALT's diffutils-2.8.7-alt1 package.
- Corrected info files installation.
- Packaged diffutils translations.

* Wed Oct 29 2003 Solar Designer <solar-at-owl.openwall.com> 2.7-owl25
- Dropped diff.1 from this package as it exists in man-pages.

* Mon Aug 19 2002 Michail Litvak <mci-at-owl.openwall.com> 2.7-owl24
- Deal with info dir entries such that the menu looks pretty.

* Thu Jan 24 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Wed Jan 03 2001 Solar Designer <solar-at-owl.openwall.com>
- Fixed the unsafe temporary file creation discovered by the Immunix team
and reported to vendor-sec by Greg KH <greg at wirex.com>.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import spec from RH
