# MPI

## Install

{{ for_ubuntu }}

```sh
sudo apt install mpi-default-dev
```

Show version of `mpicc`:

```sh
mpicc --version
```

`mpicc` is a wrapper of installed `gcc`, so the version output is the same as `gcc`:

:::{literalinclude} /_files/ubuntu/output/gcc/version.txt
:language: text
:class: cli-output
:::

Show version of `mpirun`:

```sh
mpirun --version
```

{.cli-output}

```text
mpirun (Open MPI) 4.1.2

Report bugs to http://www.open-mpi.org/community/help/
```

On worker nodes, only the runtime libraries need to be installed:

```sh
sudo apt install openmpi-common libopenmpi3 openmpi-bin
```

### Install from sources

To install the newest Open MPI, we need to build it from sources. Firstly, download the tarball of sources:

```sh
wget https://download.open-mpi.org/release/open-mpi/v5.0/openmpi-5.0.5.tar.bz2
```

```sh
tar -C ~/workspace/devel -xjf openmpi-5.0.5.tar.bz2
```

```sh
cd ~/workspace/devel
./configure
make
```

## Usage

### Compile sources

```sh
mpicc mpi_hello_world.c -o mpi_hello_world
```

### Run an executable

Run the executable directly will start up only one process.

Run it with:

```sh
mpirun ./mpi_hello_world
```

`N` processes will be started up, where `N` is the number of CPUs in local host.

Specify the number of processes:

```sh
mpirun -n 4 ./mpi_hello_world
```

If you want to run on other hosts, copy the executable to them:

```sh
scp ./mpi_hello_world worker-1:
```

:::{note}
The executable must be put to correct path where `ssh` can find, not the same path as on local host. Pass free login must be configured before running.
:::

Run on two hosts `master-1` and `worker-1` with 4 processes per host:

```sh
mpirun --host master-1:4 --host worker-1:4 ./mpi_hello_world
```

If the number of processes were missing, only one process is started on each host.

Use a host file:

```sh
mpirun --hostfile hostfile ./mpi_hello_world
```

The content of `hostfile`:

{.file-content}

```text
master-1 slots=4
worker-1 slots=4
```
