%define _legacy_common_support 1

%global desktop_id fr.handbrake.ghb
%global commit0 a8bc2549b3de632e2597cb133bc3aa20ca8a3629
%global date 20200507
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%define _legacy_common_support 1
%global _lto_cflags %{nil}

Name:           handbrake
Version:        1.4.2
Release:        7%{?dist}
Summary:        An open-source multiplatform video transcoder
License:        GPLv2+
URL:            http://handbrake.fr/

Source0:        https://github.com/handbrake/handbrake/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz


BuildRequires:  a52dec-devel >= 0.7.4
BuildRequires:  cmake
BuildRequires:  bzip2-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  desktop-file-utils
# Should be >= 2.12.1:
BuildRequires:  fontconfig-devel >= 2.10.95
# Should be >= 2.6.5:
BuildRequires:  freetype-devel >= 2.4.11
# Should be >= 0.19.7:
BuildRequires:  fribidi-devel >= 0.19.4
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
# Should be >= 1.3.0
BuildRequires:  harfbuzz-devel
BuildRequires:  intltool
BuildRequires:  jansson-devel
BuildRequires:  lame-devel >= 3.98
BuildRequires:  libappindicator-gtk3-devel
# Should be >= 0.13.2:
BuildRequires:  libass-devel >= 0.13.1
# Contains a required patch for HandBrake 1.0:
BuildRequires:  libbluray-devel >= 0.9.3-2
BuildRequires:  libdvdnav-devel >= 5.0.1
%if 0%{?fedora} >= 34
BuildRequires:  pkgconfig(dvdread) >= 6.1.1
%else
BuildRequires:  pkgconfig(dvdread)
%endif
BuildRequires:  libgudev1-devel
BuildRequires:  libmfx-devel >= 1.16
BuildRequires:  libmpeg2-devel >= 0.5.1
BuildRequires:  libnotify-devel
BuildRequires:  libogg-devel
BuildRequires:  librsvg2-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  libtheora-devel
BuildRequires:  libtool
BuildRequires:  libva-devel
BuildRequires:  libvorbis-devel
# Should be >= 1.5.0:
BuildRequires:  libvpx-devel >= 1.3
BuildRequires:  libxml2-devel
BuildRequires:  m4
BuildRequires:  make
BuildRequires:  opencl-headers
# Should be >= 1.1.3:
BuildRequires:  opus-devel
BuildRequires:  patch
BuildRequires:  python3-devel
BuildRequires:  subversion
BuildRequires:  tar
BuildRequires:  webkitgtk4-devel
BuildRequires:  wget
BuildRequires:  x264-devel >= 1:0.163
BuildRequires:  x265-devel >= 3.5
BuildRequires:  yasm
BuildRequires:  zlib-devel
BuildRequires:	git
BuildRequires:	wget
BuildRequires:	speex-devel
BuildRequires:  gcc-c++
BuildRequires:	numactl-devel
BuildRequires:	meson
BuildRequires:	nasm
BuildRequires:	gtk3-devel
BuildRequires:	libdrm-devel
BuildRequires:	libdav1d-devel
BuildRequires:	turbojpeg-devel
#BuildRequires:	intel-mediasdk-devel

# ffmpeg
BuildRequires:	xvidcore-devel lame-devel twolame-devel twolame-devel yasm ladspa-devel libbs2b-devel libmysofa-devel game-music-emu-devel soxr-devel libssh-devel libvpx-devel libvorbis-devel opus-devel libtheora-devel freetype-devel
BuildRequires:  automake libtool

Requires:       hicolor-icon-theme

%description
%{name} is a general-purpose, free, open-source, cross-platform, multithreaded
video transcoder software application. It can process most common multimedia
files and any DVD or Bluray sources that do not contain any kind of copy
protection.

%package gui
Summary:        An open-source multiplatform video transcoder (GUI)
Obsoletes:      HandBrake < %{version}-%{release}
Provides:       HandBrake = %{version}-%{release}
Requires:       hicolor-icon-theme
Requires:       libdvdcss%{_isa}

%description gui
%{name} is a general-purpose, free, open-source, cross-platform, multithreaded
video transcoder software application. It can process most common multimedia
files and any DVD or Bluray sources that do not contain any kind of copy
protection.

This package contains the main program with a graphical interface.

%package cli
Summary:        An open-source multiplatform video transcoder (CLI)
Requires:       libdvdcss%{_isa}

%description cli
%{name} is a general-purpose, free, open-source, cross-platform, multithreaded
video transcoder software application. It can process most common multimedia
files and any DVD or Bluray sources that do not contain any kind of copy
protection.

This package contains the command line version of the program.

%prep
%autosetup -p1 -n HandBrake-%{commit0}


  # python2 substitutions
  sed -i -e '1c#! /usr/bin/python2' "gtk/src/makedeps.py"
  sed -i -e '1c#! /usr/bin/python2' "make/configure.py"

sed -i 's|-lx264 |-lx264 -lx265 |g' gtk/configure.ac
sed -i 's|x264 |x264 x265 |g' test/module.defs

# Use system libraries in place of bundled ones
for module in libdav1d libdvdnav libdvdread libbluray a52dec libvpx x265; do
    sed -i -e "/MODULES += contrib\/$module/d" make/include/main.defs
done

# Fix desktop file
sed -i -e 's/%{desktop_id}.svg/%{desktop_id}/g' gtk/src/%{desktop_id}.desktop

 find -type f -exec sed -iE '1s=^#! */usr/bin/\(python\|env python\)[23]\?=#!%{__python3}=' {} +


%build

echo "HASH=%{commit0}" > version.txt
echo "SHORTHASH=%{shortcommit0}" >> version.txt
echo "DATE=$(date "+%Y-%m-%d %T")" >> version.txt

# Not an autotools configure script.
mkdir build
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --force \
    --build=$PWD/build --debug=std \
    --disable-gtk-update-checks \
    --strip="/bin/true" \
    --optimize=speed \
    --enable-fdk-aac \
    --enable-nvenc \
    --enable-qsv

make -C build V=0



%install
%make_install -C build

# Desktop file, icons and AppStream metadata from FlatPak build (more complete)
rm -f %{buildroot}/%{_datadir}/applications/ghb.desktop \
    %{buildroot}/%{_datadir}/icons/hicolor/scalable/apps/hb-icon.svg

install -D -p -m 644 gtk/src/%{desktop_id}.desktop \
    %{buildroot}/%{_datadir}/applications/%{desktop_id}.desktop
install -D -p -m 644 gtk/src/%{desktop_id}.svg \
    %{buildroot}/%{_datadir}/icons/hicolor/scalable/apps/%{desktop_id}.svg

desktop-file-validate %{buildroot}/%{_datadir}/applications/%{desktop_id}.desktop

%find_lang ghb

%post gui
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
%if 0%{?fedora} <= 24 || 0%{?rhel}
/usr/bin/update-desktop-database &> /dev/null || :
%endif

%postun gui
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
%if 0%{?fedora} <= 24 || 0%{?rhel}
/usr/bin/update-desktop-database &> /dev/null || :
%endif

%posttrans gui
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f ghb.lang gui
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS.markdown NEWS.markdown README.markdown THANKS.markdown
%{_bindir}/ghb
%{_datadir}/applications/%{desktop_id}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{desktop_id}.svg
%{_datadir}/metainfo/*.xml

%files cli
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS.markdown NEWS.markdown README.markdown THANKS.markdown
%{_bindir}/HandBrakeCLI

%changelog

* Mon Oct 04 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.4.2-7 
- Updated to 1.4.2

* Mon Aug 23 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.4.1-7 
- Updated to 1.4.1

* Thu Aug 12 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.4.0-8  
- Rebuilt for x264

* Wed Jul 28 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.4.0-7  
- Updated to 1.4.0

* Tue May 11 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.3.3-14  
- Rebuilt  for x265

* Fri Apr 09 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.3.3-13  
- Rebuilt 

* Mon Nov 23 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.3.3-12  
- Rebuilt for x264

* Sun Nov 01 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.3.3-11  
- Rebuilt for libdvdread

* Mon Oct 05 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.3.3-10  
- Updated to current commit

* Sat Jul 04 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.3.3-8  
- Rebuilt for x264

* Tue Jun 23 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.3.3-7  
- Updated to 1.3.3

* Sat May 30 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.3.2-8  
- Rebuild for x265

* Thu May 07 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.3.2-7  
- Updated to 1.3.2

* Mon Feb 24 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.3.1-8  
- Rebuild for x265

* Thu Jan 09 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.3.1-7  
- Updated to 1.3.1-7 

* Mon Nov 11 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.3.0-8  
- Rebuild for x265

* Mon Nov 11 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.3.0-7  
- Updated to 1.3.0
- Github source commits

* Fri Aug 02 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.2.2-11  
- Rebuilt for x265

* Tue Jul 16 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.2.2-10.gitdf8c5f8  
- Rebuilt for x265

* Fri Mar 22 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.2.2-8.git4eb9f7b  
- Rebuilt for x264

* Mon Feb 25 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.2.2-7.git4eb9f7b  
- Updated to 1.2.2

* Tue Feb 19 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.2.1-7.git1bd13ba  
- Updated to 1.2.1

* Fri Feb 08 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.2.0-8.git1bd13ba  
- Rebuilt for x265

* Wed Dec 19 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.2.0-7.git1bd13ba  
- Updated to 1.2.0

* Fri Oct 12 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.1.2-5.git1bd13ba  
- Automatic Mass Rebuild

* Fri Oct 05 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.1.2-4.git1bd13ba  
- Automatic Mass Rebuild

* Thu Sep 06 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.1.2-3.git1bd13ba  
- Updated to 1.1.2

* Wed Jul 04 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.1.1-3.git1bd13ba  
- Enabled nvenc

* Mon Jun 18 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.1.1-2.git1bd13ba  
- Updated to 1.1.1

* Mon Jun 18 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.1.0-5.git49f21c9  
- Rebuild for libass

* Wed May 30 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.1.0-4.git49f21c9  
- Updated to current commit

* Sun May 27 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.1.0-3.gitb463d33  
- Automatic Mass Rebuild

* Sun Apr 08 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.1.0-2.gitb463d33  
- Updated to 1.1.0-2.gitb463d33 

* Sat Feb 24 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.0.7-7.git3f34585  
- Automatic Mass Rebuild

* Sun Jan 14 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.0.7-6.git3f34585  
- Changed to ffmpeg and fdk-aac bundle

* Wed Dec 06 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.0.7-5.git91ed34f  
- Automatic Mass Rebuild

* Thu Oct 05 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.0.7-4.git91ed34f  
- Automatic Mass Rebuild

* Sat Sep 30 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.0.7-3.git91ed34f  
- Automatic Mass Rebuild

* Thu May 25 2017 David Vásquez <davidjeremias82 AT gmail DOT com> - 1.0.7-2.git91ed34f
- Updated to 1.0.7-2.git91ed34f

* Sat Mar 18 2017 David Vásquez <davidjeremias82 AT gmail DOT com> - 1.0.3-2.20170102git5ecc600
- Rebuilt for libbluray

* Mon Feb 27 2017 David Vásquez <davidjeremias82 AT gmail DOT com> - 1.0.3-1.20170102git5ecc600
- Updated to 1.0.3-1.20170102git5ecc600

* Tue Jan 03 2017 Simone Caronni <negativo17@gmail.com> - 1.0.2-1.20170102git063446f
- Update to latest snapshot of the 1.0.x branch.

* Thu Dec 15 2016 Simone Caronni <negativo17@gmail.com> - 1.0-33.20161215gitd58a50a
- Udpate to latest snapshot.

* Thu Dec 01 2016 Simone Caronni <negativo17@gmail.com> - 1.0-32.20161129gitfac5e0e
- Update to latest snapshot.
- Add patches from Dominik Mierzejewski:
  * Allow use of unpatched libbluray.
  * Use system OpenCL headers.
  * Do not strip binaries.

* Fri Nov 18 2016 Simone Caronni <negativo17@gmail.com> - 1.0-31.20161116gitb9c5daa
- Update to latest snapshot.
- Use Flatpak desktop file, icon and AppStream metadata (more complete).

* Sat Oct 08 2016 Simone Caronni <negativo17@gmail.com> - 1.0-30.20161006git88807bb
- Fix date.
- Rebuild for fdk-aac update.

* Sat Oct 08 2016 Simone Caronni <negativo17@gmail.com> - 1.0-29.20160929git88807bb
- Require x265 hotfix.

* Sun Oct 02 2016 Simone Caronni <negativo17@gmail.com> - 1.0-28.20160929gitd398531
- Rebuild for x265 update.

* Sun Oct 02 2016 Simone Caronni <negativo17@gmail.com> - 1.0-27.20160929gitd398531
- Update to latest snapshot.
- Update package release according to package guidelines.
- Enable Intel Quick Sync Video encoding by default (libmfx package in main
  repositories).
- Add AppData support for Fedora (metadata from upstream).
- Do not run update-desktop-database on Fedora 25+ as per packaging guidelines.

* Fri Aug 05 2016 Simone Caronni <negativo17@gmail.com> - 1.0-26.6b5d91a
- Update to latest sources.

* Thu Jul 14 2016 Simone Caronni <negativo17@gmail.com> - 1.0-25.56c7ee7
- Update to latest snapshot.

* Fri Jul 08 2016 Simone Caronni <negativo17@gmail.com> - 1.0-24.0fc54d0
- Update to latest sources.

* Sun Jul 03 2016 Simone Caronni <negativo17@gmail.com> - 1.0-23.b1a4f0d
- Update to latest sources.

* Sun Jun 19 2016 Simone Caronni <negativo17@gmail.com> - 1.0-22.221bfe7
- Update to latest sources, bump build requirements.

* Tue May 24 2016 Simone Caronni <negativo17@gmail.com> - 1.0-21.879a512
- Update to latest sources.

* Wed Apr 13 2016 Simone Caronni <negativo17@gmail.com> - 1.0-20.8be786a
- Update to latest sources.
- Update build requirements of x264/x265 to match upstream.

* Thu Mar 31 2016 Simone Caronni <negativo17@gmail.com> - 1.0-19.a447656
- Bugfixes.

* Tue Mar 29 2016 Simone Caronni <negativo17@gmail.com> - 1.0-18.113e2a5
- Update to latest snapshot for various fixes.

* Wed Mar 16 2016 Simone Caronni <negativo17@gmail.com> - 1.0-17.12f7be2
- Update to latest sources.

* Fri Feb 12 2016 Simone Caronni <negativo17@gmail.com> - 1.0-16.0da688d
- Update to latest snapshot.

* Sun Jan 31 2016 Simone Caronni <negativo17@gmail.com> - 1.0-15.ba5eb77
- Update to latest snapshot.

* Fri Jan 22 2016 Simone Caronni <negativo17@gmail.com> - 1.0-14.08e7b54
- Update to latest sources, contains normalization fix.
- Make Intel QuickSync encoder suppport conditional at build time.

* Sat Jan 16 2016 Simone Caronni <negativo17@gmail.com> - 1.0-13.ed8c11e
- Update to latest sources.

* Fri Jan 08 2016 Simone Caronni <negativo17@gmail.com> - 1.0-12.ee1167e
- Update to latest sources.

* Wed Dec 23 2015 Simone Caronni <negativo17@gmail.com> - 1.0-11.1e56395
- Update sources. Intel Quick Sync hardware support can be built using the same
  library as FFMpeg. No frontend support yet.

* Mon Dec 21 2015 Simone Caronni <negativo17@gmail.com> - 1.0-10.57a9f48
- Update sources.

* Fri Dec 11 2015 Simone Caronni <negativo17@gmail.com> - 1.0-9.3443f6a
- Update to latest sources.

* Sun Dec 06 2015 Simone Caronni <negativo17@gmail.com> - 1.0-8.ca69335
- Update to latest sources.

* Tue Dec 01 2015 Simone Caronni <negativo17@gmail.com> - 1.0-7.46e641c
- Switch back to bundled libav 11 to fix subtitle detection.
- Make bundling libav conditional.

* Fri Nov 27 2015 Simone Caronni <negativo17@gmail.com> - 1.0-6.46e641c
- Update to latest sources.

* Mon Nov 23 2015 Simone Caronni <negativo17@gmail.com> - 1.0-5.6c731e1
- Update ffmpeg patch.

* Fri Nov 20 2015 Simone Caronni <negativo17@gmail.com> - 1.0-4.6c731e1
- Update to latest upstream.
- Add license macro.

* Sat Nov 14 2015 Simone Caronni <negativo17@gmail.com> - 1.0-3.6d66bd5
- Use system libfdk-aac.

* Tue Nov 10 2015 Simone Caronni <negativo17@gmail.com> - 1.0-2.6d66bd5
- Update snapshot.
- Use packaging guidelines for GitHub snapshots.
- Update fdk-aac bundle.
- Update build requirements.

* Wed Oct 28 2015 Simone Caronni <negativo17@gmail.com> - 1.0-1
- Update to master branch.
- Use system x265.

* Fri Oct 23 2015 Simone Caronni <negativo17@gmail.com> - 0.10.2-3
- Udpate patches from 0.10.x branch.
- Use system ffmpeg libraries in place of bundled libav.

* Mon Sep 28 2015 Simone Caronni <negativo17@gmail.com> - 0.10.2-2
- Update latest patches from the 0.10.x branch.

* Thu Jun 11 2015 Simone Caronni <negativo17@gmail.com> - 0.10.2-1
- Update to 0.10.2.
- Use handbrake.fr URL for source 0.

* Mon Mar 09 2015 Simone Caronni <negativo17@gmail.com> - 0.10.1-1
- Update to 0.10.1.

* Mon Jan 26 2015 Simone Caronni <negativo17@gmail.com> - 0.10.0-12
- Fix huge icons problem.

* Wed Nov 26 2014 Simone Caronni <negativo17@gmail.com> - 0.10.0-11
- Update to 0.10.0 official release.

* Wed Nov 05 2014 Simone Caronni <negativo17@gmail.com> - 0.10-10.svn6507
- Update to SVN revision 6507.

* Mon Nov 03 2014 Simone Caronni <negativo17@gmail.com> - 0.10-9.svn6502
- Update to SVN revision 6502.

* Fri Oct 24 2014 Simone Caronni <negativo17@gmail.com> - 0.10-8.svn6461
- Update to SVN revision 6461.

* Fri Oct 10 2014 Simone Caronni <negativo17@gmail.com> - 0.10-7.svn6439
- Update to SVN revision 6439.

* Fri Oct 03 2014 Simone Caronni <negativo17@gmail.com> - 0.10-6.svn6422
- Update to SVN revision 6430.

* Sun Sep 28 2014 Simone Caronni <negativo17@gmail.com> - 0.10-5.svn6422
- Update to SVN revision 6422.

* Mon Sep 08 2014 Simone Caronni <negativo17@gmail.com> - 0.10-4.svn6404
- Update to SVN revision 6404.
- Update libdvdread and libdvdnav requirements.

* Mon Sep 08 2014 Simone Caronni <negativo17@gmail.com> - 0.10-3.svn6394
- Update to SVN revision 6394.

* Mon Sep 01 2014 Simone Caronni <negativo17@gmail.com> - 0.10-2.svn6386
- Update to svn revision 6386; new x265 presets.
- Update x265 libraries.

* Sat Aug 23 2014 Simone Caronni <negativo17@gmail.com> - 0.9.9-17.svn6304
- Update to svn revision 6351. HandBrake version is now 0.10:
  https://trac.handbrake.fr/milestone/HandBrake%200.10
- Lame and x264 libraries are now linked by default.
- Remove mkv, mpeg2dec and libmkv as they are no longer used.
- LibAV is now enabled by default.
- Add libappindicator-gtk3 build requirement.

* Sun Aug 17 2014 Simone Caronni <negativo17@gmail.com> - 0.9.9-16.svn6304
- Update to 6304 snapshot.

* Wed Aug 06 2014 Simone Caronni <negativo17@gmail.com> - 0.9.9-15.svn6268
- Update to latest snapshot.

* Wed Jul 30 2014 Simone Caronni <negativo17@gmail.com> - 0.9.9-14.svn6244
- Updated to latest snapshot.
- Enable avformat muxer, replaces libmkv and mp4v2 support.
- Requires libdvdnav >= 5.0.0 to fix crashes.
- Remove ExclusiveArch.

* Sat Jul 05 2014 Simone Caronni <negativo17@gmail.com> - 0.9.9-13.svn6227
- Updated to SVN snapshot.
- Remove RHEL 6 conditionals.

* Tue Mar 25 2014 Simone Caronni <negativo17@gmail.com> - 0.9.9-12
- Backport DVD changes from trunk (should fix libdvdnav crashes with specific
  DVD titles).
- Use system ffpmeg 2 libraries in place of bundled libav.

* Mon Mar 17 2014 Simone Caronni <negativo17@gmail.com> - 0.9.9-11
- Fix crash on Fedora.

* Fri Mar 14 2014 Simone Caronni <negativo17@gmail.com> - 0.9.9-10
- Use system libdvdnav/libdvdread.

* Mon Dec 23 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-9
- Use system libraries for libbluray, lame, mpeg2dec, a52dec (patch), libmkv
 		 (patch), x264 (faac, fdk-aac, libav, libdvdnav, libdvdread and mp4v2 are still
  bundled).
- Use Fedora compiler options.
- Use GStreamer 1.x on Fedora and RHEL/CentOS 7.
- Add fdk-aac support.

* Mon Dec 23 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-8
- Scriptlets need to run for gui subpackage and not base package. Thanks to
  Peter Oliver.

* Mon Sep 09 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-7
- Add requirement on libdvdcss, fix hicolor-icon-theme requirement.

* Fri Jul 26 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-6
- Enable building CLI only on CentOS/RHEL 6.
- Disable GTK update checks (updates come only packaged).

* Tue Jul 23 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-5
- Enable command line interface only for CentOS/RHEL 6.

* Thu May 30 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-4
- Updated x264 to r2282-1db4621 (stable branch) to fix Fedora 19 crash issues.

* Mon May 20 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-3
- Update to 0.9.9.
- Separate GUI and CLI packages.

* Sat May 11 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-2.5449svn
- Updated.

* Wed May 01 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-1.5433svn
- First build.
