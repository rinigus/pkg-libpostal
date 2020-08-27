%if !0%{?on_suse_obs}
%define static_build 1
%endif

Summary:  A C library for parsing/normalizing street addresses
Name: libpostal
Version: 0.3.4
Release: 1%{?dist}

License: MIT
Group: Development/Libraries
URL: https://github.com/openvenues/libpostal

%if 0%{?on_suse_obs}
Source: _service
%else
Source: %{name}-%{version}.tar.gz
%endif

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gcc-c++
BuildRequires: libtool

%description
A C library for parsing/normalizing street addresses around the world


%package devel
Summary: libpostal development headers and static library
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
A C library for parsing/normalizing street addresses around the world.
This package provides libraries and headers for development

%prep
%if 0%{?on_suse_obs}
%setup -q -n %_sourcedir/%{name}/libpostal -T -D
%else
%setup -q -n %{name}-%{version}/libpostal
%endif

%build
%{__make} clean || true

CFLAGS="$CFLAGS -fPIC -lstdc++"
CXXFLAGS="$CXXFLAGS -fPIC"
./bootstrap.sh

CONFEXTRA=""

%ifarch armv7hl
CONFEXTRA="--with-cflags-scanner-extra=-marm --disable-sse2"
%endif

%configure --datadir=/usr/local/libpostal/data --disable-data-download \
%if 0%{?static_build}
           --enable-static --disable-shared
%else
           --disable-static --enable-shared
%endif
           $CONFEXTRA

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%pre

%post

%files
%defattr(-, root, root, 0755)
%{_bindir}/libpostal_data
%if !0%{?static_build}
%{_libdir}/libpostal*.so*
%endif

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/libpostal
%if 0%{?static_build}
%{_libdir}/libpostal.a
%endif
%{_libdir}/libpostal.la
%{_libdir}/pkgconfig/libpostal.pc

%changelog
* Fri May 18 2018 rinigus <rinigus.git@gmail.com> - 1.0.0-1
- update to 1.0 libpostal

* Wed Jan 18 2017 rinigus <rinigus.git@gmail.com> - 0.3.3-1
- initial packaging release for SFOS
