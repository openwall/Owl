# $Owl: Owl/packages/sed/sed.spec,v 1.17.2.1 2008/03/16 23:59:33 ldv Exp $

Summary: A GNU stream text editor.
Name: sed
Version: 4.1.5
Release: owl1
License: GPL
Group: Applications/Text
URL: http://www.gnu.org/software/sed/
Source0: ftp://ftp.gnu.org/gnu/sed/sed-%version.tar.gz
# Original sources were downloaded from:
# http://sed.sourceforge.net/grabbag/tutorials/sedfaq.txt
# http://sed.sourceforge.net/sed1line.txt
Source1: sedfaq-015.txt.bz2
Source2: sed1line-5.5.txt.bz2
Patch0: sed-4.1.5-owl-warnings.diff
Patch1: sed-4.0.9-owl-info.diff
Patch2: sed-4.1.2-alt-doc.diff
Patch3: sed-4.1.5-alt-doc-sedfaq.diff
Patch4: sed-4.1.2-deb-doc.diff
Patch5: sed-4.1.4-owl-configure.diff
PreReq: /sbin/install-info
BuildRequires: texinfo
BuildRoot: /override/%name-%version

%description
The sed (Stream EDitor) editor is a stream or batch (non-interactive)
editor.  sed takes text as input, performs an operation or set of
operations on the text and outputs the modified text.  The operations
that sed performs (substitutions, deletions, insertions, etc.) can be
specified in a script file or from the command line.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

install -pm644 %_sourcedir/sedfaq-015.txt.bz2 doc/sedfaq.txt.bz2
install -pm644 %_sourcedir/sed1line-5.5.txt.bz2 doc/sed1line.txt.bz2
bzip2 -9fk ChangeLog NEWS

%{expand:%%define optflags %optflags -Wall}

%build
rm doc/sed.info
%configure

%__make SUBDIRS='lib sed'
./sed/sed -i 's,@DOCDIR@,%_docdir/%name-%version,' doc/sed-in.texi doc/sed.x
%__make

%__make -k check

%install
rm -rf %buildroot

%makeinstall
mv %buildroot%_bindir %buildroot/bin

# Remove unpackaged files
rm %buildroot%_infodir/dir

%post
/sbin/install-info %_infodir/sed.info %_infodir/dir

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %_infodir/sed.info %_infodir/dir
fi

%files
%defattr(-,root,root)
%doc AUTHORS BUGS ChangeLog.bz2 NEWS.bz2 README THANKS doc/*.txt.bz2
/bin/sed
%_infodir/*.info*
%_datadir/locale/*/*/*
%_mandir/man*/*

%changelog
* Mon Feb 20 2006 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.1.5-owl1
- Updated sed to 4.1.5.
- Updated sed1line.txt to version 5.5.

* Sat Nov 12 2005 Dmitry V. Levin <ldv-at-owl.openwall.com> 4.1.4-owl1
- Updated to 4.1.4.
- Applied upstream fix for off-by-one error in the "invalid reference
to subexpression" message.
- Imported sed(1) corrections from Debian and ALT.
- Packaged sed1line.txt and the sed FAQ.

* Fri Jul 16 2004 Solar Designer <solar-at-owl.openwall.com> 4.1.1-owl1
- Updated to 4.1.1.

* Mon Jul 12 2004 Michail Litvak <mci-at-owl.openwall.com> 4.0.9-owl1
- 4.0.9

* Mon Aug 19 2002 Michail Litvak <mci-at-owl.openwall.com> 3.02-owl9
- Deal with info dir entries such that the menu looks pretty.

* Wed Feb 06 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.

* Sun Aug 06 2000 Alexandr D. Kanevskiy <kad-at-owl.openwall.com>
- import spec from RH rawhide
- fix URL
