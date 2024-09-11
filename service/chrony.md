# chrony

<https://chrony-project.org/>

`chrony` is a versatile implementation of the Network Time Protocol (NTP).

::::{plat} centos
{{ cluster_las }}

Roles of the nodes:

:NTP Server: las1
:NTP Client: las2, las3

## Install

```sh
sudo dnf install chrony
```

```sh
chronyc --version
```

:::{literalinclude} /_files/centos/output/chronyc/version.txt
:language: text
:class: cli-output
:::

```sh
chronyd --version
```

:::{literalinclude} /_files/centos/output/chronyd/version.txt
:language: text
:class: cli-output
:::

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

```sh
chronyc sources
```

:::{literalinclude} /_files/centos/output/chronyc/sources.txt
:language: text
:class: cli-output
:::

List clients:

```sh
sudo chronyc clients
```

:::{literalinclude} /_files/centos/output/chronyc/clients.txt
:language: text
:class: cli-output
:::

::::
