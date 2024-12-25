# Slurm Deployment

::::{plat} centos
{{ cluster_las }}

Roles of the nodes:

:Controller: las0
:Compute Nodes: las0, las1, las2

## Prerequisites

`munge` is needed for authentication. See "<project:/service/munge.md>".

Install packages on each node according their roles. See "<project:install.md>".

## Create User & group

```sh
sudo useradd -Mlrc "SLURM workload manager" slurm
```

See IDs of group `slurm` and user `slurm`:

```console
$ getent group | grep slurm
slurm:x:981:
$ getent passwd | grep slurm
slurm:x:988:981:SLURM workload manager:/home/slurm:/bin/bash
```

Add group & user `slurm` on other hosts (the IDs must be the same):

```sh
sudo groupadd -g981 slurm
sudo useradd -Mlrc "SLURM workload manager" -g slurm -u988 slurm
```

## Edit configuration files

Go <https://slurm.schedmd.com/configurator.easy.html> to get a default `slurm.conf` file. Then edit it:

```sh
sudo vi /etc/slurm/slurm.conf
```

:::{literalinclude} /_files/centos/etc/slurm/slurm.conf
:diff: /_files/centos/etc/slurm/slurm.conf.orig
:class: file-content
:::

:::{note}

- `MaxNodeCount` must be set for configless mode
- `SlurmdUser` should be set to `root` (default), or slurmd cannot run normally
- If log file paths are not set, slurm will write logs to syslog
- `%h` in `SlurmdPidFile`, `SlurmdSpoolDir` and `SlurmdLogFile` is useful when these paths located in a storage shared by all slurmd node. Using `%n` is worse for it stand for "Node Name", and is not known at the start of slurmd

:::

Change the owner of configuration file:

```sh
sudo chown slurm:slurm -R /etc/slurm/slurm.conf
```

Because configless mode is enabled, `slurm.conf` is not needed on a `slurmd` only node. In this case, `slurmd` must be started with `-Z --conf-server`. You can do this by:

```sh
sudo systemctl edit --full slurmd
```

:::{literalinclude} /_files/centos/etc/systemd/system/slurmd.service
:diff:  /_files/centos/etc/systemd/system/slurmd.service.orig
:class: file-content
:::

Create slurmdbd configuration file:

```sh
sudo vi /etc/slurm/slurmdbd.conf
```

:::{literalinclude} /_files/centos/etc/slurm/slurmdbd.conf
:class: file-content
:::

:::{note}
If `SlurmUser` is not set, slurmdbd will try to act as root.
:::

```sh
sudo chown slurm:slurm /etc/slurm/slurmdbd.conf
# required because there is password in this file
sudo chmod 0600 /etc/slurm/slurmdbd.conf
```

## Create directories & files

```sh
# PidFile
sudo mkdir -p /var/run/slurm && sudo chown slurm:slurm /var/run/slurm
# StateSaveLocation & SlurmdSpoolDir
sudo mkdir -p /var/spool/slurm/ctld && sudo chown slurm:slurm /var/spool/slurm/ctld
# SlurmctldLogFile & SlurmdLogFile & SlurmSchedLogFile
sudo mkdir -p /var/log/slurm && sudo chown slurm:slurm /var/log/slurm
```

## JWT

Create key:

```sh
sudo dd if=/dev/random of=/var/spool/slurm/ctld/jwt_hs256.key bs=32 count=1
sudo chown slurm:slurm /var/spool/slurm/ctld/jwt_hs256.key
sudo chmod 0600 /var/spool/slurm/ctld/jwt_hs256.key
```

## slurmrestd

```sh
sudo systemctl edit --full slurmrestd
```

:::{literalinclude} /_files/centos/etc/systemd/system/slurmrestd.service
:diff: /_files/centos/etc/systemd/system/slurmrestd.service.orig
:class: file-content
:::

:::{note}
Service slurmrestd cannot be run as root or `SlurmUser`.
:::

## Run

Start `slurmdbd` first if it is configured (for `slurmctld`):

```sh
sudo systemctl enable slurmdbd --now
```

::::{tip}
Before start `slurmdbd`, create user and grant previleges for `slurmdbd` in the mysql/mariadb database:

```sql
CREATE USER slurmdbd IDENTIFIED BY 'slurmdbd-password';
GRANT ALL on `slurm_acct_db`.* TO `slurmdbd`@`%`;
```

Set mysql/mariadb conf to fullfill slurmdbd's recommendation:

```sh
sudo vi /etc/msyql/conf.d/slurmdb.cnf
```

:::{literalinclude} /_files/centos/etc/msyql/conf.d/slurmdb.cnf
:language: ini
:class: file-content
:::
::::

For controller nodes:

```sh
sudo systemctl enable slurmctld --now
```

For compute nodes:

```sh
sudo systemctl enable slurmd --now
```

Start them foreground if in containers, for example:

```sh
sudo slurmctld -D
```

Check the version:

```console
$ sinfo -V
slurm 24.11.0
```

Check sluster status:

:::{literalinclude} /_files/centos/console/sinfo/no_args.txt
:language: console
:::
