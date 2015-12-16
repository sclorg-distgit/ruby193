%global scl_name_base ruby
%global scl_name_version 193

%global scl %{scl_name_base}%{scl_name_version}
%scl_package %scl

# Do not produce empty debuginfo package.
%global debug_package %{nil}

%global install_scl 1

Summary: Package that installs %scl
Name: %scl_name
Version: 1.1
Release: 9.sc1%{?dist}
License: GPLv2+
Source0: README
Source1: LICENSE
%if 0%{?install_scl}
Requires: %{scl_prefix}rubygem-therubyracer
Requires: %{scl_prefix}rubygem-sqlite3
Requires: %{scl_prefix}rubygem-rails
Requires: %{scl_prefix}rubygem-sass-rails
Requires: %{scl_prefix}rubygem-coffee-rails
Requires: %{scl_prefix}rubygem-jquery-rails
Requires: %{scl_prefix}rubygem-uglifier
%endif
BuildRequires: help2man
BuildRequires: scl-utils-build

%description
This is the main package for %scl Software Collection.

%package runtime
Summary: Package that handles %scl Software Collection.
Requires: scl-utils
# Remove ruby193-libyaml from system.
# https://bugzilla.redhat.com/show_bug.cgi?id=1069105
Obsoletes: %{scl_prefix}libyaml <= 0.1.4-5%{?dist}
Obsoletes: %{scl_prefix}libyaml-devel <= 0.1.4-5%{?dist}

%description runtime
Package shipping essential scripts to work with %scl Software Collection.

%package build
Summary: Package shipping basic build configuration
Requires: scl-utils-build

%description build
Package shipping essential configuration macros to build %scl Software Collection.

%package scldevel
Summary: Package shipping development files for %scl

%description scldevel
Package shipping development files, especially usefull for development of
packages depending on %scl Software Collection.

%prep
%setup -T -c

# Expand macros used in README file.
cat > README << EOF
%{expand:%(cat %{SOURCE0})}
EOF

cp %{SOURCE1} .

%build
# Generate a helper script that will be used by help2man.
cat > h2m_help << 'EOF'
#!/bin/bash
[ "$1" == "--version" ] && echo "%{scl_name} %{version} Software Collection" || cat README
EOF
chmod a+x h2m_help

# Generate the man page from include.h2m and ./h2m_help --help output.
help2man -N --section 7 ./h2m_help -o %{scl_name}.7

%install
%scl_install

cat >> %{buildroot}%{_scl_scripts}/enable << EOF
export PATH=%{_bindir}\${PATH:+:\${PATH}}
export LD_LIBRARY_PATH=%{_libdir}\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}
export MANPATH=%{_mandir}:\${MANPATH}
export PKG_CONFIG_PATH=%{_libdir}/pkgconfig\${PKG_CONFIG_PATH:+:\${PKG_CONFIG_PATH}}
EOF

cat >> %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel << EOF
%%scl_%{scl_name_base} %{scl}
%%scl_prefix_%{scl_name_base} %{scl_prefix}
EOF

# Install generated man page.
mkdir -p %{buildroot}%{_mandir}/man7/
install -p -m 644 %{scl_name}.7 %{buildroot}%{_mandir}/man7/

%files

%files runtime
%doc README LICENSE
%scl_files
# Own the manual directories (rhbz#1080048, rhbz#1072319).
%dir %{_mandir}/man1
%dir %{_mandir}/man5
%dir %{_mandir}/man7
%dir %{_mandir}/man8
%{_mandir}/man7/%{scl_name}.*

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config

%files scldevel
%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel


%changelog
* Mon Mar 31 2014 Honza Horak <hhorak@redhat.com> - 1.1-9
- Fix path typo in README
  Related: #1061459

* Thu Mar 27 2014 Vít Ondruch <vondruch@redhat.com> - 1.1-8
- Own manual directories.
  Resolves: rhbz#1080048

* Thu Mar 20 2014 Josef Stribny <jstribny@redhat.com> - 1.1-7
- Require missing packages needed for the basic RoR app
  Resolves: rhbz#1074030

* Wed Feb 26 2014 Vít Ondruch <vondruch@redhat.com> - 1.1-6
- Obsolete ruby193-libyaml-devel as well.
  Related: rhbz#1069105

* Tue Feb 25 2014 Vít Ondruch <vondruch@redhat.com> - 1.1-5
- Obsolete ruby193-libyaml.
  Resolves: rhbz#1069105

* Wed Feb 12 2014 Honza Horak <hhorak@redhat.com> - 1.1-4
- Some more grammar fixes in README
  Related: #1061459

* Wed Feb 12 2014 Honza Horak <hhorak@redhat.com> - 1.1-3
- Fix grammar mistakes in README
  Related: #1061459

* Tue Feb 11 2014 Vít Ondruch <vondruch@redhat.com> - 1.1-2
- Do not produce empty debuginfo package.
  Related: rhbz#1061459

* Mon Feb 10 2014 Vít Ondruch <vondruch@redhat.com> - 1.1-1
- Bump version.
- Add -scldevel sub-package.
  Resolves: rhbz#1063297
- Add -build package dependency on scl-utils-build.
  Resolves: rhbz#1058615
- Add LICENSE, README and man page.
  Resolves: rhbz#1061459

* Mon Nov 11 2013 Vít Ondruch <vondruch@redhat.com> - 1-12
- Add setup macro, which is now mandatory (rhbz#912746).

* Thu May 23 2013 Vít Ondruch <vondruch@redhat.com> - 1-11
- Correctly replace man search path.
- Resolves: rhbz#966394

* Mon Apr 29 2013 Vít Ondruch <vondruch@redhat.com> - 1-10
- Properly expand empty variables (rhbz#957209).

* Thu Apr 25 2013 Vít Ondruch <vondruch@redhat.com> - 1-9
- Configure paths for pkg-config.

* Mon Apr 08 2013 Vít Ondruch <vondruch@redhat.com> - 1-8
- Fix for CVE-2013-1945 - insecure LD_LIBRARY_PATH (rhbz#949031).

* Wed Nov 14 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1-6
- Rebuilt for PPC.

* Thu Jul 26 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1-5
- Switched JS runtime engine to TheRubyRacer.

* Tue May 29 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1-4
- Properly override MANPATH.

* Thu Apr 26 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1-3
- Allow installing the whole scl with the ruby193 package.

* Tue Apr 24 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1-2
- Bump release to get the build on all architectures.

* Fri Mar 30 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1-1
- Initial package.
