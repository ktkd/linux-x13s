Name: kernel
Summary: The Linux Kernel
Version: 6.2.2+
Release: 1
License: GPL
Group: System Environment/Kernel
Vendor: The Linux Community
URL: https://www.kernel.org
Source: kernel-6.2.2+.tar.gz
Provides: kernel-drm kernel-6.2.2+
BuildRequires: bc binutils bison dwarves
BuildRequires: (elfutils-libelf-devel or libelf-devel) flex
BuildRequires: gcc make openssl openssl-devel perl python3 rsync

# aarch64 as a fallback of _arch in case
# /usr/lib/rpm/platform/*/macros was not included.
%define _arch %{?_arch:aarch64}
%define __spec_install_post /usr/lib/rpm/brp-compress || :
%define debug_package %{nil}

%description
The Linux Kernel, the operating system core itself

%package headers
Summary: Header files for the Linux kernel for use by glibc
Group: Development/System
Obsoletes: kernel-headers
Provides: kernel-headers = %{version}
%description headers
Kernel-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.

%package devel
Summary: Development package for building kernel modules to match the 6.2.2+ kernel
Group: System Environment/Kernel
AutoReqProv: no
%description -n kernel-devel
This package provides kernel headers and makefiles sufficient to build modules
against the 6.2.2+ kernel package.

%prep
%setup -q
rm -f scripts/basic/fixdep scripts/kconfig/conf
rm -f tools/objtool/{fixdep,objtool}

%build
make %{?_smp_mflags} KBUILD_BUILD_VERSION=%{release}

%install
mkdir -p %{buildroot}/boot
%ifarch ia64
mkdir -p %{buildroot}/boot/efi
cp $(make -s image_name) %{buildroot}/boot/efi/vmlinuz-6.2.2+
ln -s efi/vmlinuz-6.2.2+ %{buildroot}/boot/
%else
cp $(make -s image_name) %{buildroot}/boot/vmlinuz-6.2.2+
%endif
make %{?_smp_mflags} INSTALL_MOD_PATH=%{buildroot} modules_install
make %{?_smp_mflags} INSTALL_HDR_PATH=%{buildroot}/usr headers_install
cp System.map %{buildroot}/boot/System.map-6.2.2+
cp .config %{buildroot}/boot/config-6.2.2+
rm -f %{buildroot}/lib/modules/6.2.2+/build
rm -f %{buildroot}/lib/modules/6.2.2+/source
mkdir -p %{buildroot}/usr/src/kernels/6.2.2+
tar cf - --exclude SCCS --exclude BitKeeper --exclude .svn --exclude CVS --exclude .pc --exclude .hg --exclude .git --exclude=*vmlinux* --exclude=*.mod --exclude=*.o --exclude=*.ko --exclude=*.cmd --exclude=Documentation --exclude=.config.old --exclude=.missing-syscalls.d --exclude=*.s . | tar xf - -C %{buildroot}/usr/src/kernels/6.2.2+
cd %{buildroot}/lib/modules/6.2.2+
ln -sf /usr/src/kernels/6.2.2+ build
ln -sf /usr/src/kernels/6.2.2+ source

%clean
rm -rf %{buildroot}

%post
if [ -x /sbin/installkernel -a -r /boot/vmlinuz-6.2.2+ -a -r /boot/System.map-6.2.2+ ]; then
cp /boot/vmlinuz-6.2.2+ /boot/.vmlinuz-6.2.2+-rpm
cp /boot/System.map-6.2.2+ /boot/.System.map-6.2.2+-rpm
rm -f /boot/vmlinuz-6.2.2+ /boot/System.map-6.2.2+
/sbin/installkernel 6.2.2+ /boot/.vmlinuz-6.2.2+-rpm /boot/.System.map-6.2.2+-rpm
rm -f /boot/.vmlinuz-6.2.2+-rpm /boot/.System.map-6.2.2+-rpm
fi

%preun
if [ -x /sbin/new-kernel-pkg ]; then
new-kernel-pkg --remove 6.2.2+ --rminitrd --initrdfile=/boot/initramfs-6.2.2+.img
elif [ -x /usr/bin/kernel-install ]; then
kernel-install remove 6.2.2+
fi

%postun
if [ -x /sbin/update-bootloader ]; then
/sbin/update-bootloader --remove 6.2.2+
fi

%files
%defattr (-, root, root)
/lib/modules/6.2.2+
%exclude /lib/modules/6.2.2+/build
%exclude /lib/modules/6.2.2+/source
/boot/*

%files headers
%defattr (-, root, root)
/usr/include

%files devel
%defattr (-, root, root)
/usr/src/kernels/6.2.2+
/lib/modules/6.2.2+/build
/lib/modules/6.2.2+/source
