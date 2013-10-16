Summary:	Python's own image processing library 
Name:		python-imaging
Version: 	1.1.7
Release: 	10
License:	MIT
Group:		Development/Python
URL:		http://www.pythonware.com/products/pil/
Source0:	http://effbot.org/downloads/Imaging-%{version}.tar.gz
Source1:	pil-handbook.pdf.bz2
Source2:	linux-python-paint-icon.gif
Patch0:		Imaging-1.1.7-link.patch
BuildRequires:	python-devel
BuildRequires:	python-pkg-resources
BuildRequires:	jpeg-devel
BuildRequires:	png-devel
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	lcms-devel
BuildRequires:	libsane-devel
BuildRequires:	tcl-devel
BuildRequires:	tk-devel
BuildRequires:	zlib-devel
BuildRequires:	tkinter

%description
Python Imaging Library version %{version}
   
The Python Imaging Library (PIL) adds image processing capabilities 
to your Python interpreter.

This library provides extensive file format support, an efficient
internal representation, and powerful image processing capabilities.

%package devel
Summary:	Header files for python-imaging
Group:		Development/C
Requires:	python-imaging = %{version}

%description devel
Header files for the Python Imaging Library version %{version}.

%prep
%setup -q -n Imaging-%{version}
%patch0 -p0
bzcat %SOURCE1 > pil-handbook.pdf

# fix tk version
# perl -p -i -e 's/8.3/8.4/g' Setup.in

# fix distutils problem
# %patch
# Make sure to get the right python library
# perl -pi -e "s,(\\\$\((exec_prefix|prefix|exec_installdir)\)|/usr/X11R6)/lib\b,\1/%{_lib},g" Makefile.pre.in Setup.in

# Nuke references to /usr/local
perl -pi -e "s,(-[IL]/usr/local/(include|lib)),,g" setup.py


%build
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" python setup.py build_ext -i
cd Sane
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" python setup.py build_ext -i

%install
find . -type f | xargs perl -pi -e 's@/usr/local/bin/python@/usr/bin/python@'

python setup.py install --root=%{buildroot}

cd libImaging
mkdir -p  %{buildroot}%{_includedir}/python%{py_ver}/
install -m 644 ImPlatform.h Imaging.h %{buildroot}%{_includedir}/python%{py_ver}/
cd ..

cd Sane
python setup.py install --root=%{buildroot}
cd ..

%files
%defattr (-,root,root)
%doc pil-handbook.pdf Scripts Images CHANGES* README
%{_bindir}/pil*.py
%py_platsitedir/PIL.pth
%dir %py_platsitedir/PIL
%py_platsitedir/PIL/*.egg-info
%py_platsitedir/PIL/*.py*
%py_platsitedir/PIL/_imaging.so
%py_platsitedir/PIL/_imagingcms.so
%py_platsitedir/PIL/_imagingft.so
%py_platsitedir/PIL/_imagingmath.so
%py_platsitedir/PIL/_imagingtk.so
%py_platsitedir/_sane.so
%py_platsitedir/*.egg-info
%py_platsitedir/sane.py*
%files devel
%defattr (-,root,root)
%{_includedir}/python%{py_ver}/Imaging.h
%{_includedir}/python%{py_ver}/ImPlatform.h



%changelog
* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 1.1.7-5mdv2011.0
+ Revision: 667938
- mass rebuild

* Tue Feb 15 2011 Eugeni Dodonov <eugeni@mandriva.com> 1.1.7-4
+ Revision: 637875
- Rebuild

  + Funda Wang <fwang@mandriva.org>
    - fix patch

* Sat Jan 01 2011 Funda Wang <fwang@mandriva.org> 1.1.7-3mdv2011.0
+ Revision: 626946
- add missing patch
- tighten BR

* Sat Oct 30 2010 Michael Scherer <misc@mandriva.org> 1.1.7-2mdv2011.0
+ Revision: 590388
- rebuild for python 2.7
- fix build on python 2.7 and clean redondant macros

* Wed Jan 20 2010 Frederik Himpe <fhimpe@mandriva.org> 1.1.7-1mdv2010.1
+ Revision: 494385
- Fix BuildRequires
- Update to new version 1.1.7

* Sun Jan 10 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1.6-8mdv2010.1
+ Revision: 488796
- rebuilt against libjpeg v8

* Mon Aug 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1.1.6-7mdv2010.0
+ Revision: 417196
- rebuilt against libjpeg v7

* Fri Dec 26 2008 Funda Wang <fwang@mandriva.org> 1.1.6-6mdv2009.1
+ Revision: 319437
- fix file list
- rebuild for new python

* Sat Dec 06 2008 Adam Williamson <awilliamson@mandriva.org> 1.1.6-5mdv2009.1
+ Revision: 311036
- rebuild for new tcl
- small cleanups

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 1.1.6-4mdv2009.0
+ Revision: 225132
- rebuild

* Mon Jan 28 2008 Marcelo Ricardo Leitner <mrl@mandriva.com> 1.1.6-3mdv2008.1
+ Revision: 159347
- Enabled support for Sane. Closes: #10890

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - buildrequires X11-devel instead of XFree86-devel

* Fri Oct 26 2007 GÃ¶tz Waschk <waschk@mandriva.org> 1.1.6-2mdv2008.1
+ Revision: 102332
- fix build of imagingtk extension (bug #34985)

* Wed May 02 2007 Adam Williamson <awilliamson@mandriva.org> 1.1.6-1mdv2008.0
+ Revision: 20635
- replace Icon: with Source: (thanks andreas)
- 1.1.6, drop some workarounds that are no longer needed


* Tue Nov 28 2006 GÃ¶tz Waschk <waschk@mandriva.org> 1.1.4-11mdv2007.0
+ Revision: 88169
- Import python-imaging

* Tue Nov 28 2006 Götz Waschk <waschk@mandriva.org> 1.1.4-11mdv2007.1
- update file list

* Sun Jan 01 2006 Oden Eriksson <oeriksson@mandriva.com> 1.1.4-10mdk
- rebuilt against soname aware deps (tcl/tk)
- fix deps

* Wed Mar 09 2005 Frederic Lepied <flepied@mandrakesoft.com> 1.1.4-9mdk
- install include files in a devel sub package

* Fri Dec 10 2004 Götz Waschk <waschk@linux-mandrake.com> 1.1.4-8mdk
- drop pilray support, this fixes bug 12347

* Sat Dec 04 2004 Michael Scherer <misc@mandrake.org> 1.1.4-7mdk
- Rebuild for new python

* Sat Sep 18 2004 Frederic Lepied <flepied@mandrakesoft.com> 1.1.4-6mdk
- add support for radiance pic format (bug #)

* Mon May 24 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.1.4-5mdk
- grf, fix buildrequires for real

* Sat May 22 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.1.4-4mdk
- fix buildrequires

* Tue Mar 02 2004 Götz Waschk <waschk@linux-mandrake.com> 1.1.4-3mdk
- fix build with new freetype2

