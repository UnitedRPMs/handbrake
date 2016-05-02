Name:           handbrake
Summary:        Multithreaded Video Transcoder
Version:        0.10.5
Release:	2%{dist}
Url:            http://handbrake.fr/
Source:         https://handbrake.fr/mirror/HandBrake-%{version}.tar.bz2
License:        GPLv2
Group:          Applications/Multimedia
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  cmake
BuildRequires:  curl
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  intltool
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  nasm
BuildRequires:  python > 2.7.3
BuildRequires:  subversion
BuildRequires:  desktop-file-utils
BuildRequires:  wget
BuildRequires:  yasm
BuildRequires:  glibc-devel
BuildRequires:  lame-devel
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  pkgconfig(dvdnav)
BuildRequires:  pkgconfig(dvdread)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:  pkgconfig(gtk+-3.0) >= 3.10
BuildRequires:  pkgconfig(webkitgtk-3.0)
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(libass)
BuildRequires:  pkgconfig(libavcodec) >= 57
BuildRequires:  pkgconfig(libavformat) >= 57
BuildRequires:  pkgconfig(libavresample) >= 3
BuildRequires:  pkgconfig(libavutil) >= 55
BuildRequires:  pkgconfig(libswscale) >= 4
BuildRequires:  pkgconfig(libbluray)
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(samplerate)
BuildRequires:  pkgconfig(theora)
BuildRequires:  pkgconfig(vorbis)
BuildRequires:  pkgconfig(vpx)
BuildRequires:  pkgconfig(x264)
BuildRequires:  pkgconfig(x265)
Requires: 	%{name}-cli = %{version}-%{release}
Requires: 	%{name}-gui = %{version}-%{release}
Requires:	desktop-file-utils

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
HandBrake is an open-source, GPL-licensed, multiplatform, multithreaded video
transcoder.

%package cli
Summary:        Multithreaded Video Transcoder
Group:          Applications/Multimedia
Provides:	HandBrake-cli = %{version}-%{release}

%description cli
HandBrake is an open-source, GPL-licensed, multiplatform, multithreaded video
transcoder.

This package contains a command-line interface for Handbrake.


%package gui
Summary:        Multithreaded Video Transcoder
Group:          Applications/Multimedia
Provides:	HandBrake-gui = %{version}-%{release}


%description gui
HandBrake is an open-source, GPL-licensed, multiplatform, multithreaded video
transcoder.

This package contains a GTK+ graphical user interface for Handbrake.


%prep
%setup -q -n HandBrake-%{version}

  # Use more system libs
  # We had ffmpeg here as well but it broke PGS subtitle processing
  # https://forum.handbrake.fr/viewtopic.php?f=13&t=27581
  sed -i \
    -e '/MODULES += contrib\/libbluray/d' \
    -e '/MODULES += contrib\/libdvdnav/d' \
    -e '/MODULES += contrib\/libdvdread/d' \
    make/include/main.defs

%build

  ./configure \
    --prefix=/usr \
    --force \
    --disable-gtk-update-checks
 
pushd build  
make

%install

make install DESTDIR=%{buildroot} -C build

%check

desktop-file-validate %{buildroot}%{_datadir}/applications/ghb.desktop

%find_lang ghb

%post gui
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun gui
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans gui
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f ghb.lang

%files cli
%defattr(-,root,root)
%doc AUTHORS COPYING CREDITS NEWS THANKS
%{_bindir}/HandBrakeCLI

%files gui
%defattr(-,root,root)
%doc AUTHORS COPYING CREDITS NEWS THANKS
%{_bindir}/ghb
%{_datadir}/applications/ghb.desktop
%{_datadir}/icons/hicolor/scalable/apps/hb-icon.*



%changelog
* Mon May 2 2016 Pavlo Rudyi <paulcarroty at riseup.net> - 0.10.5-2
- Added scriptlets

* Thu Apr 28 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.10.5-1
- Initial build


