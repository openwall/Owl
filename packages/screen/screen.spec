# $Id: Owl/packages/screen/screen.spec,v 1.2 2001/03/08 00:01:36 mci Exp $

Summary: A screen manager that supports multiple logins on one terminal.
Name: screen
Version: 3.9.8
Release: 4owl
Copyright: GPL
Group: Applications/System
Source0: ftp://ftp.uni-erlangen.de/pub/utilities/screen/screen-%{version}.tar.gz
Source1: screen.pam
Patch0: screen-3.9.8-deb-rh-os.diff
Patch1: screen-3.9.8-owl-config.diff
Patch2: screen-3.9.8-owl-pam.diff
Patch3: screen-3.9.8-deb-owl-bufferfile.diff
Patch4: screen-3.9.8-deb-pty.diff
Patch5: screen-3.9.8-deb-owl-mans.diff
Patch6: screen-3.9.8-rh-deletehack.diff
Patch7: screen-3.9.8-rh-docbug.diff
Prefix: %{_prefix}
BuildRoot: /var/rpm-buildroot/%{name}-root
Prereq: /sbin/install-info, pam_userpass, utempter
BuildPreReq: pam >= 0.72-8owl


%description
The screen utility allows you to have multiple logins on just one
terminal.  Screen is useful for users who telnet into a machine or are
connected via a dumb terminal, but want to use more than just one
login.

Install the screen package if you need a screen manager that can
support multiple logins on one terminal.

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

%build

autoconf
%configure --disable-socket-dir

rm doc/screen.info*

make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/skel

%makeinstall

pushd $RPM_BUILD_ROOT
rm -f .%{_bindir}/screen.old .%{_bindir}/screen
mv .%{_bindir}/screen-%{version} .%{_bindir}/screen
strip .%{_bindir}/screen
popd

install -c -m 0444 etc/etcscreenrc $RPM_BUILD_ROOT/etc/screenrc
install -c -m 0644 etc/screenrc $RPM_BUILD_ROOT/etc/skel/.screenrc
install -d $RPM_BUILD_ROOT/etc/pam.d
install -m 600 %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/screen

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/screen.info.gz %{_infodir}/dir --entry="* screen: (screen).             Terminal multiplexer."

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/screen.info.gz %{_infodir}/dir --entry="* screen: (screen).             Terminal multiplexer."
fi

%files
%defattr(-,root,root)
%doc NEWS README FAQ doc/README.DOTSCREEN

%attr(2755,root,utempter) %{_bindir}/screen
%{_mandir}/man1/screen.*
%{_infodir}/screen.info*

%config /etc/screenrc
%config /etc/skel/.screenrc
%attr(0644,root,root) %config(noreplace) /etc/pam.d/screen

%changelog
* Thu Mar 08 2001 Michail Litvak <mci@owl.openwall.com>
- Many patches removed and other has reworked

* Sat Mar 03 2001 Michail Litvak <mci@owl.openwall.com>
- Added patches imported from Debian, RedHat
- PAM support for screen locking over pam_userpass

* Wed Jan 10 2001 Tim Waugh <twaugh@redhat.com>
- Rebuild, which will hopefully fix bug #22537

* Sun Oct 01 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 3.9.8
- change the .jbj patch and add some more "user" -> "auser" cases

* Thu Aug 15 2000 Crutcher Dunnavant <crutcher@redhat.com>
- Patched the documentation to change the 'C-a C-\' to 'C-a \',
- which is what is the real behaviour. this fixes bug #16103

* Thu Aug  3 2000 Crutcher Dunnavant <crutcher@redhat.com>
- Fixed my fix, so that the hack goes in the /global/ file :)

* Thu Aug  3 2000 Crutcher Dunnavant <crutcher@redhat.com>
- Stuck an entry into the default screenrc file that forces
- '^?' (backspace) to send '^H'.
- Its an ugly fix for a termcap inheritance problem,
- but it works, if anyone REALLY needs '^?' they can change it,
- and I think we anger less people with this than the way it 
- currently behaves. (Read: vi and emacs work now)
- POST NOTE (Aug 15): emacs is NOT happy with ^H, BUT screen thinks
- that this is what backspace is supposed to do, so we don't change it.

* Thu Aug  3 2000 Crutcher Dunnavant <crutcher@redhat.com>
- Fixed some conflicting descriptions in the documentation

* Thu Aug  3 2000 Crutcher Dunnavant <crutcher@redhat.com>
- got a patch from rzm@icm.edu.pl to fix bug #10353
- which caused screen to crash when copying to a file buffer

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jun 10 2000 Bill Nottingham <notting@redhat.com>
- rebuild, FHS tweaks

* Sat May  6 2000 Bill Nottingham <notting@redhat.com>
- fix build for ia64

* Mon Apr  3 2000 Bernhard Rosenkränzer <bero@redhat.com>
- rebuild with new ncurses

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Tue Feb 15 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Fix MD5 password support (Bug #9463)

* Thu Feb  3 2000 Bill Nottingham <notting@redhat.com>
- handle compressed man pages

* Fri Dec 10 1999 Bill Nottingham <notting@redhat.com>
- update to 3.9.5

* Wed Oct 20 1999 Bill Nottingham <notting@redhat.com>
- you know, we weren't just patching in Unix98 pty support for fun.

* Wed Aug 18 1999 Bill Nottingham <notting@redhat.com>
- put screendir in ~

* Wed Aug 18 1999 Jeff Johnson <jbj@redhat.com>
- update to 3.9.4.

* Wed Jun 16 1999 Bill Nottingham <notting@redhat.com>
- force tty permissions/group

* Wed Jun 5 1999 Dale Lovelace <dale@redhat.com>
- permissions on /etc/skel/.screenrc to 644

* Mon Apr 26 1999 Bill Nottingham <notting@redhat.com>
- take out warning of directory permissions so root can still use screen

* Wed Apr 07 1999 Bill Nottingham <notting@redhat.com>
- take out warning of directory ownership so root can still use screen

* Wed Apr 07 1999 Erik Troan <ewt@redhat.com>
- patched in utempter support, turned off setuid bit

* Fri Mar 26 1999 Erik Troan <ewt@redhat.com>
- fixed unix98 pty support

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Thu Mar 11 1999 Bill Nottingham <notting@redhat.com>
- add patch for Unix98 pty support

* Mon Dec 28 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.7.6.

* Sun Aug 16 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- upgraded to 3.7.4

* Wed Oct 08 1997 Erik Troan <ewt@redhat.com>
- removed glibc 1.99 specific patch

* Tue Sep 23 1997 Erik Troan <ewt@redhat.com>
- added install-info support

* Mon Jul 21 1997 Erik Troan <ewt@redhat.com>
- built against glibc
