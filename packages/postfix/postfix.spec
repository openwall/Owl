# $Id: Owl/packages/postfix/postfix.spec,v 1.1 2000/11/21 19:49:45 solar Exp $

Summary: Postfix mail system
Name: postfix
%define original_date 19991231
%define original_pl pl10
%define original_version %{original_date}-%{original_pl}
%define package_version %{original_date}_%{original_pl}
Version: %{package_version}
Release: 1owl
Copyright: IBM Public License
Group: System Environment/Daemons
Source0: ftp://ftp.sunet.se/pub/unix/mail/postfix/official/%{name}-%{original_version}.tar.gz
Source1: aliases
Source2: postfix.init
Patch0: postfix-19991231-pl10-owl-INSTALL.diff
Patch1: postfix-19991231-pl10-owl-config.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}
Provides: MTA smtpd smtpdaemon
Conflicts: sendmail

%description
Postfix is Wietse Venema's attempt to provide an alternative to the
widely-used Sendmail program.  Postfix attempts to be fast, easy to
administer, and hopefully secure, while at the same time being sendmail
compatible enough to not upset your users.

%prep
%setup -q -n %{name}-%{original_version}
%patch0 -p1
%patch1 -p1

%build
make OPT="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT

yes '' | {
	function chowngrp()
	{
		local list mode

		list=$1
		shift
		mode=$1
		while shift; do
			echo "$1 $mode" |
			sed -n "s,^$RPM_BUILD_ROOT,,p" >> $list
		done
	}

	function chown()
	{
		chowngrp filelist.user $*
	}

	function chgrp()
	{
		chowngrp filelist.group $*
	}

	rm -f filelist.* flag.*
	. INSTALL.sh
	touch flag.$?
}

test -f flag.0

pushd $RPM_BUILD_ROOT

rm etc/postfix/install.cf

install -m 644 $RPM_SOURCE_DIR/aliases etc/postfix/
ln -s /etc/postfix/aliases{,.db} etc/

mkdir -p etc/rc.d/init.d
install -m 700 $RPM_SOURCE_DIR/postfix.init etc/rc.d/init.d/postfix

mkdir -p usr/lib
ln -s /usr/sbin/sendmail usr/lib/sendmail

chmod go-r usr/sbin/postdrop

strip usr/{bin,sbin,libexec/postfix}/* || :
gzip -9nf usr/man/man*/*

popd

cat > filelist << EOF
%defattr (-,root,root)
%doc 0README BEWARE COMPATIBILITY DEBUG_README HISTORY LICENSE RELEASE_NOTES
%doc RESTRICTION_CLASS TODO UUCP_README
%doc examples html
EOF

cat filelist.{user,group} | sed 's/ .*$//' | sort -u > filelist.plain

while read filename; do
	test -e ${RPM_BUILD_ROOT}${filename}
	user="`sed -n "s,^$filename \(.*\)\$,\1,p" < filelist.user`"
	test -n "$user" || user=root
	group="`sed -n "s,^$filename \(.*\)\$,\1,p" < filelist.group`"
	test -n "$group" || group=root
	if [ -d ${RPM_BUILD_ROOT}${filename} ]; then
		echo "%dir %attr(-,$user,$group) $filename"
	else
		echo "%attr(-,$user,$group) $filename"
	fi
done < filelist.plain >> filelist

find $RPM_BUILD_ROOT -type d |
	sed "s,^$RPM_BUILD_ROOT,," |
	sort |
	comm -23 - filelist.plain |
	grep '/postfix$' |
	sed 's,^,%dir ,' >> filelist

find $RPM_BUILD_ROOT ! -type d |
	sed "s,^$RPM_BUILD_ROOT,," |
	sort |
	comm -23 - filelist.plain |
	sed -e 's,^/etc,%config &,' -e 's,/usr/man/.*$,&*,' >> filelist

%clean
rm -rf $RPM_BUILD_ROOT

%pre
grep ^postdrop: /etc/group &> /dev/null || groupadd -g 161 postdrop
grep ^postdrop: /etc/passwd &> /dev/null ||
	useradd -g postdrop -u 161 -d / -s /bin/false -M postdrop
grep ^postfix: /etc/group &> /dev/null || groupadd -g 182 postfix
grep ^postfix: /etc/passwd &> /dev/null ||
	useradd -g postfix -u 182 -d / -s /bin/false -M postfix
grep ^postman: /etc/group &> /dev/null || groupadd -g 183 postman
grep ^postman: /etc/passwd &> /dev/null ||
	useradd -g postman -u 183 -d / -s /bin/false -M postman

%post
/usr/sbin/postalias /etc/postfix/aliases
/usr/sbin/postfix check
/sbin/chkconfig --add postfix

%preun
/usr/sbin/postfix stop
/sbin/chkconfig --del postfix

%postun
rm -f /etc/postfix/aliases.db
rm -f /var/spool/postfix/pid/*
find /var/spool/postfix \( -type p -o -type s \) -delete
rmdir /var/spool/postfix/{*,}

%files -f filelist

%changelog
* Tue Nov 21 2000 Solar Designer <solar@owl.openwall.com>
- Wrote this spec file.
- Took postfix.init from Simon J Mudd's package with minor changes.
- SMTP server is now disabled by default.
