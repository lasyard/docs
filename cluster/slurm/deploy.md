# Slurm Deployment

## Prerequisites

If `AuthType=auth/munge` is set, `munge` is needed for authentication. See "<project:/service/munge.md>".

Since version 23.11, Slurm has its own authentication plugin. The option is `AuthType=auth/slurm`.

Install packages on each node according their roles. See "<project:install.md>".

## Configure

### Create slurm user & group

```console
$ sudo useradd -Mlrc "SLURM workload manager" -d /nonexistent -s /usr/sbin/nologin slurm
```

Find the IDs of group `slurm` and user `slurm`:

```console
$ getent group | grep slurm
slurm:x:998:
$ getent passwd | grep slurm
slurm:x:998:998:SLURM workload manager:/nonexistent:/usr/sbin/nologin
```

Add group & user `slurm` on other hosts (the IDs must be the same either using `auth/munge` or using `auth/slurm`):

```console
$ sudo groupadd -g998 slurm
$ sudo useradd -Mlrc "SLURM workload manager" -g slurm -u998 slurm
```

### Create configuration files

Create file `/etc/slurm/slurm.conf`:

:::{literalinclude} /_files/ubuntu/etc/slurm/slurm.conf
:language: ini
:::

:::{note}

- `MaxNodeCount` must be set for configless mode
- `SlurmdUser` (not `SlurmUser`) should be set to `root` (default), or `slurmd` cannot run properly
- If log file paths are not set, slurm will write logs to syslog
- `%h` in `SlurmdPidFile`, `SlurmdSpoolDir` and `SlurmdLogFile` is useful when these paths located in a storage shared by all computing node. Using `%n` is worse for it stand for "Node Name", and is not known at the start of `slurmd`
- The type of GPU must be a substring of the real GPU type, and empty string is not looked on as substring of any other strings

:::

:::{tip}
Online configuration generating tools are at <https://slurm.schedmd.com/configurator.html> and <https://slurm.schedmd.com/configurator.easy.html>.
:::

Create file `/etc/slurm/cgroup.conf`:

:::{literalinclude} /_files/ubuntu/etc/slurm/cgroup.conf
:language: ini
:::

If there is `GresTypes` configured (e.g. for GPU), you can create file `/etc/slurm/gres.conf`:

:::{literalinclude} /_files/ubuntu/etc/slurm/gres.conf
:language: ini
:::

To check if `Gres` can be dectected, you can do this on the computing node:

```console
$ slurmd -C
NodeName=las3 CPUs=8 Boards=1 SocketsPerBoard=8 CoresPerSocket=1 ThreadsPerCore=1 RealMemory=7935 Gres=gpu:nvidia_l40s:1
Found gpu:nvidia_l40s:1 with Autodetect=nvml (Substring of gpu name may be used instead)
UpTime=1-02:27:56
```

If your `slurmd` doesn't support `nvml`, `Autodetect=nvidia` will be used.

Do not forget to change the owners of the configuration files to `slurm`:

```console
$ sudo chown slurm:slurm /etc/slurm/*.conf
```

### Create key for authentication

```console
$ sudo dd if=/dev/random of=/etc/slurm/slurm.key bs=1024 count=1
1+0 records in
1+0 records out
1024 bytes (1.0 kB, 1.0 KiB) copied, 8.8143e-05 s, 11.6 MB/s
$ sudo chown slurm:slurm /etc/slurm/slurm.key
$ sudo chmod 600 /etc/slurm/slurm.key
```

The key must be distributed to every nodes in the cluster.

### Create directories

```console
$ sudo mkdir -p /var/spool/slurm && sudo chown slurm:slurm /var/spool/slurm
$ sudo mkdir -p /var/log/slurm && sudo chown slurm:slurm /var/log/slurm
```

### Configure slurmd

Because configless mode is enabled, `slurm.conf` is not needed on a computing node. In this case, `slurmd` must be started with `-Z --conf-server`. You can do this by:

```console
$ sudo systemctl edit --full slurmd
```

:::{literalinclude} /_files/ubuntu/etc/systemd/system/slurmd.service
:diff:  /_files/ubuntu/etc/systemd/system/slurmd.service.orig
:::

### Configure slurmdbd

`slurmdbd` can store data in [MySQL](project:/service/mysql.md) or [MariaDb](project:/service/mariadb.md). If MariaDb is used, create a file `/etc/msyql/conf.d/slurmdb.cnf` to set the recommended parameters:

:::{literalinclude} /_files/ubuntu/etc/mysql/conf.d/slurmdb.cnf
:language: ini
:::

Create user and grant previleges for `slurmdbd` in the mysql/mariadb database:

```sql
CREATE USER slurmdbd IDENTIFIED BY 'slurmdbd-password';
GRANT ALL on `slurm_acct_db`.* TO `slurmdbd`@`%`;
```

Create `slurmdbd` configuration file `/etc/slurm/slurmdbd.conf`:

:::{literalinclude} /_files/ubuntu/etc/slurm/slurmdbd.conf
:class: ini
:::

:::{note}
If `SlurmUser` is not set, slurmdbd will try to act as root.
:::

Set owner and modes of the configuration file:

```console
$ sudo chown slurm:slurm /etc/slurm/slurmdbd.conf
$ sudo chmod 0600 /etc/slurm/slurmdbd.conf
```

:::{important}
For the password of database is set in this file, no others should read the file except the owner.
:::

## JWT and REST API

Create JWT key:

```console
$ sudo dd if=/dev/random of=/etc/slurm/jwt_hs256.key bs=32 count=1
1+0 records in
1+0 records out
32 bytes copied, 7.6925e-05 s, 416 kB/s
$ sudo chown slurm:slurm /etc/slurm/jwt_hs256.key
$ sudo chmod 0600 /etc/slurm/jwt_hs256.key
```

Create user/group for `slurmrestd`:

```console
$ sudo useradd -Mlrc "SLURM REST API Server" -d /nonexistent -s /usr/sbin/nologin slurmrestd
$ getent group | grep slurmrestd
slurmrestd:x:997:
$ getent passwd | grep slurmrestd
slurmrestd:x:997:997:SLURM REST API Server:/nonexistent:/usr/sbin/nologin
```

Install `slurmrestd` first, then configure the service:

```console
$ sudo systemctl edit --full slurmrestd
```

:::{literalinclude} /_files/ubuntu/etc/systemd/system/slurmrestd.service
:diff: /_files/ubuntu/etc/systemd/system/slurmrestd.service.orig
:::

:::{note}
Service slurmrestd cannot be run as root or `SlurmUser`.
:::

## Run

Start services in the following order:

- `slurmdbd` if it is configured
- `slurmctld` on the controller node
- `slurmd` on the worker nodes
- `slurmrestd` if it is needed

Start them foreground if in containers, for example:

```console
$ sudo slurmctld -D
```

Check the version:

```console
$ sinfo -V
slurm 24.11.5
```

Check sluster status:

```console
$ sinfo
PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST
normal*      up   infinite      4   idle las[0-3]
high         up   infinite      4   idle las[0-3]
```
