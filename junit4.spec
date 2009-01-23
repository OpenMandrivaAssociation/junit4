# Copyright (c) 2000-2008, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support        1

Name:           junit4
Version:        4.5
Release:        %mkrel 3.0.2
Epoch:          0
Summary:        Java regression test package
License:        CPL
Url:            http://www.junit.org/
Group:          Development/Java
Source0:        junit-4.5.tar.bz2
# steps to reproduce
# cvs -d:pserver:anonymous@junit.cvs.sourceforge.net:/cvsroot/junit login
# cvs -z3 -d:pserver:anonymous@junit.cvs.sourceforge.net:/cvsroot/junit export -r r44 junit
# mv junit junit-4.4
# tar czf junit-4.4.tar.gz junit-4.4/

# Source1:        junit4.4-build.xml
Source2:        junit-4.5.pom
BuildRequires:  ant
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  dos2unix
BuildRequires:  hamcrest
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
JUnit is a regression testing framework written by Erich Gamma and Kent Beck.
It is used by the developer who implements unit tests in Java. JUnit is Open
Source Software, released under the Common Public License Version 1.0 and
JUnit is Open Source Software, released under the IBM Public License and
hosted on SourceForge.

%package manual
Group:          Development/Java
Summary:        Manual for %{name}

%description manual
Documentation for %{name}.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%package demo
Group:          Development/Java
Summary:        Demos for %{name}
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

%prep
%setup -q -n junit-%{version}
%remove_java_binaries
ln -sf $(build-classpath hamcrest/core) lib/hamcrest-core-1.1.jar
#rm src/org/junit/tests/BothTest.java


%build
%{ant} dist

find -name \*.htm -o -name \*.html | xargs dos2unix

%install
%{__rm} -rf %{buildroot}

# jars
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a junit%{version}/junit-4.5.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)
# pom
install -d -m 755 %{buildroot}%{_datadir}/maven2/poms
install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/maven2/poms/JPP-%{name}.pom
%add_to_maven_depmap junit junit %{version} JPP %{name}
%add_to_maven_depmap junit junit4 %{version} JPP %{name}
# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a junit%{version}/javadoc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})
# demo
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}/demo/junit
%{__cp} -a junit%{version}/junit/* %{buildroot}%{_datadir}/%{name}/demo/junit

%{gcj_compile}

# fix end-of-line
%{__perl} -pi -e 's/\r$//g' README.html

for i in `find junit%{version}/doc -type f -name "*.htm*"`; do
    %{__perl} -pi -e 's/\r$//g' $i
done

for i in `find %{buildroot}%{_datadir}/%{name} -type f -name "*.java"`; do
    %{__perl} -pi -e 's/\r$//g' $i
done

%clean
%{__rm} -rf %{buildroot}

%post
%update_maven_depmap
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc README.html
%{_javadir}/*
%{_datadir}/maven2
%{_mavendepmapfragdir}
%{gcj_files}
%dir %{_datadir}/%{name}

%files manual
%defattr(0644,root,root,0755)
%doc junit%{version}/doc/*

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}/*
