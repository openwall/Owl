# $Id: Owl/packages/dialog/dialog.spec,v 1.8 2002/01/24 17:31:28 solar Exp $

Summary: A utility for creating TTY dialog boxes.
Name: dialog
Version: 0.9a
%define original_date 20010527
Release: owl9
License: GPL
Group: Applications/System
Source: ftp://dickey.his.com/dialog/%{name}-%{version}-%{original_date}.tgz
Patch0: dialog-0.9a-owl-pwdbox.diff
Patch1: dialog-0.9a-alt-locale.diff
Patch2: dialog-0.9a-owl-fselect.diff
BuildRoot: /override/%{name}-%{version}

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
  background tail  Similar to tail but runs in the background.
  calendar         A calendar box displays month, day and year in
		   separately adjustable windows
  timebox	   A dialog is displayed which allows you to select
                   hour, minute and second.

%prep
%setup -q -n %{name}-%{version}-%{original_date}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%configure --enable-nls
make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING CHANGES README samples
%{_prefix}/bin/dialog
%{_mandir}/man1/dialog.*

%changelog
* Thu Jan 24 2002 Solar Designer <solar@owl.openwall.com>
- Enforce our new spec file conventions.

* Sun Jun 13 2001 Michail Litvak <mci@owl.openwall.com>
- patch to fix bug with fselect mouse lock-up

* Tue Jun 12 2001 Michail Litvak <mci@owl.openwall.com>
- remove alt-tmpdir patch

* Sun Jun 10 2001 Michail Litvak <mci@owl.openwall.com>
- Updated to new version
- imported patches from ALT Linux

* Thu Dec 28 2000 Michail Litvak <mci@owl.openwall.com>
- Updated to new snapshot for fix file locking problem

* Thu Dec 07 2000 Michail Litvak <mci@owl.openwall.com>
- Imported from RH
- New upstream release
- Added patch to display '*' in passwordbox
