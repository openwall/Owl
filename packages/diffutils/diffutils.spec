# $Id: Owl/packages/diffutils/diffutils.spec,v 1.8 2003/10/29 18:56:15 solar Exp $

Summary: A GNU collection of diff utilities.
Name: diffutils
Version: 2.7
Release: owl25
License: GPL
Group: Applications/Text
URL: http://www.gnu.org/software/diffutils/diffutils.html
Source0: ftp://ftp.gnu.org/gnu/diffutils/diffutils-%version.tar.gz
Source1: cmp.1
Source2: diff3.1
Source3: sdiff.1
Patch0: diffutils-2.7-immunix-owl-tmp.diff
PreReq: /sbin/install-info
Prefix: %_prefix
BuildRoot: /override/%name-%version

%description
Diffutils includes four utilities: diff, cmp, diff3, and sdiff.  diff
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

%build
autoconf
%configure
make PR_PROGRAM=%_bindir/pr

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

cd $RPM_BUILD_ROOT
mkdir -p .%_mandir/man1
for manpage in cmp.1 diff3.1 sdiff.1; do
	install -m 644 $RPM_SOURCE_DIR/$manpage .%_mandir/man1/
done

%post
/sbin/install-info %_infodir/diff.info.gz %_infodir/dir \
	--entry="* diff: (diff).                                 The GNU diff."

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/diff.info.gz %_infodir/dir \
		--entry="* diff: (diff).                                 The GNU diff."
fi

%files
%defattr(-,root,root)
%doc NEWS README
%_bindir/*
%_mandir/*/*
%_infodir/diff.info*

%changelog
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
