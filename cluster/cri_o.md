# CRI-O

<https://cri-o.io/>

LIGHTWEIGHT CONTAINER RUNTIME FOR KUBERNETES.

:::{include} /_frags/plats/centos.txt
:::

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
