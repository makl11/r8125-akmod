%global modname r8125

%if 0%{?fedora}
%global debug_package %{nil}
%endif

Name:           %{modname}
Version:        9.016.01
Release:        1%{?dist}
Vendor:         Realtek
Summary:        Realtek %{modname} 2.5GbE PCIE Kernel Driver
Group:          System Environment/Kernel
License:        GPL-2.0-only
URL:            https://www.realtek.com/Download/List?cate_id=584#:~:text=2%2E5G%20Ethernet%20LINUX%20driver%20r8125
BugURL:         https://github.com/makl11/r8125-akmod/issues
Source0:        %{modname}-%{version}.tar.bz2

Provides: %{name}-kmod-common = %{version}
Requires: %{name}-kmod >= %{version}

BuildRequires: systemd-rpm-macros

%description
Realtek r8125 2.5GbE PCIE Kernel Driver
RTL8125 / RTL8125B(G) / RTL8125D / RTL8125K
RTL8125BP / RTL8125CP

%prep
%autosetup -C

%build
head -n32 Makefile > LICENSE

%install
install -D -m 0644 %{SOURCE0} %{buildroot}%{_datarootdir}/licenses/%{modname}/LICENSE

%files
%doc README
%license LICENSE

%changelog
