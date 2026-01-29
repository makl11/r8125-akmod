%global         modname           r8125
%global         buildforkernels   akmod

%if 0%{?fedora}
%global         debug_package     %{nil}
%endif

Name:           %{modname}-kmod
Version:        9.016.01
Release:        %autorelease
Summary:        Realtek RTL8125 Family 2.5GbE PCIe Kernel Driver
Group:          System Environment/Kernel
License:        GPL-2.0-only
URL:            https://www.realtek.com/Download/List?cate_id=584#:~:text=2%2E5G%20Ethernet%20LINUX%20driver%20r8125
BugURL:         https://github.com/makl11/r8125-akmod/issues
# Realtek protects the download using a captcha
# https://www.realtek.com/Download/ToDownload?type=direct&downloadid=3763
Source0:        %{modname}-%{version}.tar.bz2

BuildRequires:  kmodtool make gcc sed gawk

%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
r8125 Kernel Driver for Realtek 2.5 Gigabit Ethernet PCI Express
Network Interface Controllers

RTL8125 / RTL8125B(G) / RTL8125D / RTL8125K
RTL8125BP / RTL8125CP

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%autosetup -C

for kernel_version in %{?kernel_versions}; do
  mkdir -p _kmod_build_${kernel_version%%___*}
  cp -r src/ _kmod_build_${kernel_version%%___*}/%{name}-%{version}
done

%build
for kernel_version in %{?kernel_versions}; do
  pushd _kmod_build_${kernel_version%%___*}/%{name}-%{version}
     make KERNELDIR="${kernel_version##*___}" print_vars
     make KERNELDIR="${kernel_version##*___}" clean
     make KERNELDIR="${kernel_version##*___}" modules
  popd
done

%install
for kernel_version in %{?kernel_versions}; do
  mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
  install -D -m 755 _kmod_build_${kernel_version%%___*}/%{name}-%{version}/%{modname}.ko \
    %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
done
%{?akmod_install}

%changelog
%autochangelog
