%global modname r8125

%if 0%{?fedora}
%global debug_package %{nil}
%endif

Name:           %{modname}
Version:        9.016.01
Release:        %autorelease
Summary:        Realtek RTL8125 Family 2.5GbE PCIe Kernel Driver
Group:          System Environment/Kernel
License:        GPL-2.0-only
URL:            https://www.realtek.com/Download/List?cate_id=584#:~:text=2%2E5G%20Ethernet%20LINUX%20driver%20r8125
BugURL:         https://github.com/makl11/r8125-akmod/issues
Source0:        %{modname}-%{version}.tar.bz2
Source1:        LICENSE
Source2:        modprobe.conf

BuildArch:      noarch

Provides: %{name}-kmod-common = %{version}
Requires: %{name}-kmod >= %{version}

BuildRequires: systemd-rpm-macros

%description
r8125 Kernel Driver for Realtek 2.5 Gigabit Ethernet PCI Express Network Interface Controllers
RTL8125 / RTL8125B(G) / RTL8125D / RTL8125K
RTL8125BP / RTL8125CP

%prep
%autosetup -C

%build
head -n32 Makefile | cat - %{SOURCE1} > LICENSE

%install
mkdir -p %{buildroot}%{_prefix}/lib/modprobe.d/
install -p -m 0644 %{SOURCE2} %{buildroot}%{_prefix}/lib/modprobe.d/%{modname}.conf

%files
%defattr(644, root, root, 755)
%doc README
%license LICENSE
%{_prefix}/lib/modprobe.d/%{modname}.conf

%changelog
%autochangelog
