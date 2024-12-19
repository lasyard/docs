# dnf

<https://docs.fedoraproject.org/en-US/quick-docs/dnf/>

## Install

[EPEL](https://docs.fedoraproject.org/en-US/epel/) repository is required to install `dnf`:

```sh
sudo yum install epel-release
```

Then install `dnf`:

```sh
sudo yum install dnf
```

Repository url may need to be changed for CentOS 8:

```sh
sudo sed -i -e "s|mirrorlist=|#mirrorlist=|" /etc/yum.repos.d/CentOS-Linux-*.repo
sudo sed -i -e "s|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|" /etc/yum.repos.d/CentOS-Linux-*.repo
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

List mannually installed packages:

```sh
dnf repoquery --userinstalled
```

List files of a package:

```sh
dnf repoquery -l chrony
```

Uninstall/remove a package:

```sh
sudo dnf remove slurm
```

Remove all user installed packages:

```sh
dnf repoquery --userinstalled | grep -v kernel-core | xargs sudo dnf remove -y
```

List package groups:

```sh
dnf group list
```

List packages in a group:

```sh
dnf group info "Development Tools"
```

Install a package group:

```sh
sudo dnf group install "Development Tools"
```

Clean:

```sh
sudo dnf clean all
```

Disable a repo:

```sh
sudo dnf config-manager --disable docker-ce-stable
```
