Name:			libjsw
Version:		1.5.8
Release:		%mkrel 5

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
Provides:	jsw-devel = %{version}-%{release}
Obsoletes:	%{old_devel_name}

%description -n	%{devel_name}
This package contains the header files and libraries needed for
developing programs using the Joystick Wrapper library.

%{common_description}


%prep
%setup -q
perl -pi -e 's|#include <jsw.h>|#include "../include/jsw.h"|' js*/*.{c,h}

%build
pushd libjsw
  make CFLAGS="$RPM_OPT_FLAGS -fPIC" LIBS=-lstdc++
popd

%install
rm -rf %{buildroot}
for d in libjsw; do
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
%{_libdir}/libjsw.so.%{lib_major}*

%files -n %{devel_name}
%defattr(-,root,root)
%{_includedir}/jsw.h
%{_libdir}/libjsw.so
%{_mandir}/man3/*.3*


%changelog
* Thu Feb 10 2011 Funda Wang <fwang@mandriva.org> 1.5.8-5mdv2011.0
+ Revision: 637191
- only build libs

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

* Sun Mar 14 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.5.8-3mdv2010.1
+ Revision: 519104
- fix build dependencies
- fix dependencies

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Emmanuel Andry <eandry@mandriva.org>
    - New version 1.5.8
    - drop BR gtk1.2-devel

* Thu Jan 08 2009 Guillaume Bedot <littletux@mandriva.org> 1.5.7-1mdv2009.1
+ Revision: 327084
- Fix underlinking
- New policies and proposals
- 1.5.7

* Fri Jul 25 2008 Thierry Vignaud <tv@mandriva.org> 1.5.6-4mdv2009.0
+ Revision: 248839
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 2mdv2008.1-current
+ Revision: 140924
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Fri Jan 05 2007 Olivier Blin <oblin@mandriva.com> 1.5.6-2mdv2007.0
+ Revision: 104303
- fix library installation on x86_64
- build with -fPIC to fix x86_64 build
- buildrequire gtk+1.2-devel
- initial libjsw and jscalibrator release
- Create libjsw

