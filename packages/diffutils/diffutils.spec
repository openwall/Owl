# $Id: Owl/packages/diffutils/diffutils.spec,v 1.3 2001/01/04 06:28:51 solar Exp $

Summary: A GNU collection of diff utilities.
Name: 		diffutils
Version: 	2.7
Release: 	23owl
Group: 		Applications/Text
URL: 		http://www.gnu.org/software/diffutils/diffutils.html
Source: 	ftp://ftp.gnu.org/gnu/diffutils/diffutils-%{version}.tar.gz
Source1: 	cmp.1
Source2: 	diff.1
Source3:	diff3.1
Source4: 	sdiff.1
Patch0:		diffutils-2.7-immunix-owl-tmp.diff
License: 	GPL
Prefix: 	%{_prefix}
Prereq: 	/sbin/install-info
Buildroot: 	/var/rpm-buildroot/%{name}-root

%description
Diffutils includes four utilities: diff, cmp, diff3 and sdiff. Diff
compares two files and shows the differences, line by line.  The cmp
command shows the offset and line numbers where two files differ, or
cmp can show the characters that differ between the two files.  The
diff3 command shows the differences between three files.  Diff3 can be
used when two people have made independent changes to a common
original; diff3 can produce a merged file that contains both sets of
changes and warnings about conflicts.  The sdiff command can be used
to merge two files interactively.

Install diffutils if you need to compare text files.

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
gzip -9nf .%{_infodir}/diff*
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
%{_infodir}/diff.info*gz

%changelog
* Wed Jan 03 2001 Solar Designer <solar@owl.openwall.com>
- Fixed the unsafe temporary file creation discovered by the Immunix team
and reported to vendor-sec by Greg KH <greg@wirex.com>.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import spec from RH

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jul 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fix %%changelog entries (escape them)
- update source location
- remove manual stripping
- add URL

* Tue Jun 06 2000 Than Ngo <than@redhat.de>
- add %%defattr
- use rpm macros

* Wed May 31 2000 Ngo Than <than@redhat.de>
- put man pages and info files in correct place
- cleanup specfile

* Thu Feb 03 2000 Preston Brown <pbrown@redhat.com>
- rebuild to gzip man pages.

* Mon Apr 19 1999 Jeff Johnson <jbj@redhat.com>
- man pages not in %%files.
- but avoid conflict for diff.1

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 14)

* Sun Mar 14 1999 Jeff Johnson <jbj@redhat.com>
- add man pages (#831).
- add %%configure and Prefix.

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Tue Jul 14 1998 Bill Kawakami <billk@home.com>
- included the four man pages stolen from Slackware

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sun May 03 1998 Cristian Gafton <gafton@redhat.com>
- fixed spec file to reference/use the $RPM_BUILD_ROOT always
    
* Wed Dec 31 1997 Otto Hammersmith <otto@redhat.com>
- fixed where it looks for 'pr' (/usr/bin, rather than /bin)

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- added BuildRoot

* Sun Sep 14 1997 Erik Troan <ewt@redhat.com>
- uses install-info

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
