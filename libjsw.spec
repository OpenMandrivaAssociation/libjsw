%define major 1
%define libname %mklibname jsw %{major}
%define devname %mklibname jsw -d

Summary:	Joystick Wrapper library
Name:		libjsw
Version:	1.5.8
Release:	8
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		http://wolfsinger.com/~wolfpack/packages/
Source0:	http://wolfsinger.com/~wolfpack/packages/%{name}-%{version}.tar.bz2
Patch0:		libjsw-1.5.8-no-strip.patch
Patch1:		libjsw-1.5.8-soname.patch
Patch2:		libjsw-1.5.8-no-postinstall.patch

%description
The Joystick Wrapper library (libjsw) is designed to provide a uniform
API and user configuration for joysticks and other game controllers on
all platforms.

It features an integrated library level calibration system using
jscalibrator to provide a one time calibration for any program that
uses libjsw. libjsw also features several levels of advanced joystick
input error correction.

%package -n %{libname}
Summary:	Joystick Wrapper library
Group:		System/Libraries

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with the Joystick Wrapper library.

The Joystick Wrapper library (libjsw) is designed to provide a uniform
API and user configuration for joysticks and other game controllers on
all platforms.

It features an integrated library level calibration system using
jscalibrator to provide a one time calibration for any program that
uses libjsw. libjsw also features several levels of advanced joystick
input error correction.

%package -n %{devname}
Summary:	Development tools for programs using the Joystick Wrapper library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	jsw-devel = %{version}-%{release}

%description -n %{devname}
This package contains the header files and libraries needed for
developing programs using the Joystick Wrapper library.

The Joystick Wrapper library (libjsw) is designed to provide a uniform
API and user configuration for joysticks and other game controllers on
all platforms.

It features an integrated library level calibration system using
jscalibrator to provide a one time calibration for any program that
uses libjsw. libjsw also features several levels of advanced joystick
input error correction.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
perl -pi -e 's|#include <jsw.h>|#include "../include/jsw.h"|' js*/*.{c,h}

%build
pushd libjsw
    make CFLAGS="%{optflags} -fPIC" LIBS=-lstdc++
popd

%install
pushd libjsw
    make install \
	PREFIX=%{buildroot}%{_prefix} \
	JSW_MAN_DIR=%{buildroot}%{_mandir}/man3 \
	JSW_LIB_DIR=%{buildroot}%{_libdir} \
	MAN_DIR=%{buildroot}%{_mandir}/man1
popd

%files -n %{libname}
%{_libdir}/libjsw.so.%{major}*

%files -n %{devname}
%{_includedir}/jsw.h
%{_libdir}/libjsw.so
%{_mandir}/man3/*.3*

