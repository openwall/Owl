# $Id: Owl/packages/screen/screen.spec,v 1.20 2002/02/05 15:06:49 solar Exp $

Summary: A screen manager that supports multiple sessions on one terminal.
Name: screen
Version: 3.9.10
Release: owl2
License: GPL
Group: Applications/System
Source0: ftp://ftp.uni-erlangen.de/pub/utilities/screen/screen-%{version}.tar.gz
Source1: screen.pam
Patch0: screen-3.9.9-owl-os.diff
Patch1: screen-3.9.9-owl-config.diff
Patch2: screen-3.9.9-owl-pam.diff
Patch3: screen-3.9.9-deb-owl-bufferfile.diff
Patch4: screen-3.9.9-deb-pty.diff
Patch5: screen-3.9.9-deb-owl-mans.diff
Patch6: screen-3.9.9-rh-deletehack.diff
Patch7: screen-3.9.9-rh-docbug.diff
Patch8: screen-3.9.9-owl-telnet.diff
Patch9: screen-3.9.10-owl-tmp.diff
PreReq: /sbin/install-info
Requires: tcb, pam_userpass, utempter
Prefix: %{_prefix}
BuildRequires: pam-devel
BuildRoot: /override/%{name}-%{version}

%description
The screen utility allows you to have multiple interactive sessions on
just one terminal and keep the sessions over disconnects.  screen is
useful for remote users or users who are connected via a serial line
but want to use more than one session.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

%{expand:%%define optflags %optflags -Wall}

%build
autoconf
%configure --disable-socket-dir

rm doc/screen.info*

make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/pam.d

%makeinstall

pushd $RPM_BUILD_ROOT
rm -f .%{_bindir}/screen.old .%{_bindir}/screen
mv .%{_bindir}/screen-%{version} .%{_bindir}/screen
popd

install -m 644 etc/etcscreenrc $RPM_BUILD_ROOT/etc/screenrc
install -m 644 $RPM_SOURCE_DIR/screen.pam $RPM_BUILD_ROOT/etc/pam.d/screen

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/screen.info.gz %{_infodir}/dir \
	--entry="* screen: (screen).             Terminal multiplexer."

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/screen.info.gz %{_infodir}/dir \
		--entry="* screen: (screen).             Terminal multiplexer."
fi

%files
%defattr(-,root,root)
%doc NEWS README doc/FAQ doc/README.DOTSCREEN etc/screenrc
%attr(2711,root,utempter) %{_bindir}/screen
%{_mandir}/man1/screen.1.*
%{_infodir}/screen.info*
%config(noreplace) /etc/screenrc
%config(noreplace) /etc/pam.d/screen

%changelog
* Tue Feb 05 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Fri Nov 16 2001 Solar Designer <solar@owl.openwall.com>
- Use pam_tcb.
- Build with -Wall.

* Tue Nov 13 2001 Solar Designer <solar@owl.openwall.com>
- Corrected the package description.

* Tue Nov 13 2001 Michail Litvak <mci@owl.openwall.com>
- 3.9.10
- more tmp fixes in configure

* Sun Oct 07 2001 Solar Designer <solar@owl.openwall.com>
- Updates to appl_userpass.c to support building against Linux-PAM 0.74+.

* Fri Aug 03 2001 Michail Litvak <mci@owl.openwall.com>
- install doc/FAQ as FAQ instead link to doc/FAQ

* Wed Jun 13 2001 Michail Litvak <mci@owl.openwall.com>
- updated to 3.9.9
- patch configure to avoid non secure file creation in /tmp

* Mon Mar 19 2001 Solar Designer <solar@owl.openwall.com>
- screen.pam: explicit pam_deny for everything but authentication.

* Sat Mar 10 2001 Solar Designer <solar@owl.openwall.com>
- Don't require and link against libpam_misc.

* Sat Mar 10 2001 Michail Litvak <mci@owl.openwall.com>
- example user's .screenrc moved to doc
- added patch to builtin telnet (bcopy->memmove)
- spec, patches cleanups

* Thu Mar 08 2001 Michail Litvak <mci@owl.openwall.com>
- Many patches removed and other reworked

* Sat Mar 03 2001 Michail Litvak <mci@owl.openwall.com>
- Added patches imported from Debian, RedHat
- PAM support for screen locking via pam_userpass
