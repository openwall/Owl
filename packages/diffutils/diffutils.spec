# $Id: Owl/packages/diffutils/diffutils.spec,v 1.13 2005/10/23 21:09:44 solar Exp $

Summary: A GNU collection of diff utilities.
Name: diffutils
Version: 2.8.7
Release: owl1
License: GPL
Group: Applications/Text
URL: http://www.gnu.org/software/diffutils/
Source0: ftp://alpha.gnu.org/pub/gnu/%name/%name-%version.tar.gz
Patch0: diffutils-2.8.7-owl-info.diff
Patch1: diffutils-2.8.7-rh-warnings.diff
Patch2: diffutils-2.8.7-alt-tmp.diff
Patch3: diffutils-2.8.7-alt-i18n.diff
Patch4: diffutils-2.8.7-alt-backup_suffix.diff
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
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
# Disable nanoseconds in diff output.
export ac_cv_struct_st_mtim_nsec=no ac_cv_search_clock_gettime='none required'
# Predefine location of the pr utility.
export PR_PROGRAM=%_bindir/pr
%configure
make

%install
rm -rf %buildroot
%makeinstall

# Remove unpackaged files if any
rm -f %buildroot%_infodir/dir

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
# diff(1) manpage still lives in man-pages package
%exclude %_mandir/man1/diff.*

%changelog
* Tue May 17 2005 Dmitry V. Levin <ldv@owl.openwall.com> 2.8.7-owl1
- Updated to 2.8.7.
- Imported a bunch of patches from ALT's diffutils-2.8.7-alt1 package.
- Corrected info files installation.
- Packaged diffutils translations.

* Wed Oct 29 2003 Solar Designer <solar@owl.openwall.com> 2.7-owl25
- Dropped diff.1 from this package as it exists in man-pages.

* Mon Aug 19 2002 Michail Litvak <mci@owl.openwall.com> 2.7-owl24
- Deal with info dir entries such that the menu looks pretty.

* Thu Jan 24 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Wed Jan 03 2001 Solar Designer <solar@owl.openwall.com>
- Fixed the unsafe temporary file creation discovered by the Immunix team
and reported to vendor-sec by Greg KH <greg@wirex.com>.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import spec from RH
