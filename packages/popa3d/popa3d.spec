# $Id: Owl/packages/popa3d/popa3d.spec,v 1.30 2003/03/02 03:45:32 solar Exp $

Summary: Post Office Protocol (POP3) server.
Name: popa3d
Version: 0.6.1
Release: owl1
License: relaxed BSD and (L)GPL-compatible
Group: System Environment/Daemons
Source0: ftp://ftp.openwall.com/pub/projects/popa3d/popa3d-%{version}.tar.gz
Source1: params.h
Source2: popa3d.pam
Source3: popa3d.init
Source4: popa3d.xinetd
PreReq: /sbin/chkconfig, grep, shadow-utils
Requires: /var/empty, tcb, pam_userpass, xinetd
BuildRoot: /override/%{name}-%{version}

%description
popa3d is a tiny Post Office Protocol version 3 (POP3) server with
security as its primary design goal.

%prep
%setup -q
cp $RPM_SOURCE_DIR/params.h params.h

%build
make CFLAGS="-c -Wall $RPM_OPT_FLAGS -DHAVE_PROGNAME" LIBS="-lpam"

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT SBINDIR=%_sbindir MANDIR=%_mandir

mkdir -p $RPM_BUILD_ROOT/etc/{pam.d,rc.d/init.d,xinetd.d}
install -m 600 $RPM_SOURCE_DIR/popa3d.pam \
	$RPM_BUILD_ROOT/etc/pam.d/popa3d
install -m 700 $RPM_SOURCE_DIR/popa3d.init \
	$RPM_BUILD_ROOT/etc/rc.d/init.d/popa3d
install -m 600 $RPM_SOURCE_DIR/popa3d.xinetd \
	$RPM_BUILD_ROOT/etc/xinetd.d/popa3d

%clean
rm -rf $RPM_BUILD_ROOT

%pre
grep -q ^popa3d: /etc/group || groupadd -g 184 popa3d
grep -q ^popa3d: /etc/passwd ||
	useradd -g popa3d -u 184 -d / -s /bin/false -M popa3d
rm -f /var/run/popa3d.restart
if [ $1 -ge 2 ]; then
	/etc/rc.d/init.d/popa3d status && touch /var/run/popa3d.restart || :
	/etc/rc.d/init.d/popa3d stop || :
fi

%post
test -f /var/run/popa3d.restart && /etc/rc.d/init.d/popa3d start || :
rm -f /var/run/popa3d.restart

%preun
if [ $1 -eq 0 ]; then
	/etc/rc.d/init.d/popa3d stop || :
	/sbin/chkconfig --del popa3d
fi

%files
%defattr(-,root,root)
%_sbindir/popa3d
%_mandir/man8/popa3d.8*
%config(noreplace) /etc/pam.d/popa3d
%config /etc/rc.d/init.d/popa3d
%config /etc/xinetd.d/popa3d
%doc DESIGN LICENSE

%changelog
* Sun Mar 02 2003 Solar Designer <solar@owl.openwall.com> 0.6.1-owl1
- Ensure DB_STALE is set if mailbox_get() fails for that possible reason.
- Added version.c and the -V option to print out version information.

* Thu Feb 20 2003 Solar Designer <solar@owl.openwall.com> 0.6-owl1
- pop_reply_multiline() will now return different POP_CRASH_* codes on
error (both network- and server-related errors are possible there).
- Let it be 0.6 stable release.

* Sun Jan 26 2003 Solar Designer <solar@owl.openwall.com>
- Corrected the message size reporting bug introduced with 0.4.9.3 and
now reported on popa3d-users by Nuno Teixeira.

* Sun Sep 08 2002 Solar Designer <solar@owl.openwall.com>
- Avoid non-ANSI/ISO C constructs.
- Deal with file sizes beyond what will fit in unsigned long reasonably.

* Fri Aug 02 2002 Solar Designer <solar@owl.openwall.com>
- Use unsigned integer types where integer overflows are possible and
post-checked for; ISO C 99 leaves the behavior on integer overflow for
signed integer types undefined.
- Use unsigned long for file and message sizes and file offsets.

* Sun Jun 30 2002 Solar Designer <solar@owl.openwall.com>
- Mention "POP3" in ".SH NAME" in the man page such that "apropos POP3"
will catch it, as suggested by Phil Pennock.

* Sat Jun 22 2002 Solar Designer <solar@owl.openwall.com>
- Style change with plural form of abbreviations (ID's -> IDs) in the
documentation and source code comments.

* Mon May 27 2002 Solar Designer <solar@owl.openwall.com>
- Workaround a bug in certain versions of Microsoft Outlook Express
(reported) where the client would abort on body-less messages which are
lacking a blank line after the headers (valid per RFC 822, 2822).

* Sat May 25 2002 Solar Designer <solar@owl.openwall.com>
- Relaxed the overflow check with strtol() to what really is needed
to solve the interoperability problem reported by Yury Trembach on
fido7.ru.unix.

* Tue Apr 02 2002 Solar Designer <solar@owl.openwall.com>
- Let the local delivery agent help generate unique IDs by setting the
X-Delivery-ID: header.

* Fri Mar 22 2002 Solar Designer <solar@owl.openwall.com>
- Re-worked all of the UIDL calculation, adding support for multi-line
headers and re-considering which headers to use.

* Thu Feb 07 2002 Michail Litvak <mci@owl.openwall.com>
- Enforce our new spec file conventions.

* Fri Nov 16 2001 Solar Designer <solar@owl.openwall.com>
- Use pam_tcb.

* Sun Oct 28 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 0.5 which adds a popa3d(8) man page.

* Tue Sep 11 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 0.4.9.4 (fixed two bugs introduced with 0.4.9.2 and 0.4.9.3).

* Sun Sep 09 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 0.4.9.3.
- The same popa3d binary may now be run as a standalone server as well as
via xinetd, an /etc/xinetd.d file is provided.

* Sun Sep 02 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 0.4.9.2.

* Wed Jun 20 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 0.4.9.1 (finally replaced the GNU MD5 routines to relax
the license for the entire package, solve certain portability issues,
and reduce code size).

* Mon May 28 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 0.4.9.

* Thu Dec 07 2000 Solar Designer <solar@owl.openwall.com>
- Updated popa3d.init to use --expect-user.

* Wed Dec 06 2000 Solar Designer <solar@owl.openwall.com>
- 0.4.4 with pam_userpass support.
- Wrote this spec file, popa3d.pam, and popa3d.init.
