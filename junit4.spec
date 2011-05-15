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

Name:           junit4
Version:        4.8.2
Release:        4
Summary:        Java regression test package
License:        CPL
URL:            http://www.junit.org/
Group:          Development/Java
# git clone --bare git://github.com/KentBeck/junit.git junit.git
# mkdir junit-4.8.2
# git --git-dir=junit.git --work-tree=junit-4.8.2 checkout r4.8.2
# tar cjf junit-4.8.2.tar.bz2 junit-4.8.2/
Source0:        junit-%{version}.tar.bz2
Requires(post): jpackage-utils >= 0:1.7.4
Requires(postun): jpackage-utils >= 0:1.7.4
Requires:       hamcrest
Requires:       java-1.6.0
BuildRequires:  ant
BuildRequires:  jpackage-utils >= 0:1.7.4
BuildRequires:  java-1.6.0-devel
BuildRequires:  hamcrest
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

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
Requires:       jpackage-utils

%description javadoc
Javadoc for %{name}.

%package demo
Group:          Development/Java
Summary:        Demos for %{name}
Requires:       %{name} = %{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

%prep
%setup -q -n junit-%{version}
find . -type f -name "*.jar" | xargs -t rm
ln -s $(build-classpath hamcrest/core) lib/hamcrest-core-1.1.jar
perl -pi -e 's/\r$//g' stylesheet.css

%build
export CLASSPATH=
export OPT_JAR_LIST=:
ant -Dant.build.javac.source=1.5 dist

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 junit%{version}/junit-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
pushd $RPM_BUILD_ROOT%{_javadir} 
ln -sf %{name}-%{version}.jar %{name}.jar
popd

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -m 644 pom.xml $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{name}.pom
%add_to_maven_depmap junit junit %{version} JPP %{name}

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr junit%{version}/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# demo
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/demo/junit # Not using %%name for last part because it is 
                                                                # part of package name
cp -pr junit%{version}/junit/* $RPM_BUILD_ROOT%{_datadir}/%{name}/demo/junit

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(0644,root,root,0755)
%doc cpl-v10.html README.html
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%{_datadir}/maven2/*
%{_mavendepmapfragdir}/*

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%files manual
%defattr(0644,root,root,0755)
%doc junit%{version}/doc/*

