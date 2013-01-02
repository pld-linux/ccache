Summary:	Compiler cache
Summary(pl.UTF-8):	Przyspieszacz kompilowania
Summary(pt_BR.UTF-8):	Cache para compiladores C/C++
Name:		ccache
Version:	3.1.8
Release:	2
License:	GPL v3
Group:		Development/Tools
Source0:	http://samba.org/ftp/ccache/%{name}-%{version}.tar.bz2
# Source0-md5:	0e0f25fb342dcb1196d9c2986a7323cf
Patch0:		%{name}-nohash_size_mtime.patch
URL:		http://ccache.samba.org/
BuildRequires:	automake
BuildRequires:	zlib-devel >= 1.2.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		%{_prefix}/%{_lib}/%{name}

%description
ccache is a compiler cache. It acts as a caching pre-processor to
C/C++ compilers, using the -E compiler switch and a hash to detect
when a compilation can be satisfied from cache. This often results in
a 5 to 10 times speedup in common compilations.

%description -l pl.UTF-8
ccache działa jako cachujący preprocesor dla kompilatorów C/C++. Przy
użyciu opcji kompilatora -E oraz tablicy haszującej do wykrywania, czy
do kompilacji wystarczy zawartość cache. Daje to zazwyczaj
przyspieszenie kompilacji 5 do 10 razy.

%description -l pt_BR.UTF-8
ccache é um cache para compiladores. Ele funciona mantendo um cache de
pré-processamento para compiladores C/C++ utilizando-se do parâmetro
- -E e de um hash para detectar quando uma compilação pode ser
  reaproveitada de um cache armazenado em disco. O ganho de tempo em
  compilações comuns pode chegar a uma escala de até 10 vezes em relação
  ao tempo normal.

%package wrapper
Summary:	Symlinks for c++/cc/g++/gcc
Summary(pl.UTF-8):	Dowiązania symboliczne do c++/cc/g++/gcc
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description wrapper
This package contains the softlinks to ccache for each compiler.

%description wrapper -l pl.UTF-8
Ten pakiet zawiera dowiązania symboliczne do ccache dla każdego
kompilatora.

%prep
%setup -q
%patch0 -p1

# Make sure system zlib is used
%{__rm} -r zlib

%build
cp -f /usr/share/automake/config.* .
CPPFLAGS="%{rpmcppflags} -D_FILE_OFFSET_BITS=64"
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
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.txt MANUAL.txt NEWS.txt README.txt
%attr(755,root,root) %{_bindir}/ccache
%{_mandir}/man1/ccache.1.*
%config(noreplace,missingok) %verify(not md5 mtime size) /etc/env.d/CCACHE_*

%files wrapper
%defattr(644,root,root,755)
%attr(755,root,root) /etc/profile.d/%{name}.sh
%dir %{_libdir}
%attr(755,root,root) %{_libdir}/*
