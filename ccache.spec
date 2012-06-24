Summary:	Compiler cache
Summary(pl):	Przyspieszacz kompilowania
Summary(pt_BR):	Cache para compiladores C/C++
Name:		ccache
Version:	2.4
Release:	1
License:	GPL
Group:		Development/Tools
Source0:	http://ccache.samba.org/ftp/ccache/%{name}-%{version}.tar.gz
# Source0-md5:	73c1ed1e767c1752dd0f548ec1e66ce7
URL:		http://ccache.samba.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ccache is a compiler cache. It acts as a caching pre-processor to
C/C++ compilers, using the -E compiler switch and a hash to detect
when a compilation can be satisfied from cache. This often results in
a 5 to 10 times speedup in common compilations.

%description -l pl
ccache dzia�a jako cachuj�cy preprocesor dla kompilator�w C/C++. Przy
u�yciu opcji kompilatora -E oraz tablicy haszuj�cej do wykrywania, czy
do kompilacji wystarczy zawarto�� cache. Daje to zazwyczaj
przyspieszenie kompilacji 5 do 10 razy.

%description -l pt_BR
ccache � um cache para compiladores. Ele funciona mantendo um cache de
pr�-processamento para compiladores C/C++ utilizando-se do par�metro
- -E e de um hash para detectar quando uma compila��o pode ser
  reaproveitada de um cache armazenado em disco. O ganho de tempo em
  compila��es comuns pode chegar a uma escala de at� 10 vezes em rela��o
  ao tempo normal.

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
cp -f /usr/share/automake/config.* .
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -fr $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/ccache
%{_mandir}/man1/ccache*
