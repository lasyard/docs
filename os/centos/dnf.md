# dnf

<https://docs.fedoraproject.org/en-US/quick-docs/dnf/>

## Upgrade from yum to dnf

[EPEL](https://docs.fedoraproject.org/en-US/epel/) repository is required to install `dnf`:

```console
$ sudo yum install epel-release
```

Then install `dnf`:

```console
$ sudo yum install dnf
```

Repository url may need to be changed for CentOS 8:

```sh
$ sudo sed -i -e "s|mirrorlist=|#mirrorlist=|" /etc/yum.repos.d/CentOS-Linux-*.repo
$ sudo sed -i -e "s|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|" /etc/yum.repos.d/CentOS-Linux-*.repo
```

## Usage

List repositories:

```console
$ dnf repolist
```

List installed packages:

```console
$ dnf list --installed
```

List mannually installed packages:

```console
$ dnf repoquery --userinstalled
```

List files of a package:

```console
$ dnf repoquery -l chrony
```

Uninstall/remove a package:

```console
$ sudo dnf remove slurm
```

Remove all user installed packages:

```console
$ dnf repoquery --userinstalled | grep -v kernel-core | xargs sudo dnf remove -y
```

List package groups:

```console
$ dnf group list
```

List packages in a group:

```console
$ dnf group info "Development Tools"
```

Install a package group:

```console
$ sudo dnf group install "Development Tools"
```

Clean:

```console
$ sudo dnf clean all
```

Disable a repo:

```console
$ sudo dnf config-manager --disable docker-ce-stable
```
