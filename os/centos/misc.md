# Miscellaneous

## Check version

```console
$ cat /etc/centos-release
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

:::{literalinclude} /_files/centos/console/cat/proc_swaps.txt
:language: console
:::

Turn off swap for all devices:

```console
$ swapoff -av
swapoff /dev/dm-1
```

To permanently disable swap, edit `/etc/fstab` and comment out the line that mounts the swap partition.

## ulimit

Show current limits:

:::{literalinclude} /_files/centos/console/ulimit/a.txt
:language: console
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

:::{literalinclude} /_files/centos/console/cat/proc_1_limits.txt
:language: console
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

:::{literalinclude} /_files/centos/console/timedatectl/no_args.txt
:language: console
:::

List available time zones:

:::{literalinclude} /_files/centos/console/timedatectl/list_timezones.txt
:language: console
:::

Set time zone:

```sh
timedatectl set-timezone Asia/Shanghai
```

## alternatives

```console
$ alternatives --version
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
