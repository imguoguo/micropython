%global debug_package %{nil}
%global _hardened_build 1


Name:           micropython
Version:        1.8.1
Release:        5%{?dist}
Summary:        Implementation of Python 3 with very low memory footprint
License:        MIT
URL:            http://micropython.org/
Source0:        https://github.com/micropython/micropython/archive/v%{version}.tar.gz

# Other arches need active porting
ExclusiveArch:  %{arm} %{ix86} x86_64

BuildRequires:  python-devel
BuildRequires:  python3-devel
BuildRequires:  libffi-devel
BuildRequires:  readline-devel
BuildRequires:  execstack
BuildRequires:  openssl-devel

%description
Implementation of Python 3 with very low memory footprint

%prep
%setup -q -n %{name}-%{version}

# Removing due to non-free license; not required for build
rm -r stmhal/

# Removing pre-built binary; not required for build
rm cc3200/bootmgr/relocator/relocator.bin

%build
make -C unix V=1

execstack -c unix/micropython

%check
pushd unix
make test
popd

%install
mkdir -p %{buildroot}%{_bindir}
install -pm 755 unix/micropython %{buildroot}%{_bindir}

%files
%doc README.md
%license LICENSE
%{_bindir}/micropython

%changelog
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
