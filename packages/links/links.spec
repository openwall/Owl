# $Id: Owl/packages/links/Attic/links.spec,v 1.1 2001/06/02 21:22:47 mci Exp $
Name: links
Summary: text mode www browser with support for frames
Version: 0.95
Release: 1owl
Copyright: GPL
Source: http://artax.karlin.mff.cuni.cz/~mikulas/links/download/%{name}-%{version}.tar.gz
Group: Applications/Internet
BuildRoot: /var/rpm-buildroot/%{name}-%{version}
Patch0: links-0.95-asp-koi.diff
Patch1: links-0.95-owl-mkstemp.diff

%description
Links is a character mode world wide web browser. It supports colors,
correct table and frames rendering, international codepages and user
interfaces, background downloads, multiple connected instances, small
and fast.
                                                                      
Links have preliminary support for password authentication (it works a
lmost in every cases), cookies (in-memory only), and simple bookmarks.

It does not yet support saving cookies to disk, mailcap. It supports S
SL, but it's still in the testing phase - if it breaks, don't use it. :-)

%prep
%setup -q

%patch0 -p1
%patch1 -p1

%build
%{configure}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README SITES TODO
%{_bindir}/links

%changelog
* Sat Jun 02 2001 Michail Litvak <mci@owl.openwall.com>
- spec file imported from ASP linux 
- patch to replace tempnam to mkstemp
