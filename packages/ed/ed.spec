# $Id: Owl/packages/ed/ed.spec,v 1.4 2000/11/23 13:46:07 mci Exp $

Summary: The GNU line editor.
Name: ed
Version: 0.2
Release: 19owl
Copyright: GPL
Group: Applications/Text
Source: ftp://ftp.gnu.org/gnu/%{name}-%{version}.tar.gz
Patch0: ed-0.2-deb-mkfile.diff
Patch1: ed-0.2-deb-parentheses.diff
Patch2: ed-0.2-owl-mkstemp.diff
Prereq: /sbin/install-info
Prefix: %{_prefix}
Buildroot: /var/rpm-buildroot/%{name}-root

%description
Ed is a line-oriented text editor, used to create, display, and modify
text files (both interactively and via shell scripts).  For most
purposes, ed has been replaced in normal usage by full-screen editors
(emacs and vi, for example).

Ed was the original UNIX editor, and may be used by some programs.  In
general, however, you probably don't need to install it and you probably
won't use it.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
chmod 755 configure
autoconf
%configure --exec-prefix=/
make LDFLAGS=-s

%install
%makeinstall bindir=$RPM_BUILD_ROOT/bin \
	     mandir=$RPM_BUILD_ROOT%{_mandir}/man1

%post
/sbin/install-info %{_infodir}/ed.info.gz %{_infodir}/dir --entry="* ed: (ed).                  The GNU Line Editor."

%preun
if [ $1 = 0 ] ; then
  /sbin/install-info --delete %{_infodir}/ed.info.gz %{_infodir}/dir --entry="* ed: (ed).                  The GNU Line Editor."
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc NEWS POSIX README THANKS
/bin/*
%{_infodir}/ed.info*
%{_mandir}/*/*

%changelog
* Wed Nov 22 2000 Michail Litvak <mci@owl.openwall.com>
- imported from RH
- patches from Debian 
- ed-0.2-deb-mkfile.diff: don't compile in 
  libed.a as it's redundant old code   superseded by code in glibc.  
  This reduces the ed binary by 23k.
- ed-0.2-deb-parentheses.diff: parentheses to quiet -Wall
- ed-0.2-deb-tmpnam.diff: Patched buf.c to use tempnam()

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Than Ngo <than@redhat.de>
- fix typo

* Sat Jun 17 2000 Than Ngo <than@redhat.de>
- add %%defattr
- clean up specfile

* Sat May 20 2000 Ngo Than <than@redhat.de>
- rebuild for 7.0
- put man pages and infos in right place

* Thu Feb 03 2000 Preston Brown <pbrown@redhat.com>
- rebuild to gzip man pages.

* Tue Mar 23 1999 Jeff Johnson <jbj@redhat.com>
- fix %post syntax error (#1689).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 11)

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Fri Dec 18 1998 Preston Brown <pbrown@redhat.com>
- bumped spec number for initial rh 6.0 build

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- added install-info support
- added BuildRoot
- correct URL in Source line

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
