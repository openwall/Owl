# $Owl: Owl/packages/pv/pv.spec,v 1.4 2011/10/11 19:07:41 segoon Exp $

Summary: A tool for monitoring the progress of data through a pipeline.
Name: pv
Version: 1.2.0
Release: owl2
License: Artistic 2.0
Group: Applications/System
URL: http://www.ivarch.com/programs/pv.shtml
Source: http://pipeviewer.googlecode.com/files/%name-%version.tar.bz2
# Signature: http://www.ivarch.com/programs/sources/%name-%version.tar.bz2.txt
BuildRequires: gettext
BuildRoot: /override/%name-%version

%description
PV ("Pipe Viewer") is a tool for monitoring the progress of data through a
pipeline.  It can be inserted into any normal pipeline between two processes
to give a visual indication of how quickly data is passing through, how long
it has taken, how near to completion it is, and an estimate of how long it
will be until completion.

%prep
%setup -q
# Not yet:
#mv README README.iso8859
#iconv -f ISO-8859-1 -t UTF-8 README.iso8859 > README
#mv doc/NEWS doc/NEWS.iso8859
#iconv -f ISO-8859-1 -t UTF-8 doc/NEWS.iso8859 > doc/NEWS

# XXX: a hack, actually as the original test is :(
# Depending on system load, output line count will differ.
# Just relax the check for heavily loaded build systems.
sed -i 's/-gt 8/-gt 6/' tests/008-numeric
sed -i 's/-lt 13/-lt 15/' tests/008-numeric

%build
%configure
%__make

%install
rm -rf %buildroot
%__make DESTDIR=%buildroot install
%find_lang %name

%check
%__make test

%files -f %name.lang
%defattr(-,root,root)
%doc README doc/{COPYING,NEWS,TODO}
%_bindir/%name
%_mandir/man1/%name.1.gz

%changelog
* Tue Oct 11 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 1.2.0-owl2
- Relaxed 008-numeric test because it wrongly relies on debatable performance
assumptions.  This test fails in some 'make world' cases.

* Thu Jan 27 2011 Vasiliy Kulikov <segoon-at-owl.openwall.com> 1.2.0-owl1
- Initial import from Fedora.
- Updated to 1.2.0.
