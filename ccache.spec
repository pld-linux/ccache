Name:		ccache
Summary:	compiler cache
Summary(pl):	przyspieszacz kompilowania 
Url:		http://ccache.samba.org/
Version:	1.8
Release:	1
License:	GPL
Group:		Development/Tools
Source0:	http://ccache.samba.org/ftp/ccache/%{name}-%{version}.tar.gz
BuildRoot:      %{tmpdir}/%{name}-%{version}-root-%(id -u -n)
%description
ccache is a compiler cache. It acts as a caching pre-processor to
C/C++ compilers, using the -E compiler switch and a hash to detect
when a compilation can be satisfied from cache. This often results in
a 5 to 10 times speedup in common compilations.

%description -l pl 

%prep
%setup -q -n ccache-1.8

%build
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d  $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}
install   ccache $RPM_BUILD_ROOT%{_bindir}
install   ccache.1 $RPM_BUILD_ROOT%{_mandir}/man1

gzip -9nf README

%clean
rm -fr $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ccache
%{_mandir}/man1/ccache*
%doc *.gz
