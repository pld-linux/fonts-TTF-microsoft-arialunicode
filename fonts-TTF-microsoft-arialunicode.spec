#
# Conditional build:
%bcond_with	license_agreement	# generates package (may require MS Office license?)
#
%define		base_name		fonts-TTF-Microsoft-ArialUnicode
%define		rel			3
Summary:	Microsoft Arial Unicode TrueType font
Summary(pl.UTF-8):	Font TrueType Arial Unicode firmy Microsoft
%if %{with license_agreement}
Name:		%{base_name}
%else
Name:		%{base_name}-installer
%endif
Version:	1.0
Release:	%{rel}%{?with_license_agreement:wla}
# part of MS Office - may require Office license to use
License:	?
Group:		Fonts
%if %{with license_agreement}
# also at http://dl.sourceforge.net/corefonts/
Source0:	http://orwell.ru/download/aruniupd.exe
# NoSource0-md5: 1bef548eb449a0b24ad1c0b8e9d5f2ba
BuildRequires:	cabextract
Requires(post,postun):	fontpostinst
Requires:	%{_fontsdir}/TTF
%else
Source0:	http://svn.pld-linux.org/svn/license-installer/license-installer.sh
# Source0-md5:	329c25f457fea66ec502b7ef70cb9ede
Requires:	cabextract
Requires:	rpm-build-tools >= 4.4.37
Requires:	rpmbuild(macros) >= 1.544
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ttffontsdir	%{_fontsdir}/TTF

%description
Microsoft Arial Unicode TrueType font.
%if !%{with license_agreement}
License issues made us not to include inherent files into this package
by default (it probably requires MS Office license). If you want to
create full working package please build it with one of the following
command:

%{base_name}.install --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
%endif

%description -l pl.UTF-8
Font TrueType Arial Unicode firmy Microsoft.
%if !%{with license_agreement}
Kwestie licencji zmusiły nas do niedołączania do tego pakietu istotnych
plików (prawdopodobnie wymaga licencji na MS Office). Jeśli chcesz stworzyć
w pełni funkcjonalny pakiet, zbuduj go za pomocą polecenia:

%{base_name}.install --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
%endif

%prep
%if %{with license_agreement}
%setup -q -c -T
/usr/bin/cabextract -L %{SOURCE0}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if !%{with license_agreement}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{base_name}}

sed -e '
	s/@BASE_NAME@/%{base_name}/g
	s/@TARGET_CPU@/%{_target_cpu}/g
	s-@VERSION@-%{version}-g
	s-@RELEASE@-%{release}-g
	s,@SPECFILE@,%{_datadir}/%{base_name}/%{base_name}.spec,g
	s,@DATADIR@,%{_datadir}/%{base_name},g
' %{SOURCE0} > $RPM_BUILD_ROOT%{_bindir}/%{base_name}.install

install %{_specdir}/%{base_name}.spec $RPM_BUILD_ROOT%{_datadir}/%{base_name}

%else
install -d $RPM_BUILD_ROOT%{ttffontsdir}
install *.ttf $RPM_BUILD_ROOT%{ttffontsdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with license_agreement}
%post
fontpostinst TTF

%postun
fontpostinst TTF

%else
%post
echo "
License issues made us not to include inherent files into this package
by default (it probably requires Windows license). If you want to
create full working package please build it with the following command:

%{base_name}.install --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
"
%endif

%files
%defattr(644,root,root,755)
%if %{with license_agreement}
%{ttffontsdir}/*
%else
%attr(755,root,root) %{_bindir}/%{base_name}.install
%{_datadir}/%{base_name}
%endif
