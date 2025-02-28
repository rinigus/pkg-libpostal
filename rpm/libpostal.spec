%if 0%{?sailfish_build}
%define static_only_build 1
%endif

Summary:  A C library for parsing/normalizing street addresses
Name: libpostal
Version: 1.0.0+git1
Release: 1%{?dist}

License: MIT
Group: Development/Libraries/Other
URL: https://github.com/openvenues/libpostal

Source0: %{name}-%{version}.tar.xz
Source1: libpostal-rpmlintrc

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gcc-c++
BuildRequires: libtool
#%if !0%{?sailfish_build}
#BuildRequires: pkg-config
#%endif

%description
A C library for parsing/normalizing street addresses around the world


%package devel
Summary: Libpostal development headers and static library
Group: Development/Libraries/Other
Requires: %{name} = %{version}

%description devel
A C library for parsing/normalizing street addresses around the world.
This package provides libraries and headers for development

%prep
%setup -q -n %{name}-%{version}/libpostal

%build
%{__make} clean || true

CFLAGS="$CFLAGS -fPIC -lstdc++"
CXXFLAGS="$CXXFLAGS -fPIC"
./bootstrap.sh

CONFEXTRA=""

%ifarch armv7hl
CONFEXTRA="--with-cflags-scanner-extra=-marm --disable-sse2"
%endif
%ifarch aarch64
CONFEXTRA="--disable-sse2"
%endif

%configure --datadir=/usr/local/libpostal/data --disable-data-download \
%if 0%{?static_only_build}
           --enable-static --disable-shared \
%else
           --disable-static --enable-shared \
%endif
           $CONFEXTRA

%{__make} %{?_smp_mflags}

%install
%{__make} install DESTDIR=%{buildroot}
%{__rm} -rf %{buildroot}%{_libdir}/libpostal.la ||:

%clean
%{__rm} -rf %{buildroot}

%pre

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%{_bindir}/libpostal_data
%if !0%{?static_only_build}
%{_libdir}/libpostal*.so.*
%endif

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/libpostal
%{_libdir}/libpostal*.so
%if 0%{?static_only_build}
%{_libdir}/libpostal.a
%endif
%{_libdir}/pkgconfig/libpostal.pc

%changelog
* Fri May 18 2018 rinigus <rinigus.git@gmail.com> - 1.0.0-1
- update to 1.0 libpostal

* Wed Jan 18 2017 rinigus <rinigus.git@gmail.com> - 0.3.3-1
- initial packaging release for SFOS
