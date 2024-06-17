# CRI-O

<https://cri-o.io/>

LIGHTWEIGHT CONTAINER RUNTIME FOR KUBERNETES.

:CPU: x86_64 * 8
:OS: CentOS 8.5

## Install

```sh
vi /etc/yum.repos.d/cri-o.repo
```

:::{literalinclude} /_files/centos/etc/yum.repos.d/cri-o.repo
:language: ini
:class: file-content
:::

## Run

```sh
systemctl enable crio --now
```
