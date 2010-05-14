%define		bzrrev	21
%define		rel		0.3
Summary:	Spyke = Telepathy+Python+Skype
Name:		telepathy-spyke
Version:	0.1
Release:	0.%{bzrrev}.%{rel}
License:	GPL
Group:		Libraries
# bzr branch lp:spyke
# tar --exclude-vcs -cjf spyke-$(bzr revno spyke).tar.bz2 spyke
# ../dropin spyke-$(bzr revno spyke).tar.bz2
Source0:	spyke-%{bzrrev}.tar.bz2
# Source0-md5:	b216c16224fed4c048e14d52c5e77124
URL:		https://launchpad.net/spyke
BuildRequires:	python
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	python-shiny >= 0.1-1.4
# for pdb
Requires:	python-devel-tools
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Connection Manager for Skype.

%prep
%setup -q -n spyke

# rm dead links
rm data/icons/hicolor/16x16/apps/skype.png
rm data/icons/hicolor/32x32/apps/skype.png
rm data/icons/hicolor/48x48/apps/skype.png

# install to sys dir
sed -i -e 's,\.local/,,' setup.py

# dislike .py ext in $PATH
sed -i -e 's,Exec=/usr/bin/env telepathy_spyke.py,Exec=/usr/bin/env %{_bindir}/telepathy_spyke,' data/org.freedesktop.Telepathy.ConnectionManager.spyke.service

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_bindir}/telepathy_spyke{.py,}

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_datadir}/dbus-1/services/com.Skype.API.service
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.ConnectionManager.spyke.service
%{_datadir}/mission-control/profiles/skype.profile
%{_datadir}/telepathy/managers/spyke.manager
%attr(755,root,root) %{_bindir}/telepathy_spyke
%dir %{py_sitescriptdir}/spyke
%{py_sitescriptdir}/spyke/*.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/spyke-*.egg-info
%endif
