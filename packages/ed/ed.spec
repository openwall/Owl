# $Id: Owl/packages/ed/ed.spec,v 1.8 2002/01/31 09:54:43 mci Exp $

Summary: The GNU line editor.
Name: ed
Version: 0.2
Release: owl19
License: GPL
Group: Applications/Text
Source: ftp://ftp.gnu.org/gnu/%{name}-%{version}.tar.gz
Patch0: ed-0.2-deb-mkfile.diff
Patch1: ed-0.2-deb-parentheses.diff
Patch2: ed-0.2-owl-mkstemp.diff
PreReq: /sbin/install-info
Prefix: %{_prefix}
BuildRoot: /override/%{name}-%{version}

%description
Ed is a line-oriented text editor, used to create, display, and modify
text files (both interactively and via shell scripts).  For most
purposes, ed has been replaced in normal usage by full-screen editors
(emacs and vi, for example).

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
/sbin/install-info %{_infodir}/ed.info.gz %{_infodir}/dir\
	--entry="* ed: (ed).                  The GNU Line Editor."

%preun
if [ $1 -eq 0 ] ; then
	/sbin/install-info --delete %{_infodir}/ed.info.gz %{_infodir}/dir\
		--entry="* ed: (ed).                  The GNU Line Editor."
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
* Wed Jan 30 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions.

* Thu Nov 23 2000 Michail Litvak <mci@owl.openwall.com>
- ed-0.2-deb-tmpnam.diff replaced by ed-0.2-owl-mkstemp.diff
  we must use mkstemp(3)

* Wed Nov 22 2000 Michail Litvak <mci@owl.openwall.com>
- imported from RH
- patches from Debian 
- ed-0.2-deb-mkfile.diff: don't compile in 
  libed.a as it's redundant old code   superseded by code in glibc.  
  This reduces the ed binary by 23k.
- ed-0.2-deb-parentheses.diff: parentheses to quiet -Wall
- ed-0.2-deb-tmpnam.diff: Patched buf.c to use tempnam()
