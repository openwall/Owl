# $Id: Owl/packages/pwdb/Attic/pwdb.spec,v 1.5 2001/07/30 02:21:27 solar Exp $

Summary: The password database library.
Name: pwdb
Version: 0.61.1
Release: 2owl
Copyright: GPL or BSD
Group: System Environment/Base
Source: pwdb-%{version}.tar.gz
Patch0: pwdb-0.61-owl-fgets.diff
Patch1: pwdb-0.61-owl-clean.diff
Patch2: pwdb-0.61-owl-backup.diff
Patch3: pwdb-0.61-owl-sprintf.diff
Patch4: pwdb-0.61-owl-sp_flag.diff
Patch5: pwdb-0.61-koni-owl-memory-leaks.diff
Buildroot: /var/rpm-buildroot/%{name}-%{version}

%description
The pwdb package contains libpwdb, the password database library.
libpwdb is a library which implements a generic user information
database.  libpwdb was specifically designed to work with Linux-PAM
(Pluggable Authentication Modules).  libpwdb allows configurable
access to and management of security tools like /etc/passwd,
/etc/shadow and network authentication systems including NIS and
Radius.

# Use optflags_lib for this package if defined.
%{expand:%%define optflags %{?optflags_lib:%optflags_lib}%{!?optflags_lib:%optflags}}

%prep
%setup -q -c
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
rm default.defs
ln -s defs/redhat.defs default.defs
# checking out of the CVS sometimes preserves the setgid bit on
# directories...
chmod -R g-s .

%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{etc,lib,usr/include/pwdb}

make	INCLUDED=$RPM_BUILD_ROOT/usr/include/pwdb \
	LIBDIR=$RPM_BUILD_ROOT/lib \
	LDCONFIG=":" \
	install

install -m 644 conf/pwdb.conf $RPM_BUILD_ROOT/etc/pwdb.conf

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc Copyright doc/pwdb.txt doc/html
%config /etc/pwdb.conf
/usr/include/pwdb
/lib/libpwdb.a
/lib/libpwdb.so
/lib/libpwdb.so.%{version}

%changelog
* Mon Jul 30 2001 Solar Designer <solar@owl.openwall.com>
- optflags_lib support.

* Mon Jun 18 2001 Solar Designer <solar@owl.openwall.com>
- Updated to 0.61.1, which adds some header files.

* Sun Apr 08 2001 Solar Designer <solar@owl.openwall.com>
- Included a patch for memory leaks reported to libpwdb developers by
Koni <mhw6@cornell.edu>.

* Sun Sep 03 2000 Solar Designer <solar@owl.openwall.com>
- Initialize sp_flag (a reserved field) in _pwdb_shadow_replace().

* Mon Aug 07 2000 Solar Designer <solar@owl.openwall.com>
- Imported from RH, added four reliability/security patches; a lot of
problems still remain in the code, we should stop using pam_pwdb soon.

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix setting the password for passwordless accounts. Patch from Thomas
  Sailer

* Mon Jan 31 2000 Cristian Gafton <gafton@redhat.com>
- rebuild to fix dependencies
