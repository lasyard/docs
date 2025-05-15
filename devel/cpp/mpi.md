# MPI

## Install

### By package manager

:::::{tabs}
::::{group-tab} Ubuntu 22.04

```console
$ sudo apt install mpi-default-dev
```

Show version of `mpicc`:

```console
$ mpicc -v
Using built-in specs.
COLLECT_GCC=/usr/bin/gcc
COLLECT_LTO_WRAPPER=/usr/lib/gcc/x86_64-linux-gnu/11/lto-wrapper
OFFLOAD_TARGET_NAMES=nvptx-none:amdgcn-amdhsa
OFFLOAD_TARGET_DEFAULT=1
Target: x86_64-linux-gnu
Configured with: ../src/configure -v --with-pkgversion='Ubuntu 11.4.0-1ubuntu1~22.04' --with-bugurl=file:///usr/share/doc/gcc-11/README.Bugs --enable-languages=c,ada,c++,go,brig,d,fortran,objc,obj-c++,m2 --prefix=/usr --with-gcc-major-version-only --program-suffix=-11 --program-prefix=x86_64-linux-gnu- --enable-shared --enable-linker-build-id --libexecdir=/usr/lib --without-included-gettext --enable-threads=posix --libdir=/usr/lib --enable-nls --enable-bootstrap --enable-clocale=gnu --enable-libstdcxx-debug --enable-libstdcxx-time=yes --with-default-libstdcxx-abi=new --enable-gnu-unique-object --disable-vtable-verify --enable-plugin --enable-default-pie --with-system-zlib --enable-libphobos-checking=release --with-target-system-zlib=auto --enable-objc-gc=auto --enable-multiarch --disable-werror --enable-cet --with-arch-32=i686 --with-abi=m64 --with-multilib-list=m32,m64,mx32 --enable-multilib --with-tune=generic --enable-offload-targets=nvptx-none=/build/gcc-11-XeT9lY/gcc-11-11.4.0/debian/tmp-nvptx/usr,amdgcn-amdhsa=/build/gcc-11-XeT9lY/gcc-11-11.4.0/debian/tmp-gcn/usr --without-cuda-driver --enable-checking=release --build=x86_64-linux-gnu --host=x86_64-linux-gnu --target=x86_64-linux-gnu --with-build-config=bootstrap-lto-lean --enable-link-serialization=2
Thread model: posix
Supported LTO compression algorithms: zlib zstd
gcc version 11.4.0 (Ubuntu 11.4.0-1ubuntu1~22.04)
```

Actually, `mpicc` is a wrapper of installed `gcc`, so the version output is the same as `gcc`.

Show version of `mpirun`:

```console
$ mpirun --version
mpirun (Open MPI) 4.1.2

Report bugs to http://www.open-mpi.org/community/help/
```

On worker nodes, only the runtime libraries need to be installed:

```console
$ sudo apt install openmpi-common libopenmpi3 openmpi-bin
```

::::
:::::

### Install from sources

To install the newest Open MPI, we need to build it from sources. Firstly, download the tarball of sources:

```console
$ curl -LO https://download.open-mpi.org/release/open-mpi/v5.0/openmpi-5.0.7.tar.bz2
$ md5sum openmpi-5.0.7.tar.bz2 
0529027472015810e5f0d749136ca0a3  openmpi-5.0.7.tar.bz2
```

:::::{tabs}
::::{group-tab} Ubuntu 22.04
:::{include} /_files/frags/toolchain/ubuntu_gcc_11.txt
:::
Compression is used to transfer data among hosts, so install `zlib` development files before building:

```console
$ sudo apt install zlib1g-dev
```

Extract and build:

```console
$ tar -C ~/workspace/devel -xjf openmpi-5.0.7.tar.bz2
$ cd ~/workspace/devel/openmpi-5.0.7
$ ./configure --with-pmix --with-cuda=/usr/local/cuda
...
Accelerators
-----------------------
CUDA support: yes
...
$ make -j
$ sudo make install
```

:::{note}
Configure with `--with-pmix` force to use internal PMIx, avoid mangling with the PMIx existing in the system.
:::

Check the version:

```console
$ mpirun --version
mpirun (Open MPI) 5.0.7

Report bugs to https://www.open-mpi.org/community/help/
```

Show full information about the installed Open MPI and PMIx:

```console
$ ompi_info 
                 Package: Open MPI ubuntu@las3 Distribution
                Open MPI: 5.0.7
  Open MPI repo revision: v5.0.7
   Open MPI release date: Feb 14, 2025
                 MPI API: 3.1.0
            Ident string: 5.0.7
                  Prefix: /usr/local
...
$ pmix_info 
                 Package: PMIx ubuntu@las2 Distribution
                    PMIX: 5.0.5
      PMIX repo revision: v5.0.5
       PMIX release date: Unreleased developer copy
           PMIX Standard: 4.2
       PMIX Standard ABI: Stable (0.0), Provisional (0.0)
                  Prefix: /usr/local
 Configured architecture: pmix.arch
...
```

::::
:::::

:::{tip}
If any of the new installed executables runs with error "symbol lookup" or "cannot find dynamic library", try refresh the `ld` cache with:

```console
$ sudo ldconfig
```

:::

## Usage

### Compile sources

See [GitHub](https://github.com/lasyard/coding/blob/main/cpp/mpi_hello_world.c) to get the example source file.

Compile it:

```console
$ mpicc mpi_hello_world.c -o mpi_hello_world
```

### Run an executable

#### Single host

Run the executable directly will start up only one process:

```console
$ ./mpi_hello_world 
Hello world from "las3", rank 0 of 1 processors
```

Run it with `mpirun`:

```console
$ mpirun ./mpi_hello_world 
Hello world from "las3", rank 7 of 8 processors
Hello world from "las3", rank 2 of 8 processors
Hello world from "las3", rank 3 of 8 processors
Hello world from "las3", rank 1 of 8 processors
Hello world from "las3", rank 0 of 8 processors
Hello world from "las3", rank 5 of 8 processors
Hello world from "las3", rank 4 of 8 processors
Hello world from "las3", rank 6 of 8 processors
```

`N` processes will be started up, where `N` is the number of CPU cores in local host.

Specify the number of processes:

```console
$ mpirun -n 4 ./mpi_hello_world
Hello world from "las3", rank 0 of 4 processors
Hello world from "las3", rank 2 of 4 processors
Hello world from "las3", rank 1 of 4 processors
Hello world from "las3", rank 3 of 4 processors
```

If the number specified exceeds the number of CPU cores:

```console
$ mpirun -n 16 ./mpi_hello_world 
--------------------------------------------------------------------------
There are not enough slots available in the system to satisfy the 16
slots that were requested by the application:

  ./mpi_hello_world

Either request fewer procs for your application, or make more slots
available for use.

A "slot" is the PRRTE term for an allocatable unit where we can
launch a process.  The number of slots available are defined by the
environment in which PRRTE processes are run:

  1. Hostfile, via "slots=N" clauses (N defaults to number of
     processor cores if not provided)
  2. The --host command line parameter, via a ":N" suffix on the
     hostname (N defaults to 1 if not provided)
  3. Resource manager (e.g., SLURM, PBS/Torque, LSF, etc.)
  4. If none of a hostfile, the --host command line parameter, or an
     RM is present, PRRTE defaults to the number of processor cores

In all the above cases, if you want PRRTE to default to the number
of hardware threads instead of the number of processor cores, use the
--use-hwthread-cpus option.

Alternatively, you can use the --map-by :OVERSUBSCRIBE option to ignore the
number of available slots when deciding the number of processes to
launch.
--------------------------------------------------------------------------
```

#### Multiple hosts

Make sure that every hosts involved have MPI installed. Copy the compiled executable to them, for example:

```console
$ scp ./mpi_hello_world las2:
$ scp ./mpi_hello_world las3:
```

:::{note}
The executable must be put to correct path where `ssh` can find, not the same path as on local host. Pass free login must be configured before running.
:::

Run on two hosts `las3` and `las2` with 4 processes per host:

```console
$ mpirun --host las2:4 --host las3:4 ./mpi_hello_world
Hello world from "las2", rank 2 of 8 processors
Hello world from "las2", rank 0 of 8 processors
Hello world from "las2", rank 1 of 8 processors
Hello world from "las2", rank 3 of 8 processors
Hello world from "las3", rank 5 of 8 processors
Hello world from "las3", rank 6 of 8 processors
Hello world from "las3", rank 4 of 8 processors
Hello world from "las3", rank 7 of 8 processors
```

If the number of processes were missing, only one process is started on each host.

You can write the hosts info into a file:

```text
las2 slots=4
las3 slots=4
```

Suppose the file name is `hostfile`, you can run the program with:

```console
$ mpirun --hostfile hostfile ./mpi_hello_world
Hello world from "las2", rank 2 of 8 processors
Hello world from "las2", rank 3 of 8 processors
Hello world from "las2", rank 0 of 8 processors
Hello world from "las2", rank 1 of 8 processors
Hello world from "las3", rank 4 of 8 processors
Hello world from "las3", rank 7 of 8 processors
Hello world from "las3", rank 5 of 8 processors
Hello world from "las3", rank 6 of 8 processors
```
