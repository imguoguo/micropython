%global debug_package %{nil}
%global _hardened_build 1


Name:           micropython
Version:        1.9.4
Release:        1%{?dist}
Summary:        Implementation of Python 3 with very low memory footprint

# micorpython itself is MIT
# axtls and berkeley-db are BSD
License:        MIT and BSD

URL:            http://micropython.org/
Source0:        https://github.com/micropython/micropython/archive/v%{version}.tar.gz

%global axtls_commit 43a6e6bd3bbc03dc501e16b89fba0ef042ed3ea0
Source1:       https://github.com/pfalcon/axtls/archive/%{axtls_commit}/axtls-%{axtls_commit}.tar.gz

%global berkley_commit 35aaec4418ad78628a3b935885dd189d41ce779b
Source2:       https://github.com/pfalcon/berkeley-db-1.xx/archive/%{berkley_commit}/berkeley-db-1.xx-%{berkley_commit}.tar.gz

# Other arches need active porting
ExclusiveArch:  %{arm} x86_64

BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  libffi-devel
BuildRequires:  readline-devel
BuildRequires:  execstack
BuildRequires:  openssl-devel

# Part of the tests runs MicroPython and CPython and compares the results.
# MicroPython is ~3.4.
# In Python 3.7 however, StopIteration handling in generators changed
# and the results are no longer comparable.
# PEP 479: https://www.python.org/dev/peps/pep-0479/
# Upstream issue: https://github.com/micropython/micropython/issues/4000
# We use the latest working CPython version in those test, setting the
# MICROPY_CPYTHON3 environment variable.
# Normal %%{__pytohn3} is used anywhere else.
# There is no runtime dependency on this CPython (or any other).
%global cpython_version_tests 3.6
BuildRequires:  %{_bindir}/python%{cpython_version_tests}


Provides:       bundled(axtls)
Provides:       bundled(libdb) = 1.85

%description
Implementation of Python 3 with very low memory footprint

%prep
%setup -q -n %{name}-%{version}

# git submodules
rmdir lib/axtls
tar -xf %{SOURCE1}
mv axtls-%{axtls_commit} lib/axtls

head -n 28 lib/axtls/axtlswrap/Makefile > LICENSE.axtls

rmdir lib/berkeley-db-1.xx
tar -xf %{SOURCE2}
mv berkeley-db-1.xx-%{berkley_commit} lib/berkeley-db-1.xx

head -n 32 lib/berkeley-db-1.xx/db/db.c > LICENSE.libdb

# Fix shebangs
files=$(grep -rl '#!/usr/bin/env python')
pathfix.py -i %{__python3} -p $files

# Removing pre-built binary; not required for build
rm ports/cc3200/bootmgr/relocator/relocator.bin

%build
pushd ports/unix
make axtls V=1 %{?_smp_mflags}
make PYTHON=%{__python3} V=1 %{?_smp_mflags}
popd

execstack -c ports/unix/micropython

%check
pushd ports/unix
export MICROPY_CPYTHON3=python%{cpython_version_tests}
make PYTHON=%{__python3} V=1 test
popd

%install
mkdir -p %{buildroot}%{_bindir}
install -pm 755 ports/unix/micropython %{buildroot}%{_bindir}

%files
%doc README.md
%license LICENSE LICENSE.axtls LICENSE.libdb
%{_bindir}/micropython

%changelog
* Wed Aug 01 2018 Miro Hrončok <mhroncok@redhat.com> - 1.9.4-1
- Update to 1.9.4 (#1577187)
- Use CPython 3.6 in tests that compare results due to PEP479 (#1604827)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.9.3-5
- Rebuilt for Python 3.7

* Thu Mar 15 2018 Miro Hrončok <mhroncok@redhat.com> - 1.9.3-4
- Get rid of python2 build dependency
- Temporarily disable i686, investigate later

* Thu Mar 15 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.9.3-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 01 2017 Miro Hrončok <mhroncok@redhat.com> - 1.9.3-1
- Update to 1.9.3 (#1508424)

* Tue Sep 12 2017 Miro Hrončok <mhroncok@redhat.com> - 1.9.2-1
- Update to 1.9.2 (#1332739) and fix FTBFS (#1423943)
- Add 2 git submodules to sources, add bundled provides
- Changed license tag to include BSD (becasue of those submodules)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Aug 13 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.8.1-2
- Add ExclusiveArch, other arches need active porting

* Wed Jun 06 2016 John Dulaney <jdulaney@fedoraproject.org> - 1.8.1-1
- Update to 1.8.1

* Wed May 04 2016 John Dulaney <jdulaney@fedoraproject.org> - 1.8-1
- Update to 1.8

* Tue Apr 19 2016 John Dulaney <jdulaney@fedoraproject.org> - 1.7-1
- Update to 1.7

* Tue Apr 05 2016 John Dulaney <jdulaney@fedoraproject.org> - 1.6-3
- Remove license-encumbered bits in stmhal/

* Tue Apr 05 2016 John Dulaney <jdulaney@fedoraproject.org> - 1.6-2
- Remove cc3200/bootmgr/relocator/relocator.bin
- Fix license macro

* Tue Apr 05 2016 John Dulaney <jdulaney@fedoraproject.org> - 1.6-1
- Update to 1.6

* Tue May 20 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.2-1
- Initial spec
