Name:			libjsw
Version:		1.5.7
Release:		%mkrel 1

%define lib_major	1
%define lib_name	%mklibname jsw %{lib_major}
%define devel_name	%mklibname jsw -d
%define old_devel_name	%mklibname jsw 1 -d

%define common_description The Joystick Wrapper library (libjsw) is designed to provide a uniform\
API and user configuration for joysticks and other game controllers on\
all platforms.\
\
It features an integrated library level calibration system using\
jscalibrator to provide a one time calibration for any program that\
uses libjsw. libjsw also features several levels of advanced joystick\
input error correction.

Summary:	Joystick Wrapper library
License:	GPLv2+
Group:		System/Kernel and hardware
URL:		http://wolfsinger.com/~wolfpack/packages/
Source0:	http://wolfsinger.com/~wolfpack/packages/%{name}-%{version}.tar.bz2

BuildRequires:	gtk+1.2-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
%{common_description}

%package -n %{lib_name}
Summary:	Joystick Wrapper library
Group:		System/Libraries

%description -n	%{lib_name}
This package contains the library needed to run programs dynamically
linked with the Joystick Wrapper library.

%{common_description}


%package -n %{devel_name}
Summary:	Development tools for programs using the Joystick Wrapper library
Group:		Development/C
Requires:	%{lib_name} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{old_devel_name}

%description -n	%{devel_name}
This package contains the header files and libraries needed for
developing programs using the Joystick Wrapper library.

%{common_description}


%package -n jscalibrator
Summary:	Joystick calibration utility
Group:		System/Libraries

%description -n jscalibrator
jscalibrator is a joystick calibration utility.

%{common_description}


%prep
%setup -q
perl -pi -e 's|#include <jsw.h>|#include "../include/jsw.h"|' js*/*.{c,h}

%build
pushd libjsw
  make CFLAGS="$RPM_OPT_FLAGS -fPIC"
popd
pushd jscalibrator
  make '*.o'
  make CC=g++ LIB_DIRS=-L../libjsw
popd

%install
rm -rf %{buildroot}
for d in libjsw jscalibrator; do
 pushd $d
 make install \
  PREFIX=%{buildroot}%{_prefix} \
  JSW_MAN_DIR=%{buildroot}%{_mandir}/man3 \
  JSW_LIB_DIR=%{buildroot}%{_libdir} \
  MAN_DIR=%{buildroot}%{_mandir}/man1
 popd
done

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%files -n %{lib_name}
%defattr(-,root,root)
%doc README
%{_libdir}/libjsw.so.*

%files -n %{devel_name}
%defattr(-,root,root)
%{_includedir}/jsw.h
%{_libdir}/libjsw.so
%{_mandir}/man3/*.3*

%files -n jscalibrator
%{_bindir}/jscalibrator
%{_iconsdir}/jscalibrator.xpm
%{_datadir}/libjsw/help/*.html
%{_datadir}/libjsw/help/*.png
%{_mandir}/man1/*.1*

