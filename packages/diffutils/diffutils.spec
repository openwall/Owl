# $Id: Owl/packages/diffutils/diffutils.spec,v 1.4 2002/01/24 17:46:53 solar Exp $

Summary: A GNU collection of diff utilities.
Name: diffutils
Version: 2.7
Release: owl23
License: GPL
Group: Applications/Text
URL: http://www.gnu.org/software/diffutils/diffutils.html
Source0: ftp://ftp.gnu.org/gnu/diffutils/diffutils-%{version}.tar.gz
Source1: cmp.1
Source2: diff.1
Source3: diff3.1
Source4: sdiff.1
Patch0: diffutils-2.7-immunix-owl-tmp.diff
PreReq: /sbin/install-info
Prefix: %{_prefix}
BuildRoot: /override/%{name}-%{version}

%description
Diffutils includes four utilities: diff, cmp, diff3 and sdiff. Diff
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
make PR_PROGRAM=%{_bindir}/pr

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

cd $RPM_BUILD_ROOT
mkdir -p .%{_mandir}/man1
for manpage in %{SOURCE1} %{SOURCE3} %{SOURCE4}; do
	install -m 0644 ${manpage} .%{_mandir}/man1
done

%post
/sbin/install-info %{_infodir}/diff.info.gz %{_infodir}/dir --entry="* diff: (diff).                 The GNU diff."

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/diff.info.gz %{_infodir}/dir --entry="* diff: (diff).                 The GNU diff."
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc NEWS README
%{_bindir}/*
%{_mandir}/*/*
%{_infodir}/diff.info*

%changelog
* Thu Jan 24 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Wed Jan 03 2001 Solar Designer <solar@owl.openwall.com>
- Fixed the unsafe temporary file creation discovered by the Immunix team
and reported to vendor-sec by Greg KH <greg@wirex.com>.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import spec from RH
