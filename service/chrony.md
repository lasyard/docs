# chrony

<https://chrony-project.org/>

`chrony` is NTP server and client on CentOS 8.5.

## Install

```sh
$ sudo dnf install chrony
```

Check the version:

```console
$ chronyd --version
chronyd (chrony) version 4.1 (+CMDMON +NTP +REFCLOCK +RTC +PRIVDROP +SCFILTER +SIGND +ASYNCDNS +NTS +SECHASH +IPV6 +DEBUG)
```

```console
$ chronyc --version
chronyc (chrony) version 4.1 (+READLINE +SECHASH +IPV6 +DEBUG)
```

## Configure

### Server

Edit file `/etc/chrony.conf`:

:::{literalinclude} /_files/centos/etc/chrony.conf.server
:diff: /_files/centos/etc/chrony.conf.orig
:::

### Client

Edit file `/etc/chrony.conf`:

:::{literalinclude} /_files/centos/etc/chrony.conf.client
:diff: /_files/centos/etc/chrony.conf.orig
:::

Enable the service on both servers and clients:

```console
$ sudo systemctl enable chronyd --now
```

## Usage

List servers:

```console
$ chronyc sources
MS Name/IP address         Stratum Poll Reach LastRx Last sample
===============================================================================
^* las0                          2  10   377   709    -58us[  -79us] +/- 9075us
```

List clients:

```console
$ sudo chronyc clients
Hostname                      NTP   Drop Int IntL Last     Cmd   Drop Int  Last
===============================================================================
las1                           52      0  10   -   810       0      0   -     -
las2                           64      0  10   -   958       0      0   -     -
localhost                       0      0   -   -     -       6      0   5    14
```
