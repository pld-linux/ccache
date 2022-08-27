#
# Conditional build:
%bcond_without	redis		# Redis secondary storage support

Summary:	Compiler cache
Summary(pl.UTF-8):	Pamięć podręczna dla kompilatora
Summary(pt_BR.UTF-8):	Cache para compiladores C/C++
Name:		ccache
Version:	4.6.3
Release:	1
License:	GPL v3+
Group:		Development/Tools
Source0:	https://github.com/ccache/ccache/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	bcbce774b535db4576157c110144502e
URL:		https://ccache.dev/
BuildRequires:	asciidoc
BuildRequires:	cmake >= 3.10
%{?with_redis:BuildRequires:	hiredis-devel >= 0.13.3}
%ifarch %{arm}
BuildRequires:	libatomic-devel
%endif
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	rpmbuild(macros) >= 1.742
BuildRequires:	ruby-asciidoctor
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zstd-devel >= 1.1.2
%{?with_redis:Requires:	hiredis >= 0.13.3}
Requires:	zstd >= 1.1.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		pkglibexecdir	%{_libexecdir}/%{name}

%ifarch %{arm}
%define		archcflags	-DXXH_FORCE_MEMORY_ACCESS=1
%endif

%description
ccache is a compiler cache. It acts as a caching pre-processor to
C/C++ compilers, using the -E compiler switch and a hash to detect
when a compilation can be satisfied from cache. This often results in
a 5 to 10 times speedup in common compilations.

%description -l pl.UTF-8
ccache to pamięć podręczna dla kompilatora - działa jako cachujący
preprocesor dla kompilatorów C/C++, wykorzystujący opcję kompilatora
-E oraz tablicę haszującą do wykrywania, czy do kompilacji wystarczy
zawartość pamięci podręcznej. Daje to zazwyczaj przyspieszenie
kompilacji 5 do 10 razy.

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

%build
export CFLAGS="%{rpmcflags} %{?archcflags}"
%cmake -B build \
	-DUSE_CCACHE=OFF \
	-DUSE_FASTER_LINKER=OFF \
	%{cmake_on_off redis REDIS_STORAGE_BACKEND}

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/env.d

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{pkglibexecdir},/etc/profile.d}
%ifarch x32
target=x86_64-%{_target_vendor}-%{_target_os}-gnux32
%else
target=%{_target_cpu}-%{_target_vendor}-%{_target_os}
%endif
for cc in cc c++ g++ gcc $target-gcc $target-g++; do
	ln -s ../../bin/%{name} $RPM_BUILD_ROOT%{pkglibexecdir}/$cc
done
echo 'export PATH=%{pkglibexecdir}:$PATH' > \
	$RPM_BUILD_ROOT/etc/profile.d/%{name}.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.* README.md doc/{AUTHORS.*,MANUAL.*,NEWS.*}
%attr(755,root,root) %{_bindir}/ccache
%{_mandir}/man1/ccache.1*

%files wrapper
%defattr(644,root,root,755)
/etc/profile.d/%{name}.sh
%dir %{pkglibexecdir}
%attr(755,root,root) %{pkglibexecdir}/c++
%attr(755,root,root) %{pkglibexecdir}/cc
%attr(755,root,root) %{pkglibexecdir}/g++
%attr(755,root,root) %{pkglibexecdir}/gcc
%attr(755,root,root) %{pkglibexecdir}/*-g++
%attr(755,root,root) %{pkglibexecdir}/*-gcc
