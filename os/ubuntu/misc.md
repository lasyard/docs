# Miscellaneous

## Check version

```console
$ cat /etc/debian_version
bookworm/sid
$ cat /etc/lsb-release
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=22.04
DISTRIB_CODENAME=jammy
DISTRIB_DESCRIPTION="Ubuntu 22.04.5 LTS"
```

## User management

Add a new user:

```console
$ sudo adduser xxxx
```

Add the new user to the `sudo` group:

```console
$ sudo usermod -aG sudo xxxx
```

Add a new user with other specified attributes:

```console
$ sudo adduser --disabled-password --disabled-login --no-create-home --gecos "XXXX" --uid 1001 xxxx
```

Delete a user:

```console
$ sudo deluser xxxx
Removing user `xxxx' ...
Warning: group `xxxx' has no more members.
Done.
$ sudo rm -rf /home/xxxx
```

## hostname

Show hostname:

```console
$ hostname
```

Temporarily set hostname:

```console
$ sudo hostname xxxx
```

Edit `/etc/hostname` to set it permanently (effective after reboot), and make it effective immediately after editing the file:

```console
$ sudo hostname -F /etc/hostname
```

You may need to edit `/etc/hosts` to map the hostname accordingly.
