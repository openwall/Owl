# $Id: Owl/packages/cvs/cvs.spec,v 1.1 2003/04/27 12:24:30 solar Exp $

Summary: A version control system.
Name: cvs
Version: 1.11.5
Release: owl0.1
License: GPL
Group: Development/Tools
URL: http://www.cvshome.org
Source: ftp://ftp.cvshome.com/pub/%{name}-%{version}/%{name}-%{version}.tar.bz2
Patch0: cvs-1.11.5-owl-zlib.diff
Patch1: cvs-1.11.5-owl-no-checkin-update-prog.diff
Patch2: cvs-1.11.5-alt-owl-tmp.diff
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

%build
%configure --without-gssapi

make LDFLAGS=-s
gzip -9nf doc/*.ps

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

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
%{_datadir}/%{name}

%changelog
* Mon Mar 24 2003 Simon B <simonb@owl.openwall.com> 1.11.5-owl0.1
- Pulled in mktemp fixes from ALT Linux
- Disable {Checkin,Update}-prog
- General tidying up based on suggestions from Solar Designer

* Fri Mar 14 2003 Simon B <simonb@owl.openwall.com>
- initial Owl spec file
- compile CVS dynamically against zlib instead of using the version
included with the CVS source.
