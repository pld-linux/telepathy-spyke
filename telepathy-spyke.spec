%define		bzrrev	21
%define		rel		0.3
Summary:	Spyke = Telepathy+Python+Skype - connection manager
Summary(pl.UTF-8):	Spyke = Telepathy+Python+Skype - zarządca połączeń
Name:		telepathy-spyke
Version:	0.1
Release:	0.%{bzrrev}.%{rel}
License:	GPL v3+
Group:		Libraries
# bzr branch lp:spyke
# tar --exclude-vcs -cjf spyke-$(bzr revno spyke).tar.bz2 spyke
# ../dropin spyke-$(bzr revno spyke).tar.bz2
Source0:	spyke-%{bzrrev}.tar.bz2
# Source0-md5:	b216c16224fed4c048e14d52c5e77124
URL:		https://launchpad.net/spyke
BuildRequires:	python >= 1:2.6
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-shiny >= 0.1-1.4
# for pdb
Requires:	python-devel-tools
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Connection Manager for Skype.

%description
Zarządca połączeń dla Skype'a.

%prep
%setup -q -n spyke

# rm dead links
%{__rm} data/icons/hicolor/16x16/apps/skype.png
%{__rm} data/icons/hicolor/32x32/apps/skype.png
%{__rm} data/icons/hicolor/48x48/apps/skype.png

# install to sys dir
%{__sed} -i -e 's,\.local/,,' setup.py

# dislike .py ext in $PATH, no need for env
%{__sed} -i -e 's,Exec=/usr/bin/env telepathy_spyke.py,Exec=%{_bindir}/telepathy_spyke,' data/org.freedesktop.Telepathy.ConnectionManager.spyke.service

%build
%py_build

%install
rm -rf $RPM_BUILD_ROOT

%py_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/telepathy_spyke{.py,}

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/telepathy_spyke
%{_datadir}/dbus-1/services/com.Skype.API.service
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.ConnectionManager.spyke.service
%{_datadir}/mission-control/profiles/skype.profile
%{_datadir}/telepathy/managers/spyke.manager
%dir %{py_sitescriptdir}/spyke
%{py_sitescriptdir}/spyke/*.py[co]
%{py_sitescriptdir}/spyke-0.1-py*.egg-info
