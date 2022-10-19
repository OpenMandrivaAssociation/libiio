%define major 0
%define libname %mklibname iio %{major}
%define devname %mklibname -d iio

Name:          libiio
Version:       0.24
Release:       1
Summary:       Library for Industrial IO
License:       LGPLv2
URL:           https://analogdevicesinc.github.io/libiio/
Source0:       https://github.com/analogdevicesinc/libiio/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:        libiio-0.23-aarch64-build-workaround.patch

BuildRequires: bison
BuildRequires: cmake
BuildRequires: ninja
BuildRequires: doxygen
BuildRequires: flex
BuildRequires: pkgconfig(libserialport)
BuildRequires: libaio-devel
BuildRequires: pkgconfig(libusb)
BuildRequires: libxml2-devel
BuildRequires: graphviz
BuildRequires: pkgconfig(avahi-client)
BuildRequires: git-core
BuildRequires: python-devel
BuildRequires: python-setuptools
BuildRequires: python-sphinx
BuildRequires: python-sphinx_rtd_theme

%description
Library for interfacing with Linux IIO devices

libiio is used to interface to Linux Industrial Input/Output (IIO) Subsystem.
The Linux IIO subsystem is intended to provide support for devices that in some 
sense are analog to digital or digital to analog converters (ADCs, DACs). This 
includes, but is not limited to ADCs, Accelerometers, Gyros, IMUs, Capacitance 
to Digital Converters (CDCs), Pressure Sensors, Color, Light and Proximity 
Sensors, Temperature Sensors, Magnetometers, DACs, DDS (Direct Digital 
Synthesis), PLLs (Phase Locked Loops), Variable/Programmable Gain Amplifiers 
(VGA, PGA), and RF transceivers.

%package utils
Summary: Utilities for Industrial IO
Requires: %{libname} = %{EVRD}

%description utils
Utilities for accessing IIO using libiio

%package -n %{libname}
Summary: Development package for %{name}

%description -n %{libname}
Library for Industrial IO

%package -n %{devname}
Summary: Development package for %{name}
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Files for development with %{name}.

%package doc
Summary: Development documentation for %{name}

%description doc
Documentation for development with %{name}.

%package -n python-iio
Summary: Python bindings for Industrial IO (libiio)
Requires: %{libname} = %{EVRD}

%description -n python-iio
Python 3 bindings for Industrial IO

%prep
%autosetup -p1
sed -i 's/${LIBIIO_VERSION_MAJOR}-doc//' CMakeLists.txt

%build
%cmake \
	-DPYTHON_BINDINGS=on \
	-DWITH_DOC=on \
	-DUDEV_RULES_INSTALL_DIR=%{_udevrulesdir} \
	. \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*

%files utils
%license COPYING.txt
%{_udevrulesdir}/90-libiio.rules
%{_bindir}/iio_*
%{_sbindir}/iiod

%files -n %{devname}
%{_includedir}/iio.h
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/%{name}.so

%files doc
%doc %{_docdir}/%{name}

%files -n python-iio
%{python_sitelib}/iio*
%{python_sitelib}/pylibiio*
