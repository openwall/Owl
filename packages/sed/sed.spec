# $Id: Owl/packages/sed/sed.spec,v 1.4 2002/08/26 17:30:23 mci Exp $

Summary: A GNU stream text editor.
Name: sed
Version: 3.02
Release: owl9
License: GPL
Group: Applications/Text
Source: ftp://ftp.gnu.org/gnu/sed/sed-%{version}.tar.gz
Patch: sed-3.02-owl-info.diff 
PreReq: /sbin/install-info
Prefix: %{_prefix}
BuildRoot: /override/%{name}-%{version}

%description
The sed (Stream EDitor) editor is a stream or batch (non-interactive)
editor.  sed takes text as input, performs an operation or set of
operations on the text and outputs the modified text.  The operations
that sed performs (substitutions, deletions, insertions, etc.) can be
specified in a script file or from the command line.

%prep
%setup -q
%patch -p1

%build
rm doc/sed.info
%configure
make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

cd $RPM_BUILD_ROOT
mv .%{_bindir} bin

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/sed.info.gz %{_infodir}/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/sed.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
%doc ANNOUNCE BUGS NEWS README TODO
/bin/sed
%{_infodir}/*.info*
%{_mandir}/man*/*

%changelog
* Mon Aug 19 2002 Michail Litvak <mci@owl.openwall.com>
- Deal with info dir entries such that the menu looks pretty.

* Wed Feb 06 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- import spec from RH rawhide
- fix URL
