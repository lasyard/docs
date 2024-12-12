# chrony

<https://chrony-project.org/>

::::{plat} centos
{{ cluster_las }}

Roles of the nodes:

:NTP Server: las0
:NTP Client: las1, las2

## Install

```sh
sudo dnf install chrony
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

```sh
sudo vi /etc/chrony.conf
```

:::{literalinclude} /_files/centos/etc/chrony.conf.server
:diff: /_files/centos/etc/chrony.conf.orig
:class: file-content
:::

### Client

```sh
sudo vi /etc/chrony.conf
```

:::{literalinclude} /_files/centos/etc/chrony.conf.client
:diff: /_files/centos/etc/chrony.conf.orig
:class: file-content
:::

## Run

```sh
sudo systemctl enable chronyd --now
```

## Usage

List servers:

:::{literalinclude} /_files/centos/console/chronyc/sources.txt
:language: console
:::

List clients:

:::{literalinclude} /_files/centos/console/chronyc/clients.txt
:language: console
:::

::::
