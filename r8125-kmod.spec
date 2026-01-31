%global         modname                 r8125
%global         _sysconf_modprobe_d     %{_sysconfdir}/modprobe.d/
%global         buildforkernels         akmod
%global         AkmodsBuildRequires     make gcc sed gawk

%if 0%{?fedora}
%global         debug_package           %{nil}
%endif

Name:           %{modname}-kmod
Version:        9.016.01
Release:        2%{?dist}
Summary:        Realtek RTL8125 Family 2.5GbE PCIe Kernel module
Group:          System Environment/Kernel
License:        GPL-2.0-or-later
URL:            https://www.realtek.com/Download/List?cate_id=584
BugURL:         https://github.com/makl11/r8125-akmod/issues

# Realtek protects the download using a captcha
# https://www.realtek.com/Download/ToDownload?type=direct&downloadid=3763
Source0:        %{modname}-%{version}.tar.bz2
Source1:        LICENSE
Source2:        modprobe.conf

Provides:       %{name}-kmod >= %{version}
Requires:       %{name}-kmod-common = %{version}

BuildRequires:  kmodtool systemd-rpm-macros

%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
r8125 Kernel module for Realtek 2.5 Gigabit Ethernet PCI Express
Network Interface Controllers

RTL8125 / RTL8125B(G) / RTL8125D / RTL8125K
RTL8125BP / RTL8125CP

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%autosetup -C

cp -v %{SOURCE1} LICENSE
chmod 644 LICENSE README

for kernel_version in %{?kernel_versions}; do
  mkdir -p _kmod_build_${kernel_version%%___*}
  cp -a src/ _kmod_build_${kernel_version%%___*}/%{name}-%{version}
done

%build
for kernel_version in %{?kernel_versions}; do
  pushd _kmod_build_${kernel_version%%___*}/%{name}-%{version}
     %{make_build} KERNELDIR="${kernel_version##*___}" modules
  popd
done

%install
for kernel_version in %{?kernel_versions}; do
  mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
  install -D -m 755 _kmod_build_${kernel_version%%___*}/%{name}-%{version}/%{modname}.ko \
    %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
done
%{?akmod_install}

install -p -m 0755 -d %{buildroot}%{_modprobedir}/
install -p -m 0644 %{SOURCE2} %{buildroot}%{_modprobedir}/%{modname}.conf

%files
# None

%package common
Release:        4%{?dist}
Summary:        Common files for %{modname}-kmod

%description common
Common files for Realtek RTL8125 Family 2.5GbE PCIe Kernel module

%files common
%doc README
%license LICENSE
%dir %{_modprobedir}
%config %{_modprobedir}/%{modname}.conf
%ghost %{_sysconf_modprobe_d}%{modname}.conf

%changelog