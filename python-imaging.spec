Summary:	Python's own image processing library 
Name:		python-imaging
Version:	5.0.0
Release:	3
License:	MIT
Group:		Development/Python
# Original:
#Url:		http://www.pythonware.com/products/pil/
#Source0:	http://effbot.org/downloads/Imaging-%{version}.tar.gz
# Much better maintained fork:
Url:		https://python-pillow.org
Source0:	https://pypi.python.org/packages/0f/57/25be1a4c2d487942c3ed360f6eee7f41c5b9196a09ca71c54d1a33c968d9/Pillow-%{version}.tar.gz
Source1:	pil-handbook.pdf.bz2
Source2:	linux-python-paint-icon.gif
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
%setup -qn Pillow-%{version}
%apply_patches
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
CFLAGS="%{optflags} -fno-strict-aliasing" python setup.py build_ext -i -lm,dl

%install
find . -type f | xargs perl -pi -e 's@/usr/local/bin/python@/usr/bin/python@'

PYTHONDONTWRITEBYTECODE=True python setup.py install --root=%{buildroot} build_ext -lm,dl

pushd src/libImaging
mkdir -p  %{buildroot}%{_includedir}/python%{py_ver}/
install -m 644 ImPlatform.h Imaging.h %{buildroot}%{_includedir}/python%{py_ver}/
popd

%files
%doc pil-handbook.pdf CHANGES*
%dir %{py_platsitedir}/PIL
%{py_platsitedir}/PIL/*.py*
%{py_platsitedir}/PIL/_imaging*.so
%{py_platsitedir}/PIL/_webp*.so
%{py_platsitedir}/*.egg-info

%files devel
%{_includedir}/python%{py_ver}/*.h
