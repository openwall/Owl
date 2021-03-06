# $Owl: Owl/packages/dialog/dialog.spec,v 1.22 2014/07/12 14:08:46 galaxy Exp $

Summary: A utility for creating TTY dialog boxes.
Name: dialog
Version: 1.0
%define original_date 20051219
Release: owl3
License: GPL
Group: Applications/System
Source: ftp://dickey.his.com/dialog/%name-%version-%original_date.tgz
Patch0: dialog-1.0-owl-tmp.diff
Patch1: dialog-1.0-owl-warnings.diff
BuildRequires: ncurses-devel
BuildRoot: /override/%name-%version

%description
Displays user-friendly dialog boxes from shell scripts.
This application provides a method of displaying several different types
of dialog boxes from shell scripts.  This allows a developer of a script
to interact with the user in a much friendlier manner.

The following types of boxes are at your disposal:
  yes/no           Typical query style box with "Yes" and "No" answer buttons
  menu             A scrolling list of menu choices with single entry selection
  input            Query style box with text entry field
  message          Similar to the yes/no box, but with only an "Ok" button
  text             A scrollable text box that works like a simple file viewer
  info             A message display that allows asynchronous script execution
  checklist        Similar to the menu box, but allowing multiple selections
  radiolist        Checklist style box allowing single selections
  gauge            Typical "progress report" style box
  tail             Allows viewing the end of files (tail) that auto updates
  background tail  Similar to tail but runs in the background
  calendar         A calendar box displays month, day and year in
                   separately adjustable windows
  timebox          A dialog is displayed which allows you to select
                   hour, minute and second

%prep
%setup -q -n %name-%version-%original_date
%patch0 -p1
%patch1 -p1

%{expand:%%define optflags %optflags -Wall}

%build
export LDFLAGS=-ltinfo
%configure
make

%install
rm -rf %buildroot
%makeinstall

tar cjf samples.tar.bz2 samples/
bzip2 -9q CHANGES

%files
%defattr(-,root,root)
%doc COPYING CHANGES.bz2 README samples.tar.bz2
%_prefix/bin/dialog
%_mandir/man1/dialog.*

%changelog
* Sun Jul 22 2012 Vasiliy Kulikov <segoon-at-owl.openwall.com> 1.0-owl3
- Added -ltinfo into LDFLAGS to fix build error under binutils >= 2.21.

* Wed Jan 04 2006 Michail Litvak <mci-at-owl.openwall.com> 1.0-owl2
- bzip2'ed changelog and archived samples to reduce packet size.
- Improved -tmp patch.

* Fri Dec 30 2005 Michail Litvak <mci-at-owl.openwall.com> 1.0-owl1
- Updated to 1.0-20051219.
- Updated patches.

* Fri Jan 17 2003 Michail Litvak <mci-at-owl.openwall.com> 0.9b-owl2
- Patch to fix unsafe temporary file handling in samples.
- Patch from RSBAC project - allow help button using in
menubox widget without --item-help option.

* Fri Jan 10 2003 Michail Litvak <mci-at-owl.openwall.com>
- Update to new version (0.9b-20020814).
- Patch to fix warning on build.
- Dropped -owl-fselect.diff.

* Thu Jan 24 2002 Solar Designer <solar-at-owl.openwall.com>
- Enforce our new spec file conventions.
- Build with -Wall (no warnings).

* Wed Jun 13 2001 Michail Litvak <mci-at-owl.openwall.com>
- patch to fix bug with fselect mouse lock-up

* Tue Jun 12 2001 Michail Litvak <mci-at-owl.openwall.com>
- remove alt-tmpdir patch

* Sun Jun 10 2001 Michail Litvak <mci-at-owl.openwall.com>
- Updated to new version
- imported patches from ALT Linux

* Thu Dec 28 2000 Michail Litvak <mci-at-owl.openwall.com>
- Updated to new snapshot for fix file locking problem

* Thu Dec 07 2000 Michail Litvak <mci-at-owl.openwall.com>
- Imported from RH
- New upstream release
- Added patch to display '*' in passwordbox
