# $Id: Owl/packages/mutt/mutt.spec,v 1.3 2003/01/20 12:44:07 solar Exp $

Summary: A text mode mail user agent.
Name: mutt
Version: 1.4
Release: owl1
License: GPL
Group: Applications/Internet
URL: http://www.mutt.org
Source0: ftp://ftp.mutt.org/mutt/mutt-%{version}i.tar.gz
Source1: Muttrc-color
Patch0: mutt-1.4-owl-no-sgid.diff
Patch1: mutt-1.4-owl-muttbug-tmp.diff
Patch2: mutt-1.4-owl-tmp.diff
Conflicts: mutt-us
Provides: mutt-i
BuildRoot: /override/%{name}-%{version}

%description
Mutt is a text-mode mail user agent.  Mutt supports color, threading,
arbitrary key remapping, and a lot of customization.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
CFLAGS="$RPM_OPT_FLAGS" ./prepare --prefix=%{_prefix} \
	--with-sharedir=/etc --sysconfdir=/etc \
	--with-docdir=%{_docdir}/mutt-%{version} \
	--with-mandir=%{_mandir} \
	--with-infodir=%{_infodir} \
	--enable-pop --enable-imap \
	--with-ssl \
	--disable-domain \
	--disable-flock --enable-fcntl
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall \
	sharedir=$RPM_BUILD_ROOT/etc \
	sysconfdir=$RPM_BUILD_ROOT/etc \
	docdir=$RPM_BUILD_ROOT%{_docdir}/mutt-%{version} \
	install

# We like GPG here.
cat contrib/gpg.rc $RPM_SOURCE_DIR/Muttrc-color >> $RPM_BUILD_ROOT/etc/Muttrc

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%config /etc/Muttrc
%doc doc/*.txt
%doc contrib/*.rc README* contrib/sample.* NEWS TODO
%doc COPYRIGHT doc/manual.txt contrib/language* mime.types
%{_bindir}/mutt
%{_bindir}/muttbug
%{_bindir}/flea
%{_bindir}/pgpring
%{_bindir}/pgpewrap
%{_mandir}/man1/mutt.*
%{_mandir}/man5/muttrc.*
%{_mandir}/man1/flea.*

%changelog
* Mon Jan 20 2003 Solar Designer <solar@owl.openwall.com>
- Initial commit into Owl.

* Wed Jan 15 2003 Jarno Huuskonen <jhuuskon@owl.openwall.com>
- use mkstemp when creating temporary files.
- include locales and flea

* Wed Sep 25 2002 Solar Designer <solar@owl.openwall.com>
- Updated to 1.4, the package is still non-public.
- Don't use slang.

* Tue Jan 08 2002 Solar Designer <solar@owl.openwall.com>
- Based this spec file on Red Hat's, dropped most patches for now.
