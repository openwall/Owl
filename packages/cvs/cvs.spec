# $Id: Owl/packages/cvs/cvs.spec,v 1.5 2003/04/29 01:39:17 solar Exp $

Summary: A version control system.
Name: cvs
Version: 1.11.5
Release: owl0.5
License: GPL
Group: Development/Tools
URL: http://www.cvshome.org
Source: ftp://ftp.cvshome.com/pub/%{name}-%{version}/%{name}-%{version}.tar.bz2
Patch0: cvs-1.11.5-owl-zlib.diff
Patch1: cvs-1.11.5-owl-no-checkin-update-prog.diff
Patch2: cvs-1.11.5-owl-tmp.diff
Patch3: cvs-1.11.5-owl-vitmp.diff
Patch4: cvs-1.11.5-owl-fixes.diff
PreReq: /sbin/install-info
Prefix: %{_prefix}
BuildRoot: /override/%{name}-%{version}

%description
Concurrent Versions System (CVS) is a version control system which can
record the history of your files (usually, but not always, source
code).  CVS only stores the differences between versions, instead of
every version of every file you've ever created.  CVS also keeps a log
of when and why changes occurred, and who made them.

CVS is very helpful for managing releases and controlling the
concurrent editing of source files among multiple authors.  Instead of
providing version control for a collection of files in a single
directory, CVS provides version control for a hierarchical collection
of directories consisting of revision controlled files.  These
directories and files can then be combined together to form a software
release.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%{expand:%%define optflags %optflags -Wall}

%build
export ac_cv_func_mkstemp=yes \
%configure \
	--without-krb4 --without-gssapi \
	--with-tmpdir=/tmp --with-editor=/bin/vitmp

make LDFLAGS=-s
gzip -9nf doc/*.ps

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

cd $RPM_BUILD_ROOT
find .%{_datadir}/cvs -type f -print0 | xargs -r0 chmod -x --
chmod 755 .%{_datadir}/cvs/contrib/rcs2log

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/cvs.info.gz /%{_infodir}/dir
/sbin/install-info %{_infodir}/cvsclient.info.gz /%{_infodir}/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/cvs.info.gz %{_infodir}/dir
	/sbin/install-info --delete %{_infodir}/cvsclient.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
%doc AUTHORS BUGS FAQ MINOR-BUGS NEWS PROJECTS TODO README
%doc doc/RCSFILES doc/*.ps.gz
%{_bindir}/*
%{_mandir}/*/*
%{_infodir}/*.info*
%{_datadir}/cvs

%changelog
* Tue Apr 29 2003 Solar Designer <solar@owl.openwall.com> 1.11.5-owl0.5
- Many more updates to the temporary file handling patch, making it twice
bigger.
- Force configure to use /tmp for the default temporary file directory,
and not pick and store $TMPDIR that was set at build time.
- Use vitmp with cvsbug, rcs-to-cvs, and cvs itself.
- Enable mkstemp explicitly, not rely on configure.
- Patched 47 gcc -Wall warnings (all of them), including some real bugs.
- chmod -x most scripts in contrib/ to prevent bogus dependencies on perl
and csh.

* Sun Apr 27 2003 Solar Designer <solar@owl.openwall.com> 1.11.5-owl0.2
- Re-worked much of the temporary file handling patch to make it actually
do at least some of what it was supposed to; also patched the fail-open
use in configure.

* Mon Mar 24 2003 Simon B <simonb@owl.openwall.com> 1.11.5-owl0.1
- Pulled in mktemp fixes from ALT Linux
- Disable {Checkin,Update}-prog
- General tidying up based on suggestions from Solar Designer

* Fri Mar 14 2003 Simon B <simonb@owl.openwall.com>
- initial Owl spec file
- compile CVS dynamically against zlib instead of using the version
included with the CVS source.
