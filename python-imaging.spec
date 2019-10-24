%bcond_without python2

Summary:	Python's own image processing library 
Name:		python-imaging
Version:	6.2.1
Release:	1
License:	MIT
Group:		Development/Python
# Original:
#Url:		http://www.pythonware.com/products/pil/
#Source0:	http://effbot.org/downloads/Imaging-%{version}.tar.gz
# Much better maintained fork:
Url:		https://python-pillow.org
Source0:	https://github.com/python-pillow/Pillow/archive/%{version}.tar.gz
Source1:	pil-handbook.pdf.bz2
Source2:	linux-python-paint-icon.gif
Patch0:		pillow-6.1.0-no-Lusrlib.patch
Provides:	python-pillow = %{EVRD}
BuildRequires:	python-pkg-resources
BuildRequires:	python-setuptools
BuildRequires:	tkinter
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(sane-backends)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(tcl)
BuildRequires:	pkgconfig(tk)
BuildRequires:	pkgconfig(zlib)

%if %{with python2}
BuildRequires:	python2-pkg-resources
BuildRequires:	python2-setuptools
BuildRequires:	pkgconfig(python2)
%endif

%description
Python Imaging Library version %{version}

The Python Imaging Library (PIL) adds image processing capabilities 
to your Python interpreter.

This library provides extensive file format support, an efficient
internal representation, and powerful image processing capabilities.

%package devel
Summary:	Header files for python-imaging
Group:		Development/C
Requires:	python-imaging = %{EVRD}
Provides:	python-pillow-devel = %{EVRD}

%description devel
Header files for the Python Imaging Library version %{version}.

%if %{with python2}
%package -n python2-imaging
Summary:	Python 2.x's own image processing library 
Group:		Development/Python
Provides:	python2-pillow = %{EVRD}

%description -n python2-imaging
Python Imaging Library version %{version}

The Python Imaging Library (PIL) adds image processing capabilities 
to your Python interpreter.

This library provides extensive file format support, an efficient
internal representation, and powerful image processing capabilities.

%package -n python2-imaging-devel
Summary:	Header files for python-imaging
Group:		Development/C
Requires:	python2-imaging = %{EVRD}
Provides:	python2-pillow-devel = %{EVRD}

%description -n python2-imaging-devel
Header files for the Python 2.x Imaging Library version %{version}.
%endif

%prep
%autosetup -p1 -n Pillow-%{version}
bzcat %SOURCE1 > pil-handbook.pdf

# fix tk version
# perl -p -i -e 's/8.3/8.4/g' Setup.in

# fix distutils problem
# #patch
# Make sure to get the right python library
# perl -pi -e "s,(\\\$\((exec_prefix|prefix|exec_installdir)\)|/usr/X11R6)/lib\b,\1/%{_lib},g" Makefile.pre.in Setup.in

# Nuke references to /usr/local
perl -pi -e "s,(-[IL]/usr/local/(include|lib)),,g" setup.py

%build

%install
find . -type f | xargs perl -pi -e 's@/usr/local/bin/python@/usr/bin/python@'

%if %{with python2}
CFLAGS="%{optflags} -fno-strict-aliasing" python2 setup.py build_ext -i -lm,dl
PYTHONDONTWRITEBYTECODE=True python2 setup.py install --root=%{buildroot} build_ext -lm,dl
%endif

CFLAGS="%{optflags} -fno-strict-aliasing" python setup.py build_ext -i -lm,dl
PYTHONDONTWRITEBYTECODE=True python setup.py install --root=%{buildroot} build_ext -lm,dl

cd src/libImaging
mkdir -p  %{buildroot}%{_includedir}/python%{py_ver}/
install -m 644 ImPlatform.h Imaging.h %{buildroot}%{_includedir}/python%{py_ver}/
%if %{with python2}
mkdir -p  %{buildroot}%{_includedir}/python2.7/
install -m 644 ImPlatform.h Imaging.h %{buildroot}%{_includedir}/python2.7/
%endif
cd -

%files
%doc pil-handbook.pdf CHANGES*
%dir %{py_platsitedir}/PIL
%{py_platsitedir}/PIL/*.py*
%{py_platsitedir}/PIL/_imaging*.so
%{py_platsitedir}/PIL/_webp*.so
%{py_platsitedir}/*.egg-info
%{py_platsitedir}/PIL/__pycache__/*.pyc

%files devel
%{_includedir}/python%{py_ver}/*.h

%files -n python2-imaging
%dir %{py2_platsitedir}/PIL
%{py2_platsitedir}/PIL/*.py*
%{py2_platsitedir}/PIL/_imaging*.so
%{py2_platsitedir}/PIL/_webp*.so
%{py2_platsitedir}/*.egg-info

%files -n python2-imaging-devel
%{_includedir}/python2*/*.h
