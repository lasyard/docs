# Slurm Deployment

::::{plat} centos
{{ cluster_las }}

Roles of the nodes:

:Controller: las1
:Compute Nodes: las1, las2, las3

## Prerequisites

`munge` is needed for authentication. See "<project:../munge.md>".

Install packages on each node according their roles. See "<project:install.md>".

## Create User & group

```sh
sudo useradd -Mlrc "SLURM workload manager" slurm
```

See IDs of group `slurm` and user `slurm`:

```sh
getent group | grep slurm
```

{.cli-output}

```text
slurm:x:980:
```

```sh
getent passwd | grep slurm
```

{.cli-output}

```text
slurm:x:987:980:SLURM workload manager:/home/slurm:/bin/bash
```

Add group & user `slurm` on other hosts (the IDs must be the same):

```sh
sudo groupadd -g980 slurm
sudo useradd -Mlrc "SLURM workload manager" -g slurm -u987 slurm
```

## Edit configuration files

```sh
sudo vi /etc/slurm/slurm.conf
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
sudo chown slurm:slurm /etc/slurm/slurm.conf
```

Copy `slurm.conf` to all nodes, including the client.

If configless is enabled, `slurm.conf` is not needed on a `slurmd` only node. In this case, `slurmd` must be started with `-Z --conf-server`. You can do this by:

```sh
sudo systemctl edit --full slurmd
```

:::{literalinclude} /_files/centos/etc/systemd/system/slurmd.service
:diff:  /_files/centos/etc/systemd/system/slurmd.service.orig
:class: file-content
:::

```sh
sudo vi /etc/slurm/slurmdbd.conf
```

:::{literalinclude} /_files/centos/etc/slurm/slurmdbd.conf
:diff: /_files/centos/etc/slurm/slurmdbd.conf.orig
:class: file-content
:::

```sh
sudo chown slurm:slurm /etc/slurm/slurmdbd.conf
sudo chmod 0600 slurmdbd.conf
```

## Create directories & files

```sh
# SlurmctldPidFile & SlurmdPidFile
sudo mkdir -p /var/run/slurm/ && sudo chown slurm:slurm /var/run/slurm
# StateSaveLocation
sudo mkdir -p /var/spool/slurm/ctld && sudo chown slurm:slurm /var/spool/slurm/ctld
# SlurmdSpoolDir
sudo mkdir -p /var/spool/slurm/d && sudo chown slurm:slurm /var/spool/slurm/d
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

## Run

Start `slurmdbd` first if it is configured (for `slurmctld`):

```sh
sudo systemctl enable slurmdbd --now
```

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

Show version of Slurm:

```sh
sinfo -V
```

{.cli-output}

```text
slurm 24.05.1
```

Check sluster status:

```sh
sinfo
```

:::{literalinclude} /_files/centos/output/sinfo/no_args.txt
:language: text
:class: cli-output
:::
