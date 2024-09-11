# Miscellaneous

## Check version

```sh
cat /etc/centos-release
```

{.cli-output}

```text
CentOS Linux release 8.5.2111
```

## User Management

Add a user:

```sh
sudo useradd xxxx
```

Add the user to a group:

```sh
sudo usermod -aG wheel xxxx
```

## List port listening

```sh
netstat -ltnp
lsof -i :6820
```

## Disable SELinux

See current status:

```sh
getenforce
```

Temporarily disable it:

```sh
sudo setenforce 0
```

Permanently disable it:

```sh
sudo vi /etc/selinux/config
```

:::{literalinclude} /_files/centos/etc/selinux/config
:diff: /_files/centos/etc/selinux/config.orig
:class: file-content
:::

## Set swap off

```sh
cat /proc/swaps
```

:::{literalinclude} /_files/centos/output/cat/proc_swaps.txt
:language: text
:class: cli-output
:::

Turn off swap for all devices:

```sh
swapoff -av
```

{.cli-output}

```text
swapoff /dev/dm-1
```

To permanently disable swap, edit `/etc/fstab` and comment out the line that mounts the swap partition.

## ulimit

Provides control over the resources available to the shell and to processes started by it, on systems that allow such control.

Show current limits:

```sh
ulimit -a
```

:::{literalinclude} /_files/centos/output/ulimit/a.txt
:language: text
:class: cli-output
:::

Set the maximum number of open files:

```sh
ulimit -n 1048576
```

This is effective only in current shell and any child processes. To make it permanent:

```sh
sudo vi /etc/security/limits.conf
```

:::{literalinclude} /_files/centos/etc/security/limits.conf.orig
:language: text
:class: file-content
:::

The modification will take effect after a re-login.

:::{note}
If there are file in `/etc/security/limits.d`, the values may be overridden by those files.
:::

The limits are applied by a per-process manner. You can check the limits for process 1 (i.e. the init process):

```sh
cat /proc/1/limits
```

:::{literalinclude} /_files/centos/output/cat/proc_1_limits.txt
:language: text
:class: cli-output
:::

## Show system logs

Monitor system logs continuously:

```sh
journalctl -f
```

Just like `tail -f`.

Show system logs for a specific unit (service):

```sh
journalctl -u chrony
```

## hostname

Show hostname:

```sh
hostname
```

Temporarily set hostname:

```sh
sudo hostname xxxx
```

Set hostname:

```sh
sudo vi /etc/hostname
```

Make it effective immediately:

```sh
sudo hostname -F /etc/hostname
```

You may need to edit `/etc/hosts` to map the hostname accordingly.

## systemctl

Control the systemd system and service manager.

Change the editor to do `systemctl edit`:

```sh
export SYSTEMD_EDITOR=vi
```

```sh
sudo visudo
```

:::{literalinclude} /_files/centos/etc/sudoers
:diff: /_files/centos/etc/sudoers.orig
:class: file-content
:::

## Time zone

Show information:

```sh
timedatectl
```

:::{literalinclude} /_files/centos/output/timedatectl/no_args.txt
:language: ini
:class: cli-output
:::

List available time zones:

```sh
timedatectl list-timezones
```

:::{literalinclude} /_files/centos/output/timedatectl/list_timezones.txt
:language: ini
:class: cli-output
:::

Set time zone:

```sh
timedatectl set-timezone Asia/Shanghai
```

## alternatives

```sh
alternatives --version
```

{.cli-output}

```text
alternatives（备用）版本 1.19.1
```

List all software managed by alternatives:

```sh
alternatives --list
```

Config a software:

```sh
sudo alternatives --config modules.sh
```
