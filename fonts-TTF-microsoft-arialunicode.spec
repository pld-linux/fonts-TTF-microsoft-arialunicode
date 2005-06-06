#
# Conditional build:
%bcond_with	license_agreement	# generates package (may require MS Office license?)
#
Summary:	Microsoft Arial Unicode True Type font
Summary(pl):	Font True Type Arial Unicode firmy Microsoft
%define		base_name		fonts-TTF-Microsoft-ArialUnicode
%if %{with license_agreement}
Name:		%{base_name}
%else
Name:		%{base_name}-installer
%endif
Version:	1.0
Release:	1%{?with_license_agreement:wla}
# part of MS Office - may require Office license to use
License:	?
Group:		Fonts
%if %{with license_agreement}
# also at http://dl.sourceforge.net/corefonts/
Source0:	http://orwell.ru/download/aruniupd.exe
# NoSource0-md5: 1bef548eb449a0b24ad1c0b8e9d5f2ba
BuildRequires:	cabextract
Requires:	%{_fontsdir}/TTF
Requires(post,postun):	fontpostinst
%else
Requires:	cabextract
Requires:	rpm-build-tools
Requires:	wget
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ttffontsdir	%{_fontsdir}/TTF

%description
Microsoft Arial Unicode True Type font.
%if ! %{with license_agreement}
License issues made us not to include inherent files into this package
by default (it probably requires MS Office license). If you want to
create full working package please build it with one of the following
command:

%{base_name}.install --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
%{base_name}.install --with license_agreement ftp://ftp.pld-linux.org/dists/ac/PLD/<your_arch>/PLD/RPMS/%{base_name}-{version}-{release}.src.rpm
%endif

%description -l pl
Font True Type Arial Unicode firmy Microsoft.
%if ! %{with license_agreement}
Kwestie licencji zmusi³y nas do niedo³±czania do tego pakietu istotnych
plików (prawdopodobnie wymaga licencji na MS Office). Je¶li chcesz stworzyæ
w pe³ni funkcjonalny pakiet, zbuduj go za pomoc± polecenia:

%{base_name}.install --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
%{base_name}.install --with license_agreement ftp://ftp.pld-linux.org/dists/ac/PLD/<your_arch>/PLD/RPMS/%{base_name}-{version}-{release}.src.rpm
%endif

%prep
%if %{with license_agreement}
%setup -q -c -T
/usr/bin/cabextract -L %{SOURCE0}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if ! %{with license_agreement}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{base_name}}

cat <<'EOF' >$RPM_BUILD_ROOT%{_bindir}/%{base_name}.install
#!/bin/sh
if [ "$1" = "--with" -a "$2" = "license_agreement" ]
then
	TMPDIR=`rpm --eval "%%{tmpdir}"`; export TMPDIR
	SPECDIR=`rpm --eval "%%{_specdir}"`; export SPECDIR
	SRPMDIR=`rpm --eval "%%{_srcrpmdir}"`; export SRPMDIR
	SOURCEDIR=`rpm --eval "%%{_sourcedir}"`; export SOURCEDIR
	BUILDDIR=`rpm --eval "%%{_builddir}"`; export BUILDDIR
	RPMDIR=`rpm --eval "%%{_rpmdir}"`; export RPMDIR
	BACKUP_SPEC=0
	mkdir -p $TMPDIR $SPECDIR $SRPMDIR $RPMDIR $SRPMDIR $SOURCEDIR $BUILDDIR
	if [ -f $SPECDIR/%{base_name}.spec ]; then
		BACKUP_SPEC=1
		mv -f $SPECDIR/%{base_name}.spec $SPECDIR/%{base_name}.spec.prev
	fi
	if echo "$3" | grep '\.src\.rpm$' >/dev/null; then
		( cd $SRPMDIR
		if echo "$3" | grep '://' >/dev/null; then
			wget --passive-ftp -t0 "$3"
		else
			cp -f "$3" .
		fi
		rpm2cpio `basename "$3"` | ( cd $TMPDIR; cpio -i %{base_name}.spec ) )
		if ! cp -i $TMPDIR/%{base_name}.spec $SPECDIR/%{base_name}.spec; then
			exit 1
		fi
	else
		if ! cp -i "$3" $SPECDIR; then
			exit 1
		fi
	fi
	( cd $SPECDIR
	%{_bindir}/builder -nc -ncs --with license_agreement --opts --target=%{_target_cpu} %{base_name}.spec
	if [ "$?" -ne 0 ]; then
		exit 2
	fi
	RPMNAME=%{base_name}-%{version}-%{release}wla.noarch.rpm
	rpm -U $RPMDIR/$RPMNAME || \
		echo -e "Install manually the file:\n   $RPMDIR/$RPMNAME" )
	if [ "$BACKUP_SPEC" -eq 1 ]; then
		mv -f $SPECDIR/%{base_name}.spec.prev $SPECDIR/%{base_name}.spec
	fi
else
	cat %{_datadir}/%{base_name}/Microsot-EULA.txt
	echo "
License issues made us not to include inherent files into this package
by default (it probably requires Windows license). If you want to
create full working package please build it with the following command:

$0 --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
"
fi
EOF

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
%pre
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
