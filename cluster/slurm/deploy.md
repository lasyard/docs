# Slurm Deployment

{{ for_centos }}

{{ cluster_las }}

Roles of the nodes:

:Controller: las1
:Compute Nodes: las1, las2, las3

## Prerequisites

`munge` is needed for authentication. See "<project:../munge.md>".

## Install packages

Install packages on each node according their roles. See "<project:install.md>".

## Create User & group

```sh
group add slurm
useradd -m -c "SLURM workload manager" -d /var/lib/slurm -g slurm -s /bin/bash slurm
```

See IDs of group `slurm` and user `slurm`:

```sh
getent group | grep slurm
```

{.cli-output}

```text
slurm:x:1001:
```

```sh
getent passwd | grep slurm
```

{.cli-output}

```text
slurm:x:1001:1001:SLURM workload manager:/var/lib/slurm:/bin/bash
```

Add group & user `slurm` on other hosts (the IDs must be the same):

```sh
groupadd -g1001 slurm
useradd -m -c "SLURM workload manager" -d /var/lib/slurm -g slurm -s /bin/bash -u1001 slurm
```

## Edit configuration files

```sh
vi /etc/slurm/slurm.conf
```

:::{literalinclude} /_files/centos/etc/slurm/slurm.conf
:diff: /_files/centos/etc/slurm/slurm.conf.orig
:class: file-content
:::

:::{note}

- If log file paths are not set, slurm will write logs to syslog
- SlurmdUser should be set to `root`, or `slurmd` cannot run normally

:::

```sh
chown slurm:slurm /etc/slurm/slurm.conf
```

Copy `slurm.conf` to all nodes, including the client.

```sh
vi /etc/slurm/slurmdbd.conf
```

:::{literalinclude} /_files/centos/etc/slurm/slurmdbd.conf
:diff: /_files/centos/etc/slurm/slurmdbd.conf.orig
:class: file-content
:::

```sh
chown slurm:slurm /etc/slurm/slurmdbd.conf
chmod 0600 slurmdbd.conf
```

## Create necessary directories & files

```sh
# SlurmctldPidFile & SlurmdPidFile
mkdir -p /var/run/slurm/ && chown slurm:slurm /var/run/slurm
# StateSaveLocation
mkdir -p /var/spool/slurm/ctld && chown slurm:slurm /var/spool/slurm/ctld
# SlurmdSpoolDir
mkdir -p /var/spool/slurm/d && chown slurm:slurm /var/spool/slurm/d
# SlurmctldLogFile & SlurmdLogFile & SlurmSchedLogFile
mkdir -p /var/log/slurm && chown slurm:slurm /var/log/slurm
```

## JWT

Create key:

```sh
dd if=/dev/random of=/var/spool/slurm/ctld/jwt_hs256.key bs=32 count=1
chown slurm:slurm /var/spool/slurm/ctld/jwt_hs256.key
chmod 0600 /var/spool/slurm/ctld/jwt_hs256.key
```

## slurmrestd

```sh
systemctl edit --full slurmrestd
```

:::{literalinclude} /_files/centos/etc/systemd/system/slurmrestd.service
:diff: /_files/centos/etc/systemd/system/slurmrestd.service.orig
:class: file-content
:::

## Run

Start `slurmdbd` first if it is configured (for `slurmctld`):

```sh
systemctl enable slurmdbd --now
```

For controller nodes:

```sh
systemctl enable slurmctld --now
```

For compute nodes:

```sh
systemctl enable slurmd --now
```

Start them foreground if in containers, for example:

```sh
slurmctld -D
```

Check sluster status:

```sh
sinfo
```

:::{literalinclude} /_files/centos/output/sinfo/no_args.txt
:language: text
:class: cli-output
:::
