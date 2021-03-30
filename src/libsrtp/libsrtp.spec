%define __debug_install_post \
%{_rpmconfigdir}/find-debuginfo.sh %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"\
%{nil}

%global shortname srtp

Name:		libsrtp
Version:	2.3.0
Release:        1%{?dist}
Summary:	An implementation of the Secure Real-time Transport Protocol (SRTP)
License:	BSD
URL:		https://github.com/cisco/libsrtp
Source0:	https://github.com/cisco/libsrtp/archive/v%{version}.tar.gz
Source1:	sources.md5sum

BuildRequires:	gcc
BuildRequires:  openssl-devel

%description
This package provides an implementation of the Secure Real-time
Transport Protocol (SRTP), the Universal Security Transform (UST), and
a supporting cryptographic kernel.

%package devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
pushd %{_sourcedir}
grep $(basename %{SOURCE0})  %{SOURCE1} | md5sum -c
popd

%setup -q -n %{name}-%{version}


%build
export CFLAGS="%{optflags} -fPIC"
%configure --enable-openssl
make %{?_smp_mflags}
make %{?_smp_mflags} shared_library
make runtest

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc doc/*.txt 
%{_libdir}/*.so.*
%{_libdir}/*.so
%{_libdir}/*.a

%files devel
%{_includedir}/%{shortname}2/
%{_libdir}/pkgconfig/libsrtp2.pc

%changelog
* Thu Apr 16 2020 Francisco Correia <fcorreia@users.noreply.github.com> - 1.6.0
- Bump version

* Thu Apr 16 2020 Francisco Correia <fcorreia@users.noreply.github.com> - 1.5.4
- Initial Spec file from Fedora project: https://src.fedoraproject.org/rpms/libsrtp.git
