# chrony

<https://chrony-project.org/>

`chrony` is a versatile implementation of the Network Time Protocol (NTP).

:CPU: x86_64 * 8
:OS: CentOS 8.5
:NTP Server: las1
:NTP Client: las2, las3

## Install

```sh
dnf install chrony
```

```sh
chronyc --version
```

{.cli-output}

```text
chronyc (chrony) version 4.1 (+READLINE +SECHASH +IPV6 +DEBUG)
```

```sh
chronyd --version
```

{.cli-output}

```text
chronyd (chrony) version 4.1 (+CMDMON +NTP +REFCLOCK +RTC +PRIVDROP +SCFILTER +SIGND +ASYNCDNS +NTS +SECHASH +IPV6 +DEBUG)
```

## Configure

### Server

```sh
vi /etc/chrony.conf
```

:::{literalinclude} /_files/centos/etc/chrony.conf.server
:language: conf
:diff: /_files/centos/etc/chrony.conf.orig
:class: file-content
:::

### Client

```sh
vi /etc/chrony.conf
```

:::{literalinclude} /_files/centos/etc/chrony.conf.client
:language: conf
:diff: /_files/centos/etc/chrony.conf.orig
:class: file-content
:::

## Run

```sh
systemctl enable chronyd --now
```

## Usage

List servers:

```sh
chronyc sources
```

{.cli-output}

```text
MS Name/IP address         Stratum Poll Reach LastRx Last sample               
===============================================================================
^* las1                          2   7   377    41    +37us[  +45us] +/-   27ms
```

List clients:

```sh
chronyc clients
```

{.cli-output}

```text
Hostname                      NTP   Drop Int IntL Last     Cmd   Drop Int  Last
===============================================================================
las2                        17237      0   7   -   105       0      0   -     -
las3                        23920      0   6   -    13       0      0   -     -
```
