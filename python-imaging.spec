%global debug_package %{nil}

Summary:	Python's own image processing library 
Name:		python-imaging
Version:	7.2.0
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

%if "%{_lib}" != "lib"
# Get rid of -L/usr/lib insanity
sed -i -e 's,/usr/lib,%{_libdir},g' setup.py
%endif

%build

%install
find . -type f | xargs perl -pi -e 's@/usr/local/bin/python@/usr/bin/python@'

CFLAGS="%{optflags} -fno-strict-aliasing" python setup.py build_ext -i -lm,dl
PYTHONDONTWRITEBYTECODE=True python setup.py install --root=%{buildroot} build_ext -lm,dl

cd src/libImaging
mkdir -p  %{buildroot}%{_includedir}/python%{py_ver}/
install -m 644 ImPlatform.h Imaging.h %{buildroot}%{_includedir}/python%{py_ver}/
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
