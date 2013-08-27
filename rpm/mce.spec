Name:       mce
Summary:    Mode Control Entity for Nokia mobile computers
Version:    1.13.1
Release:    1
Group:      System/System Control
License:    LGPLv2
URL:        https://github.com/nemomobile/mce
Source0:    %{name}-%{version}.tar.bz2
# Patches auto-generated by git-buildpackage:
Requires:   dsme
Requires:   systemd
Requires(preun): systemd
Requires(post): systemd
Requires(postun): systemd
BuildRequires:  pkgconfig(dbus-1) >= 1.0.2
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  pkgconfig(dsme) >= 0.58
BuildRequires:  pkgconfig(gconf-2.0)
BuildRequires:  pkgconfig(glib-2.0) >= 2.18.0
BuildRequires:  pkgconfig(mce) >= 1.12.3
BuildRequires:  kernel-headers >= 2.6.32
BuildRequires:  systemd
# systemd has /etc/rpm/macros.systemd

%description
This package contains the Mode Control Entity which provides
mode management features.  This is a daemon that is the backend
for many features on Nokia's mobile computers.

%package tools
Summary:    Tools for interacting with mce
Group:      Development/Tools
Requires:   %{name} = %{version}-%{release}

%description tools
This package contains tools that can be used to interact with
the Mode Control Entity and to get mode information.

%prep
%setup -q -n %{name}-%{version}

%build
./verify_version
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
# FIXME: we need a configure script ... for now pass dirs in make install
make install DESTDIR=%{buildroot} _UNITDIR=%{_unitdir}

%preun
if [ "$1" -eq 0 ]; then
  systemctl stop %{name}.service
fi

%post
systemctl daemon-reload
systemctl reload-or-try-restart %{name}.service

%postun
systemctl daemon-reload

%files
%defattr(-,root,root,-)
%doc COPYING debian/changelog debian/copyright
# binaries
%{_sbindir}/%{name}
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/modules
%{_libdir}/%{name}/modules/*.so
# config
%dir %config %{_sysconfdir}/%{name}
%config %{_sysconfdir}/%{name}/10mce.ini
%config %{_sysconfdir}/%{name}/20mce-radio-states.ini
%config %{_sysconfdir}/%{name}/20hybris-led.ini
# empty /var/lib/mce -> rpm
%dir %{_localstatedir}/lib/%{name}/
# NB empty /var/run/mce -> handled by systemd tmpfiles.d/mce.conf
# manpages
%{_mandir}/man8/%{name}.8.gz
# dbus
%config %{_sysconfdir}/dbus-1/system.d/mce.conf
# systemd
%config %{_sysconfdir}/tmpfiles.d/mce.conf
/lib/systemd/system/%{name}.service
/lib/systemd/system/multi-user.target.wants/%{name}.service

%files tools
%defattr(-,root,root,-)
%doc COPYING debian/copyright
%{_sbindir}/mcetool
%{_sbindir}/evdev_trace
%{_sbindir}/mcetorture
%{_mandir}/man8/mcetool.8.gz
%{_mandir}/man8/mcetorture.8.gz
