# $Id: Owl/packages/grep/grep.spec,v 1.1 2000/07/29 21:16:44 kad Exp $

Summary: The GNU versions of grep pattern matching utilities.
Name: 		grep
Version: 	2.4.2
Release: 	1owl
Serial:  	1
Copyright: 	GPL
Group: 		Applications/Text
Source: 	ftp://ftp.gnu.org/pub/gnu/grep/grep-%{version}.tar.gz
Prefix: 	%{_prefix}
Prereq: 	/sbin/install-info
Packager:       <kad@owl.openwall.com>
BuildRoot:      /var/rpm-buildroot/%{name}-root


%description
The GNU versions of commonly used grep utilities.  Grep searches
through textual input for lines which contain a match to a specified
pattern and then prints the matching lines.  GNU's grep utilities
include grep, egrep and fgrep.

You should install grep on your system, because it is a very useful
utility for searching through text.

%prep
%setup -q

%build
unset LINGUAS || :

%configure
make

%install
rm -rf ${RPM_BUILD_ROOT}
%makeinstall LDFLAGS=-s prefix=${RPM_BUILD_ROOT}%{_prefix} exec_prefix=${RPM_BUILD_ROOT}
%ifos Linux
mkdir -p $RPM_BUILD_ROOT/bin
mv $RPM_BUILD_ROOT%{_prefix}/bin/* $RPM_BUILD_ROOT/bin
rm -rf $RPM_BUILD_ROOT%{_prefix}/bin
%endif
gzip -9f $RPM_BUILD_ROOT%{_infodir}/grep*

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/install-info --quiet --info-dir=%{_infodir} %{_infodir}/grep.info.gz

%preun
if [ $1 = 0 ]; then
	/sbin/install-info --quiet --info-dir=%{_infodir} --delete %{_infodir}/grep.info.gz
fi

%files
%defattr(-,root,root)
%doc ABOUT-NLS AUTHORS THANKS TODO NEWS README ChangeLog

%ifos Linux
/bin/*
%else
%{_prefix}/bin/*
%endif
%{_infodir}/*.info.gz
%{_mandir}/*/*
%{_prefix}/share/locale/*/*/grep.*

%changelog
* Sun Jul 30 2000 Alexandr D. Kanevskiy <kad@owl.openwall.com>
- imported from RH
- locales fix
