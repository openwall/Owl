# $Id: Owl/packages/sh-utils/Attic/sh-utils.spec,v 1.12 2004/11/23 22:40:49 mci Exp $

# The texinfo documentation for fileutils, sh-utils, and textutils is
# currently provided by fileutils.
%define BUILD_INFO 0

Summary: A set of GNU utilities commonly used in shell scripts.
Name: sh-utils
Version: 2.0
Release: owl4
License: GPL
Group: System Environment/Shells
Source: ftp://ftp.gnu.org/gnu/sh-utils/sh-utils-%version.tar.gz
Patch0: sh-utils-2.0-owl-no-su-hostname.diff
Patch1: sh-utils-2.0-owl-false.diff
Patch2: sh-utils-2.0-rh-cest.diff
Patch3: sh-utils-2.0-rh-utmp.diff
%if %BUILD_INFO
PreReq: /sbin/install-info
%endif
BuildRequires: sed >= 4.0.9
BuildRoot: /override/%name-%version

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
%patch3 -p1

# The docs should say /var/run/[uw]tmp not /etc/[uw]tmp
sed -i 's,/etc/utmp,/var/run/utmp,g' \
	doc/sh-utils.texi man/users.1 man/who.1
sed -i 's,/etc/wtmp,/var/run/wtmp,g' \
	doc/sh-utils.texi man/users.1 man/who.1
rm doc/sh-utils.info

%{expand:%%define optflags %optflags -Wall -Dlint}

%build
%configure --enable-largefile
make

%install
rm -rf %buildroot
%makeinstall

cd %buildroot
mkdir bin
for i in basename date echo false nice pwd sleep stty true uname env; do
	mv .%_bindir/$i bin/
done

ln -s ../../bin/env .%_bindir/
test -r .%_bindir/env

ln -s test .%_bindir/[

mkdir -p .%_sbindir
mv .%_bindir/chroot .%_sbindir/
rm .%_bindir/uptime
rm .%_mandir/man1/{hostname,su}.1

# Remove unpackaged files
rm %buildroot%_infodir/dir
%if !%BUILD_INFO
rm %buildroot%_infodir/sh-utils.info*
%endif

%if %BUILD_INFO
%post
/sbin/install-info %_infodir/sh-utils.info.gz %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/sh-utils.info.gz %_infodir/dir
fi
%else
%pre
/sbin/install-info --quiet --delete \
	%_infodir/sh-utils.info.gz %_infodir/dir
%endif

%files
%defattr(-,root,root)
%doc COPYING NEWS README THANKS TODO
/bin/*
%_bindir/*
%_sbindir/chroot
%_mandir/man*/*
%if %BUILD_INFO
%_infodir/sh-utils.info*
%endif
%_datadir/locale/*/*/*

%changelog
* Tue Jul 20 2004 Michail Litvak <mci@owl.openwall.com> 2.0-owl4 
- Use sed -i instead of perl.

* Mon Aug 05 2002 Solar Designer <solar@owl.openwall.com> 2.0-owl3
- No longer provide texinfo documentation, it is now a part of fileutils.
- Do package locale data.
- Use _*dir, configure, and makeinstall RPM macros.
- Enabled large file support.

* Wed Feb 06 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Wed Jul 26 2000 Solar Designer <solar@owl.openwall.com>
- Replaced true and false with the assembly version.

* Wed Jul 12 2000 Solar Designer <solar@owl.openwall.com>
- Imported this spec from RH, removed su and the PAM patches (as we're
using SimplePAMApps instead).
