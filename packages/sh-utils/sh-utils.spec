# $Id: Owl/packages/sh-utils/Attic/sh-utils.spec,v 1.1 2000/07/12 04:14:00 solar Exp $

Summary: A set of GNU utilities commonly used in shell scripts.
Name: sh-utils
Version: 2.0
Release: 1owl
Copyright: GPL
Group: System Environment/Shells
Source: ftp://ftp.gnu.org/pub/gnu/sh-utils/sh-utils-%{version}.tar.gz
Patch0: sh-utils-2.0-owl-no-su-hostname.diff
Patch1: sh-utils-2.0-rh-cest.diff
Patch2: sh-utils-2.0-rh-utmp.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Prereq: /sbin/install-info

%description
The GNU shell utilities are a set of useful system utilities which are
often used in shell scripts.  The sh-utils package includes basename
(to remove the path prefix from a specified pathname), chroot (to
change the root directory), date (to print/set the system time and
date), dirname (to remove the last level or the filename from a given
path), echo (to print a line of text), env (to display/modify the
environment), expr (to evaluate expressions), factor (to print prime
factors), false (to return an unsuccessful exit status), groups (to
print the groups a specified user is a member of), id (to print the
real/effective uid/gid), logname (to print the current login name),
nice (to modify a scheduling priority), nohup (to allow a command to
continue running after logging out), pathchk (to check a file name's
portability), printenv (to print environment variables), printf (to
format and print data), pwd (to print the current directory), seq (to
print numeric sequences), sleep (to suspend execution for a specified
time), stty (to print/change terminal settings), tee (to send output
to multiple files), test (to evaluate an expression), true (to return
a successful exit status), tty (to print the terminal name), uname
(to print system information), users (to print current users' names),
who (to print a list of the users who are currently logged in),
whoami (to print the effective user id), and yes (to print a string
indefinitely).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

# XXX docs should say /var/run/[uw]tmp not /etc/[uw]tmp
perl -pi -e 's,/etc/utmp,/var/run/utmp,g' doc/sh-utils.texi man/logname.1 man/users.1 man/who.1
perl -pi -e 's,/etc/wtmp,/var/run/wtmp,g' doc/sh-utils.texi man/logname.1 man/users.1 man/who.1
rm -f doc/sh-utils.info

%build
rm -rf build-$RPM_ARCH
mkdir -p build-$RPM_ARCH ; cd build-$RPM_ARCH
CFLAGS="$RPM_OPT_FLAGS" ../configure --prefix=/usr --disable-largefile
make
make info

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{bin,usr/sbin}

make install prefix=$RPM_BUILD_ROOT/usr -C build-$RPM_ARCH

# some files are shell scripts... strip will fail on those
strip $RPM_BUILD_ROOT/usr/bin/* || :

for i in basename date echo false nice pwd sleep stty true uname ; do
    install -m 755 -s $RPM_BUILD_ROOT/usr/bin/$i $RPM_BUILD_ROOT/bin/$i
    rm -f $RPM_BUILD_ROOT/usr/bin/$i
done

install -m 755 $RPM_BUILD_ROOT/usr/bin/chroot $RPM_BUILD_ROOT/usr/sbin
rm -f $RPM_BUILD_ROOT/usr/bin/chroot
rm -f $RPM_BUILD_ROOT/usr/bin/{hostname,uptime}
rm -f $RPM_BUILD_ROOT/usr/man/man1/{hostname,uptime,su}.1

rm -f $RPM_BUILD_ROOT/usr/bin/[
ln -sf test $RPM_BUILD_ROOT/usr/bin/[

gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/*
gzip -9nf $RPM_BUILD_ROOT/usr/info/sh-utils.info

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info /usr/info/sh-utils.info.gz /usr/info/dir

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete /usr/info/sh-utils.info.gz /usr/info/dir
fi

%files
%defattr(-,root,root)
%doc NEWS README
/bin/*
/usr/sbin/chroot
/usr/bin/*
/usr/man/man1/*
/usr/info/sh-utils.info.gz

%changelog
* Wed Jul 12 2000 Solar Designer <solar@false.com>
- Imported this spec from RH, removed su and the PAM patches (as we're
using SimplePAMApps instead).

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description

* Wed Jan  5 2000 Jeff Johnson <jbj@redhat.com>
- add cest timezone (#8162).

* Thu Nov 18 1999 Michael K. Johnson <johnsonm@redhat.com>
- export DISPLAY as part of "su -" so that pam_xauth works.
  (really ought to be exported anyways...)

* Tue Aug 17 1999 Cristian Gafton <gafton@redhat.com>
- update to sh-utils 2.0 and port meaningfull patches (why the heck they keep
  ignoring the PAM patches?!)  (Because our PAM patches, by necessity,
  remove RMS's rant about the wheel group and how evil he thinks it
  is...  So we never expect the PAM patches to be accepted.  -mkj)
- sick thing: they still refer to /etc/[uw]tmp
- fix bogus requirement for autoconf version 2.14.1, which is unreleased as
  of today...

* Thu Aug  5 1999 Jeff Johnson <jbj@redhat.com>
- comment out "timestmap test stinks" hack. WTFO?
- remove info page so that it is regenerated correctly.

* Wed Aug  4 1999 Jeff Johnson <jbj@redhat.com>
- docs should say /var/run/[uw]tmp not /etc/[uw]tmp (#4319).

* Wed Jul 28 1999 Cristian Gafton <gafton@redhat.com>
- fix date +yesterday/tomorrow (#3778)
- fix #2308, #3954

* Tue Apr 13 1999 Michael K. Johnson <johnsonm@redhat.com>
- su.pamd now calls pam_xauth

* Mon Apr 12 1999 Michael K. Johnson <johnsonm@redhat.com>
- merge pam patches
- wait until in child process to drop priviledges as we need
  euid != ruid during pam_open_session and pam_close_session

* Thu Apr 01 1999 Erik Troan <ewt@redhat.com>
- make sure standard in is a tty so we can't feed it from a pipe

* Wed Mar 31 1999 Erik Troan <ewt@redhat.com>
- don't trust stdin for su (bug 1274)

* Fri Mar 26 1999 Michael Maher <mike@redhat.com>
- added stty patch, fixed bug #997

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 16)

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Mon Jun  8 1998 Michal Jaegermann <michal@harddata.com>
- fixed reversed test for when to allocate in who.c and an incorrect
  use of xrealloc.

* Thu Apr 30 1998 Donnie Barnes <djb@redhat.com>
- moved /usr/bin/nice to /bin/nice

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sat Apr 11 1998 Cristian Gafton <gafton@redhat.com>
- manhattan rebuild

* Wed Oct 22 1997 Michael K. Johnson <johnsonm@redhat.com>
- added minor patch for glibc 2.1

* Wed Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- fixed the URLs in spec file
- cleaned up the spec file

* Thu Oct 02 1997 Michael K. Johnson <johnsonm@redhat.com>
- BuildRoot
- New pam standard.

* Sun Sep 14 1997 Erik Troan <ewt@redhat.com>
- uses install-info

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Fri Apr 18 1997 Michael K. Johnson <johnsonm@redhat.com>
- Fixed the sense of the user and root default paths.

* Mon Apr 14 1997 Erik Troan <ewt@redhat.com>
- Fixed getutent patch to define UTMP_READ_INCR
- Modified su.c to define default paths w/o regard to other header files or
  -D style definitions

* Wed Apr 02 1997 Erik Troan <ewt@redhat.com>
- Updated getutent patch for 1.16
- Added mktime patch for 64bit time_t

* Tue Mar 25 1997 Michael K. Johnson <johnsonm@redhat.com>
- DEFPATH handling moved from ...path.patch to _PATH_DEFPATH*

* Mon Mar 03 1997 Michael K. Johnson <johnsonm@redhat.com>
- Moved from pam.conf to pam.d
