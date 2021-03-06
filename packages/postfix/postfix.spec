# $Owl: Owl/packages/postfix/postfix.spec,v 1.59 2016/08/23 15:16:02 solar Exp $

Summary: Postfix mail system.
Name: postfix
Version: 2.4.15
Release: owl5
Epoch: 1
License: IBM Public License
Group: System Environment/Daemons
URL: http://www.postfix.org/
# ftp://ftp.porcupine.org/mirrors/postfix-release/official/%name-%version.tar.gz
Source0: %name-%version.tar.xz
Source1: aliases
Source2: main.cf
Source3: postfix.init
Source4: postfix.control
Source5: postfix-master-chrootify.awk
Source6: postfix-lorder.sh
Source7: postfix-oclosure.sh
Source8: postqueue.control
Source9: README.Owl
Patch0: postfix-2.4.14-owl-dotforward-size-check.diff
Patch1: postfix-2.4.6-mjt-var_command_maxtime.diff
Patch2: postfix-2.4.6-alt-script.diff
Patch3: postfix-2.4.6-owl-update-chroot.diff
Patch4: postfix-2.4.6-alt-install.diff
Patch5: postfix-2.4.6-alt-post-install.diff
Patch6: postfix-2.4.6-alt-owl-filelist.diff
Patch7: postfix-2.4.6-alt-owl-config.diff
Patch8: postfix-2.4.6-alt-owl-local_minimum_uid.diff
Patch9: postfix-2.4.6-alt-mailbox_unpriv_delivery.diff
Patch10: postfix-2.4.6-alt-owl-shared.diff
Patch11: postfix-2.4.6-alt-main.cf.params.diff
Patch12: postfix-2.4.6-alt-var_virt_maps_legacy.diff
Patch13: postfix-2.4.15-alt-warnings.diff
Patch14: postfix-2.4.6-alt-postconf-E.diff
Patch15: postfix-2.4.6-alt-owl-defaults.diff
Patch16: postfix-2.4.6-alt-owl-doc.diff
Patch17: postfix-2.4.8-owl-safe_open.diff
Patch18: postfix-2.4.8-owl-postalias-no-hostname.diff
Patch19: postfix-2.4.15-owl-version.diff
Patch20: postfix-2.4.15-owl-linux-3.diff
Requires(post,preun): chkconfig, grep, shadow-utils
Requires(post,postun): /sbin/ldconfig
Requires(post): diffutils
Requires: owl-control >= 0.4, owl-control < 2.0
Requires: owl-startup
BuildRequires: db4-devel >= 4.2, pcre-devel, tinycdb-devel, sed >= 4.1.1
Conflicts: sendmail, qmail
Provides: MTA, smtpd, smtpdaemon
Obsoletes: sendmail-cf, sendmail-doc
BuildRoot: /override/%name-%version

# Configuration definitions below are here for both customization
# and to simplify building list of files for a package.

%define queue_directory /var/spool/postfix
%define config_directory /etc/postfix

%define daemon_directory %_libexecdir/postfix
%define program_directory %daemon_directory
%define command_directory %_sbindir

%define newaliases_path %_bindir/newaliases
%define mailq_path %_bindir/mailq
%define sendmail_path %_sbindir/sendmail

%define docdir %_docdir/%name-%version
%define manpage_directory %_mandir
%define html_directory %docdir/html
%define readme_directory %config_directory/README_FILES

%define restart_flag /var/run/%name.restart
%define libpostfix lib%name-%version.so
%define libpostfix_dict lib%{name}_dict-%version.so

%description
Postfix is Wietse Venema's attempt to provide an alternative to the
widely-used Sendmail program.  Postfix attempts to be fast, easy to
administer, and hopefully secure, while at the same time being sendmail
compatible enough to not upset your users.

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
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1

install -pm644 %_sourcedir/README.Owl README_FILES/

# Add objs and objs-print makefile targets.
sed -i 's/^update /&objs /' Makefile.in
sed -i 's/^# do not edit below this line/objs: $(OBJS)\n\nobjs-print: objs\n\tls $(OBJS)\n\n&/' \
	src/*/Makefile.in

# Change services to run chrooted.
awk -f %_sourcedir/postfix-master-chrootify.awk <conf/master.cf >conf/master.cf.new
mv conf/master.cf.new conf/master.cf

# Comment out smtp and smtpd.
sed -i 's,^\(smtp[[:space:]]\+inet[[:space:]]\+.*[[:space:]]\+smtpd[[:space:]]*\)$,#\1,' \
	conf/master.cf

# Remove license, makedefs.out, html documentation, man pages,
# readme files and sample files from the master list.
sed -i '/\(LICENSE\|makedefs\.out\|\(html\|manpage\|readme\|sample\)_directory\)/ d' \
	conf/postfix-files
rm conf/LICENSE

# Adjust arch-dependent paths.
sed -i 's/@LIB@/%_lib/' conf/postfix-{files,script}

# Fix build with upcoming util-linux-ng.
sed -i 's/col -bx |/LANG=en_US &/' proto/Makefile.in

bzip2 -9fk HISTORY

%build
export MAKEFLAGS="$MAKEFLAGS DEF_MAIL_VERSION=%version"
OPT="%optflags -Wall -Wno-comment -Wno-missing-braces"
CCARGS="\
 -DDEF_COMMAND_DIR=\\\"%command_directory\\\" \
 -DDEF_CONFIG_DIR=\\\"%config_directory\\\" \
 -DDEF_DAEMON_DIR=\\\"%daemon_directory\\\" \
 -DDEF_HTML_DIR=\\\"%html_directory\\\" \
 -DDEF_MAILQ_PATH=\\\"%mailq_path\\\" \
 -DDEF_MANPAGE_DIR=\\\"%manpage_directory\\\" \
 -DDEF_NEWALIAS_PATH=\\\"%newaliases_path\\\" \
 -DDEF_PROGRAM_DIR=\\\"%program_directory\\\" \
 -DDEF_QUEUE_DIR=\\\"%queue_directory\\\" \
 -DDEF_README_DIR=\\\"%readme_directory\\\" \
 -DDEF_SAMPLE_DIR=\\\"%readme_directory\\\" \
 -DDEF_SENDMAIL_PATH=\\\"%sendmail_path\\\" \
"
DICT_LIBS="-ldb -lcdb `pcre-config --libs`"
DICT_ARGS="-DHAS_CDB -DHAS_PCRE `pcre-config --cflags`"
SYSLIBS="-lnsl -lresolv"

pushd src

# 0. Prepare.
%__make	-j1 -C .. tidy makefiles \
	SYSLIBS="$SYSLIBS" \
	AUXLIBS= \
	CCARGS="$CCARGS $DICT_ARGS -UUSE_TLS" \
	OPT="$OPT" \
	DEBUG= \
	NO_IPV6=1

# 1. build all static libs objects with -fPIC.
%__make -C .. update \
	DEBUG='-fPIC' PROG= \
	DIRS='src/util src/global src/dns src/tls src/xsasl src/milter src/master'

# 2. separate libs objects into dict-dependent and others.
for a in */*.a; do
	ar t "$a" |
		sed -n "s,.*,${a%%/*}/&,p"
done | sort -u >postfix_all_obj.list
sh %_sourcedir/postfix-lorder.sh `cat postfix_all_obj.list` |
	sort -u |
	sort -k2,2 >postfix_lorder.list
printf '%%s\n%%s\n%%s\n' util/dict_{cdb,db,pcre}.o |
	sort -u |
	sh %_sourcedir/postfix-oclosure.sh postfix_lorder.list >postfix_dict_obj.list
join -v1 postfix_all_obj.list postfix_dict_obj.list >postfix_common_obj.list

# 3. build %libpostfix shared library.
gcc -shared -o ../lib/%libpostfix \
	-Wl,-O1 -Wl,-soname,%libpostfix \
	`cat postfix_common_obj.list` \
	$SYSLIBS
ln -s %libpostfix ../lib/libpostfix.so

# 4. build %libpostfix_dict shared library.
gcc -shared -o ../lib/%libpostfix_dict \
	-Wl,-O1 -Wl,-soname,%libpostfix_dict \
	`cat postfix_dict_obj.list` \
	../lib/libpostfix.so $DICT_LIBS
ln -s %libpostfix_dict ../lib/libpostfix_dict.so

# 5. build applications objects.
%__make -C .. objs

# 6. build dict-dependent applications with %libpostfix and %libpostfix_dict.
dict_build_dirs=
for d in *; do
	[ -f "$d/Makefile" ] || continue
	sh %_sourcedir/postfix-lorder.sh `cat postfix_dict_obj.list` \
	             `MAKEFLAGS= %__make -C "$d" -s objs-print |sed "s,^,$d/,"` |
		sort -u |
		sort -k2,2 |
		join -1 1 -2 2 -o 2.1 postfix_dict_obj.list - |
		sort -u |join -v1 - postfix_dict_obj.list |
		fgrep -qs "$d"/ || continue
	dict_build_dirs="$dict_build_dirs src/$d"
done
%__make -C .. \
	LIBS='../../lib/libpostfix_dict.so ../../lib/libpostfix.so' \
	DIRS="$dict_build_dirs" \
	SYSLIBS= \
	AUXLIBS= \
	#

# 7. build other applications with %libpostfix only.
%__make -C .. \
	LIBS=../../lib/libpostfix.so \
	SYSLIBS= \
	AUXLIBS= \
	#

popd # src

for d in proto man html; do
	%__make -C $d -f Makefile.in clobber README=
done
%__make -j1 manpages README=

# The alias file is clobbered during build, install it now.
install -pm644 %_sourcedir/aliases conf/

mkdir -p libexec/postqueuedir
mv bin/postqueue libexec/postqueuedir/

%install
rm -rf %buildroot
mkdir -p %buildroot{%_libdir,%_mandir,%daemon_directory/postqueuedir}

install -p -m755 lib/%libpostfix lib/%libpostfix_dict %buildroot%_libdir/

echo '%%defattr (-,root,root)' >postfix.files
# Postfix's postfix-install script accept various parameters both in
# command line and as environment variables.  Better to reset environment
# here, so no locally-set variable will give any surprise.
env -i "LD_LIBRARY_PATH=%buildroot%_libdir" \
	sh postfix-install -non-interactive \
		install_root=%buildroot \
		tempdir=%_tmppath

# Finish postqueue install
chmod 700 %buildroot%daemon_directory/postqueuedir
ln -s ../..%daemon_directory/postqueuedir/postqueue %buildroot%command_directory/

# Install minimal main.cf
mv %buildroot%config_directory/main.cf{,.dist}
install -pm644 %_sourcedir/main.cf %buildroot%config_directory/

install -pD -m700 %_sourcedir/postfix.init \
	%buildroot/etc/rc.d/init.d/postfix
install -pD -m700 %_sourcedir/postfix.control \
	%buildroot/etc/control.d/facilities/postfix
install -pD -m700 %_sourcedir/postqueue.control \
	%buildroot/etc/control.d/facilities/postqueue

cp -a man/man{1,5,8} %buildroot%manpage_directory/

install -p -m755 auxiliary/qshape/qshape.pl %buildroot%_bindir/qshape
install -p -m755 auxiliary/rmail/rmail %buildroot%_bindir/

ln -s ../sbin/sendmail %buildroot%_libdir/sendmail

rmdir %buildroot%config_directory/README_FILES
ln -s ../..%docdir/{LICENSE,README_FILES} %buildroot%config_directory/

ln -s postfix/aliases %buildroot/etc/
ln -s postfix/aliases.db %buildroot/etc/

# Shorten the symlinks
rm %buildroot%_bindir/{mailq,newaliases}
ln -s ../sbin/sendmail %buildroot%_bindir/mailq
ln -s ../sbin/sendmail %buildroot%_bindir/newaliases

# Chrooted environment
touch %buildroot%queue_directory/etc/{hosts,localtime,services,{host,nsswitch,resolv}.conf}
touch %buildroot%queue_directory/dev/log
mkdir %buildroot/etc/syslog.d
ln -s %queue_directory/dev/log %buildroot/etc/syslog.d/postfix

%pre
grep -q ^postdrop: /etc/group || groupadd -g 161 postdrop
grep -q ^postdrop: /etc/passwd ||
	useradd -g postdrop -u 161 -d / -s /bin/false -M postdrop
grep -q ^postfix: /etc/group || groupadd -g 182 postfix
grep -q ^postfix: /etc/passwd ||
	useradd -g postfix -u 182 -d / -s /bin/false -M postfix
grep -q ^postman: /etc/group || groupadd -g 183 postman
grep -q ^postman: /etc/passwd ||
	useradd -g postman -u 183 -d / -s /bin/false -M postman
rm -f %restart_flag
if [ $1 -ge 2 ]; then
	if %command_directory/postfix stop ||
	   /sbin/start-stop-daemon -q --stop --exec %daemon_directory/master \
		--pidfile %queue_directory/pid/master.pid --user root; then
		touch %restart_flag || :
	fi
	mkdir -p -m700 %daemon_directory/postqueuedir
	/usr/sbin/control-dump postfix postqueue
fi

%post
/sbin/ldconfig
%config_directory/post-install \
	config_directory=%config_directory \
	daemon_directory=%daemon_directory \
	upgrade-package
%command_directory/postalias %config_directory/aliases
%command_directory/postfix check
if [ $1 -ge 2 ]; then
	/usr/sbin/control-restore postfix postqueue
fi
/sbin/chkconfig --add postfix
[ -f %restart_flag ] && %command_directory/postfix start || :
rm -f %restart_flag
if [ "`/usr/sbin/control postfix`" = local ]; then
	echo -n "SMTP server not enabled by default, use "
	echo "\"control postfix server\" to enable"
fi

%preun
if [ $1 -eq 0 ]; then
	%command_directory/postfix stop || :
	/sbin/chkconfig --del postfix
	sleep 1
	%command_directory/postfix drain &> /dev/null || :
	rm -f %config_directory/aliases.db
	find %queue_directory \( -type p -o -type s \) -delete
	rm -f %queue_directory/{pid,etc,lib}/*
fi

%postun -p /sbin/ldconfig

%files -f postfix.files
%defattr (-,root,root)
%doc COMPATIBILITY HISTORY.bz2 LICENSE PORTING README_FILES RELEASE_NOTES
%doc examples html
%doc %config_directory/LICENSE
%doc %config_directory/README_FILES
%config %config_directory/main.cf.dist
%config /etc/rc.d/init.d/postfix
/etc/control.d/facilities/*
/etc/syslog.d/postfix
/etc/aliases
/etc/aliases.db
%_libdir/%libpostfix
%_libdir/%libpostfix_dict
%_libdir/sendmail
%attr(700,root,root) %verify(not mode,group) %dir %daemon_directory/postqueuedir
%daemon_directory/lmtp
%command_directory/postqueue
%_bindir/mailq
%_bindir/newaliases
%_bindir/qshape
%_bindir/rmail
%_mandir/man?/*
%attr(644,root,root) %verify(not md5 mtime size) %ghost %queue_directory/etc/*
%attr(666,root,root) %ghost %queue_directory/dev/log

%changelog
* Tue Aug 23 2016 Solar Designer <solar-at-owl.openwall.com> 1:2.4.15-owl5
- Dropped the empty comment line from /etc/postfix/main.cf.params so that the
file is in sorted order including the comment lines.

* Tue May 31 2016 Solar Designer <solar-at-owl.openwall.com> 1:2.4.15-owl4
- Added LC_COLLATE=C to a sort invocation in
postfix-2.4.6-alt-main.cf.params.diff, where previously only one of two lists
being comm'ed was sort'ed with explicit LC_COLLATE=C.

* Sun Jul 13 2014 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1:2.4.15-owl3
- Replaced the deprecated PreReq tag with Requires(post,preun).
- Regenerated the warnings patch since it was fuzzy.
- Added a missing dependency for diffutils.

* Sun Feb 12 2012 Vasiliy Kulikov <segoon-at-owl.openwall.com> 1:2.4.15-owl2
- Fixed build failure on Linux 3.x.

* Sat Dec 04 2010 Solar Designer <solar-at-owl.openwall.com> 1:2.4.15-owl1
- Updated to 2.4.15.

* Fri Nov 05 2010 Solar Designer <solar-at-owl.openwall.com> 1:2.4.14-owl2
- In postfix-script, use $INFO instead of $WARN for the chroot jail update
messages, which do not indicate any problem.  Suggested by Vasiliy Kulikov.

* Wed Jul 28 2010 Solar Designer <solar-at-owl.openwall.com> 1:2.4.14-owl1
- Updated to 2.4.14.
- Replaced the .forward sparse file check with a size check.

* Tue Sep 29 2009 Dmitry V. Levin <ldv-at-owl.openwall.com> 1:2.4.13-owl2
- Packaged /etc/syslog.d/postfix symlink to configure syslogd to listen
on %queue_directory/dev/log socket.

* Mon Aug 31 2009 Solar Designer <solar-at-owl.openwall.com> 1:2.4.13-owl1
- Updated to 2.4.13.

* Sat Jul 11 2009 Solar Designer <solar-at-owl.openwall.com> 1:2.4.11-owl1
- Updated to 2.4.11.

* Sat May 09 2009 Solar Designer <solar-at-owl.openwall.com> 1:2.4.8-owl2
- Re-introduced the postalias hack originally implemented with
postfix-19991231-pl13-owl-postalias-no-hostname.diff not to leak the
install host's name.

* Sun Aug 10 2008 Dmitry V. Levin <ldv-at-owl.openwall.com> 1:2.4.8-owl1
- Updated to 2.4.8.

* Sun Dec 23 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 1:2.4.6-owl2
- Fixed build of documentation.

* Sun Dec 16 2007 Dmitry V. Levin <ldv-at-owl.openwall.com> 1:2.4.6-owl1
- Updated to 2.4.6.
- Dropped aliases for pseudo-user accounts and some addresses
suggested by RFC 2142 from default alias file.
- Changed several default parameters values:
biff = no
smtpd_data_restrictions = reject_unauth_pipelining
smtpd_etrn_restrictions = permit_mynetworks, reject
smtpd_helo_required = yes
- The original main.cf is now delivered as /usr/share/postfix/main.cf.dist,
rather than cluttering /etc/postfix/main.cf with comments.
- Packaged README.Owl file describing notable differences between
the Owl Postfix package and the upstream source.
- Added "status" mode to startup script.

* Sun Sep 03 2006 (GalaxyMaster) <galaxy-at-owl.openwall.com> 1:2.2.11-owl2
- Relaxed the build dependency on db4-devel.

* Fri Aug 04 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1:2.2.11-owl1
- Updated to 2.2.11.
- Changed postfix-install script to avoid adding default installation
parameters to main.cf and therethrough avoid potential upgrade problems.

* Fri Apr 07 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1:2.2.10-owl1
- Updated to 2.2.10.
- Rebuilt with libdb-4.3.so.

* Sat Mar 11 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1:2.2.9-owl1
- Updated to 2.2.9.

* Thu Jan 05 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 1:2.2.8-owl1
- Updated to 2.2.8.

* Sat Dec 24 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1:2.2.7-owl2
- Rebuilt with libdb-4.2.so.

* Tue Dec 13 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1:2.2.7-owl1
- Updated to 2.2.7.

* Sun Nov 13 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1:2.2.5-owl3
- Restricted queue views and runs.

* Mon Nov 07 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1:2.2.5-owl2
- Added CDB database type and PCRE lookup tables support.
- Changed default mailbox locking method to fcntl.
- Changed default virtual_minimum_uid value from 100 to 500.
- Imported patch from ALT which introduces new integer parameter
local_minimum_uid and restricts local user lookup functions
to users with uid >= local_minimum_uid (500 by default).
- Imported patch from ALT which introduces new boolean parameter
mailbox_unpriv_delivery which, if enabled (by default), instructs local(8)
to deliver as recipient when spool directory is not world-writable.

* Thu Aug 11 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1:2.2.5-owl1
- Updated to 2.2.5.
- Updated mantools/postlink patch from Debian.
- Added workaround in %%pre script to stop Postfix even if old
/usr/sbin/postfix program cannot stop the daemon during upgrade.
- Changed chroot jail update script to set world-readable permissions
on files it copies.

* Thu Jun 30 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 1:2.2.4-owl1
- Updated to 2.2.4.
- Reviewed Owl patches, removed obsolete ones.
- Imported shared build model and adopted a bunch of patches from ALT's
postfix-2.2.4-alt2 package, including following defaults changes:
alias_database = hash:/etc/postfix/aliases,
alias_maps = hash:/etc/postfix/aliases,
mynetworks_style = host.

* Sun Nov 07 2004 Michail Litvak <mci-at-owl.openwall.com> 19991231_pl13-owl9
- Corrected the placement of man pages for FHS 2.2 compatibility.

* Fri Nov 28 2003 Solar Designer <solar-at-owl.openwall.com> 19991231_pl13-owl8
- Continue on possible errors from the rmdir in %preun such that it is still
possible to uninstall; thanks to Maciek Pasternacki for reporting this.

* Fri Oct 24 2003 Solar Designer <solar-at-owl.openwall.com> 19991231_pl13-owl7
- Explain how to enable the SMTP server with control(8).

* Wed Oct 22 2003 Solar Designer <solar-at-owl.openwall.com> 19991231_pl13-owl6
- Hack: in postalias, don't set YP_MASTER_NAME as that would leak the
hostname when doing chrooted installs for other systems.

* Sun Nov 03 2002 Solar Designer <solar-at-owl.openwall.com> 19991231_pl13-owl5
- Dump/restore the owl-control setting for SMTP server on package upgrades.

* Sun Oct 13 2002 Solar Designer <solar-at-owl.openwall.com>
- Use fcntl locking, not flock.

* Tue Sep 03 2002 Solar Designer <solar-at-owl.openwall.com>
- Conflicts: qmail

* Sun Jul 07 2002 Solar Designer <solar-at-owl.openwall.com>
- Use grep -q in %pre.

* Thu Feb 07 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Wed Dec 26 2001 Solar Designer <solar-at-owl.openwall.com>
- Additional postfix-script fail-closeness.

* Sat Dec 22 2001 Solar Designer <solar-at-owl.openwall.com>
- Hardening of the Postfix queue file permissions and access methods,
in case someone compromises the postfix account.  The fixes are by
Wietse Venema and have been back-ported from the 20011217 snapshot.
Thanks to Michael Tokarev for his help in handling these issues.
- Updated to 19991231-pl13.

* Sun Mar 18 2001 Solar Designer <solar-at-owl.openwall.com>
- Fixed a copy/paste bug in the restart script.

* Sun Dec 24 2000 Solar Designer <solar-at-owl.openwall.com>
- Obsoletes: sendmail-cf, sendmail-doc

* Mon Dec 04 2000 Solar Designer <solar-at-owl.openwall.com>
- Ignore missing source files when updating the chroot jail (this may
happen during system installation).

* Fri Dec 01 2000 Solar Designer <solar-at-owl.openwall.com>
- Simplified postfix.init for use with owl-startup.
- Restart on package upgrades.

* Wed Nov 22 2000 Solar Designer <solar-at-owl.openwall.com>
- Restrict relaying to the host's own addresses only by default.
- Ignore sparse .forward files on filesystems which allow for this.
- /var/spool/postfix/pid/ is now only writable by root.
- Run whatever possible chroot'ed (many of the processes keep root
privileges in their real and/or saved IDs and pseudo-user postfix
is shared with non-chroot'ed processes, so this is breakable).
- Wrote postfix.control to enable/disable the SMTP server.

* Tue Nov 21 2000 Solar Designer <solar-at-owl.openwall.com>
- Wrote this spec file.
- Took postfix.init from Simon J Mudd's package with minor changes.
- SMTP server is now disabled by default.
