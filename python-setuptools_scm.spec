#
# Conditional build:
%bcond_without	tests		# py.test tests
%bcond_with	tests_scm	# py.test tests using SCM programs (git, hg)

Summary:	Python 2 package to manager versions by scm tags
Summary(pl.UTF-8):	Pakiet Pythona 2 do zarządzania wersjami poprzez etykiety systemu kontroli wersji
Name:		python-setuptools_scm
Version:	5.0.2
Release:	5
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/setuptools_scm/
Source0:	https://files.pythonhosted.org/packages/source/s/setuptools_scm/setuptools_scm-%{version}.tar.gz
# Source0-md5:	8ddd44e0cd3a243350fe709024ec7224
URL:		https://github.com/pypa/setuptools_scm
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools >= 1:42
%if %{with tests}
BuildRequires:	python-py >= 1.4.26
BuildRequires:	python-pytest >= 3.1.0
BuildRequires:	python-toml
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with tests_scm}
BuildRequires:	git-core
BuildRequires:	mercurial
%endif
Requires:	python-setuptools
Requires:	python-toml
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
setuptools_scm is a simple utility for the setup_requires feature of
setuptools for use in Mercurial and Git based projects.

%description -l pl.UTF-8
setuptools_scm to proste narzędzie dla funkcji setup_requires modułu
setuptools przeznaczone do stosowania w projektach opatych na
systemach kontroli wersji Mercurial i Git.

%prep
%setup -q -n setuptools_scm-%{version}

%if %{without tests_scm}
%{__rm} testing/test_{file_finder,git,mercurial,regressions}.py
%endif

# tries to install using pip
%{__rm} testing/test_setuptools_support.py

%build
%py_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} -m pytest testing
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py_install

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst LICENSE README.rst
%{py_sitescriptdir}/setuptools_scm
%{py_sitescriptdir}/setuptools_scm-%{version}-py*.egg-info
