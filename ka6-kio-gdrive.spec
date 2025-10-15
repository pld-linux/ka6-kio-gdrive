#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.08.2
%define		kframever	6.8
%define		qtver		6.8
%define		kaname		kio-gdrive
Summary:	kio-gdrive
Name:		ka6-%{kaname}
Version:	25.08.2
Release:	2
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	525b01db4f0ff5a9697d5a7959dd0acd
URL:		https://www.kde.org/
BuildRequires:	OpenEXR-devel >= 3.0.5
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= 5.4.0
BuildRequires:	Qt6Widgets-devel >= 5.4.0
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-tools
BuildRequires:	intltool
BuildRequires:	ka6-kaccounts-integration-devel >= %{kdeappsver}
BuildRequires:	ka6-libkgapi-devel >= %{kdeappsver}
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-karchive-devel >= %{kframever}
BuildRequires:	kf6-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf6-kdnssd-devel >= %{kframever}
BuildRequires:	kf6-kdoctools-devel >= %{kframever}
BuildRequires:	kf6-kguiaddons-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	kf6-knotifications-devel >= %{kframever}
BuildRequires:	kf6-purpose-devel >= %{kframever}
BuildRequires:	kf6-solid-devel >= %{kframever}
BuildRequires:	kf6-syntax-highlighting-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
kio-gdrive.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

# not supported by glibc yet
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%doc HACKING README.md README.packagers
%attr(755,root,root) %{_libdir}/qt6/plugins/kaccounts/daemonplugins/gdrive.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kfileitemaction/gdrivecontextmenuaction.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kio/gdrive.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/propertiesdialog/gdrivepropertiesplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/purpose/purpose_gdrive.so
%{_datadir}/accounts/services/kde/google-drive.service
%{_datadir}/knotifications6/gdrive.notifyrc
%{_datadir}/metainfo/org.kde.kio_gdrive.metainfo.xml
%dir %{_datadir}/purpose
%{_datadir}/purpose/purpose_gdrive_config.qml
%{_datadir}/remoteview/gdrive-network.desktop
