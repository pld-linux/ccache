Summary:	Compiler cache
Summary(pl):	Przyspieszacz kompilowania
Summary(pt_BR):	Cache para compiladores C/C++
Name:		ccache
Version:	2.4
Release:	1.4
License:	GPL
Group:		Development/Tools
Source0:	http://ccache.samba.org/ftp/ccache/%{name}-%{version}.tar.gz
# Source0-md5:	73c1ed1e767c1752dd0f548ec1e66ce7
Patch0:		%{name}-nohash_size_mtime.patch
URL:		http://ccache.samba.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		%{_prefix}/%{_lib}/%{name}

%description
ccache is a compiler cache. It acts as a caching pre-processor to
C/C++ compilers, using the -E compiler switch and a hash to detect
when a compilation can be satisfied from cache. This often results in
a 5 to 10 times speedup in common compilations.

%description -l pl
ccache dzia³a jako cachuj±cy preprocesor dla kompilatorów C/C++. Przy
u¿yciu opcji kompilatora -E oraz tablicy haszuj±cej do wykrywania, czy
do kompilacji wystarczy zawarto¶æ cache. Daje to zazwyczaj
przyspieszenie kompilacji 5 do 10 razy.

%description -l pt_BR
ccache é um cache para compiladores. Ele funciona mantendo um cache de
pré-processamento para compiladores C/C++ utilizando-se do parâmetro
- -E e de um hash para detectar quando uma compilação pode ser
  reaproveitada de um cache armazenado em disco. O ganho de tempo em
  compilações comuns pode chegar a uma escala de até 10 vezes em relação
  ao tempo normal.

%package wrapper
Summary:	Symlinks for c++/cc/g++/gcc
Summary(pl):	Dowi±zania symboliczne do c++/cc/g++/gcc
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description wrapper
This package contains the softlinks to ccache for each compiler.

%description wrapper -l pl
Ten pakiet zawiera dowi±zania symboliczne do ccache dla ka¿dego
kompilatora.

%prep
%setup -q
%patch0 -p0

%build
%{__aclocal}
%{__autoconf}
cp -f /usr/share/automake/config.* .
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/env.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

for X in CCACHE_DIR CCACHE_TEMPDIR CCACHE_LOGFILE CCACHE_PATH CCACHE_CC CCACHE_PREFIX \
	CCACHE_DISABLE CCACHE_READONLY CCACHE_CPP2 CCACHE_NOSTATS CCACHE_NLEVELS \
	CCACHE_HARDLINK CCACHE_RECACHE CCACHE_UMASK CCACHE_HASHDIR CCACHE_UNIFY \
	CCACHE_EXTENSION CCACHE_NOHASH_SIZE_MTIME
do
	echo "#${X}=\"\"" > $RPM_BUILD_ROOT/etc/env.d/${X}
done

install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},/etc/profile.d}
for cc in cc c++ g++ gcc %{_target_cpu}-pld-linux-gcc %{_target_cpu}-pld-linux-g++; do
	ln -s ../../bin/%{name} $RPM_BUILD_ROOT%{_libdir}/$cc
done
echo 'export PATH=%{_libdir}:$PATH' > \
	$RPM_BUILD_ROOT/etc/profile.d/%{name}.sh

%clean
rm -fr $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/ccache
%{_mandir}/man1/ccache*
%attr(644,root,root) %config(noreplace,missingok) %verify(not md5 size mtime) /etc/env.d/*

%files wrapper
%defattr(644,root,root,755)
%attr(755,root,root) /etc/profile.d/%{name}.sh
%dir %{_libdir}
%attr(755,root,root) %{_libdir}/*
