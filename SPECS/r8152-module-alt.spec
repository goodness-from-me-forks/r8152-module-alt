%define vendor_name Realtek
%define vendor_label realtek
%define driver_name r8152

%if %undefined module_dir
%define module_dir extra
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{driver_name}-module-alt
Version: 2.18.1
Release: 1%{?dist}
License: GPL

#Source taken from https://github.com/wget/realtek-r8152-linux/archive/refs/tags/v2.18.1.20240701.tar.gz
Source0: %{driver_name}-alt-%{version}.tar.gz
Patch0: fix-conditional-check-for-kernel-version.patch

BuildRequires: gcc
BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n %{driver_name}-%{version}

%build
%{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd) KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko

%changelog
* Sat Oct 05 2024 Vasyl Solovei <iam@miltador.pro> - 2.18.1-1
- Adding Realtek driver r8152 v2.18.1