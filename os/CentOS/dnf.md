# dnf

<https://docs.fedoraproject.org/en-US/quick-docs/dnf/>

DNF is a software package manager that installs, updates, and removes packages on Fedora and is the successor to YUM (Yellow-Dog Updater Modified).

## Install

[EPEL](https://docs.fedoraproject.org/en-US/epel/) repository is required for `dnf`:

```sh
yum install epel-release
```

Then install `dnf`:

```sh
yum install dnf
```

Repository url may need to be changed for CentOS 8:

```sh
sed -i -e "s|mirrorlist=|#mirrorlist=|" /etc/yum.repos.d/CentOS-Linux-*.repo
sed -i -e "s|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|" /etc/yum.repos.d/CentOS-Linux-*.repo
```

## Usage

List repositories:

```sh
dnf repolist
```

List installed packages:

```sh
dnf list --installed
```

List files of a package:

```sh
dnf repoquery -l chrony
```

Uninstall/remove a package:

```sh
dnf remove slurm
```
