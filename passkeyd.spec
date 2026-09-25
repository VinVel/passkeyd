Name:           passkeyd
Version:        1.9.2
Release:        1%{?dist}
Summary:        Opinionated Linux WebAuthn authenticator
License:        GPL-3.0-only
URL:            https://github.com/bjn7/passkeyd
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  cargo-rpm-macros
BuildRequires:  clang-devel
BuildRequires:  gcc-c++
BuildRequires:  gtk4-devel
BuildRequires:  libudev-devel
BuildRequires:  pam-devel
BuildRequires:  pkgconfig
BuildRequires:  llvm-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  systemd-rpm-macros
BuildRequires:  tpm2-tss-devel
BuildRequires:  mold
BuildRequires:  cmake
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  glib2-devel
Requires:       systemd

%description
Passkeyd is a Linux WebAuthn authenticator that works with WebAuthn
applications, including browsers. It supports TPM-backed and software
cryptography and provides GTK, KDE, and Ice user interfaces.

%prep
%autosetup -n %{name}-%{version}

%build
%cargo_prep -N
sed -i 's/^offline = true$/offline = false/' .cargo/config.toml
%cargo_build

%install
install -Dpm0755 target/rpm/passkeyd %{buildroot}%{_bindir}/passkeyd
install -Dpm0755 target/rpm/passkeyd-manager %{buildroot}%{_bindir}/passkeyd-manager
install -Dpm0755 target/rpm/passkeyd-migrate %{buildroot}%{_bindir}/passkeyd-migrate

install -Dpm0755 target/rpm/passkeyd-ice-enroll %{buildroot}%{_libdir}/passkeyd/passkeyd-ice-enroll
install -Dpm0755 target/rpm/passkeyd-ice-select %{buildroot}%{_libdir}/passkeyd/passkeyd-ice-select
install -Dpm0755 target/rpm/passkeyd-ice-selection %{buildroot}%{_libdir}/passkeyd/passkeyd-ice-selection
install -Dpm0755 target/rpm/passkeyd-gtk-enroll %{buildroot}%{_libdir}/passkeyd/passkeyd-gtk-enroll
install -Dpm0755 target/rpm/passkeyd-gtk-select %{buildroot}%{_libdir}/passkeyd/passkeyd-gtk-select
install -Dpm0755 target/rpm/passkeyd-gtk-selection %{buildroot}%{_libdir}/passkeyd/passkeyd-gtk-selection
install -Dpm0755 target/rpm/passkeyd-kde-enroll %{buildroot}%{_libdir}/passkeyd/passkeyd-kde-enroll
install -Dpm0755 target/rpm/passkeyd-kde-select %{buildroot}%{_libdir}/passkeyd/passkeyd-kde-select
install -Dpm0755 target/rpm/passkeyd-kde-selection %{buildroot}%{_libdir}/passkeyd/passkeyd-kde-selection

install -Dpm0644 passkeyd.conf %{buildroot}%{_sysconfdir}/passkeyd.conf
install -Dpm0644 theme.conf %{buildroot}%{_datadir}/passkeyd/theme.conf
install -Dpm0644 passkeyd.service %{buildroot}%{_unitdir}/passkeyd.service
install -d -m0700 %{buildroot}%{_sharedstatedir}/passkeyd/database
install -Dpm0644 icons/32x32/passkeyd.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/passkeyd.png
install -Dpm0644 icons/64x64/passkeyd.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/passkeyd.png

%post
%systemd_post passkeyd.service

%preun
%systemd_preun passkeyd.service

%postun
%systemd_postun_with_restart passkeyd.service

%files
%license LICENSE
%config(noreplace) %{_sysconfdir}/passkeyd.conf
%{_bindir}/passkeyd
%{_bindir}/passkeyd-manager
%{_bindir}/passkeyd-migrate
%{_libdir}/passkeyd/
%{_datadir}/passkeyd/theme.conf
%{_datadir}/icons/hicolor/32x32/apps/passkeyd.png
%{_datadir}/icons/hicolor/64x64/apps/passkeyd.png
%{_unitdir}/passkeyd.service
%attr(0700,root,root) %{_sharedstatedir}/passkeyd/

%changelog
* Fri Sep 25 2026 passkeyd maintainers <maintainers@passkeyd.invalid> - 1.9.2-1
- Initial RPM package
