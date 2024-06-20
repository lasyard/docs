# CRI-O

<https://cri-o.io/>

LIGHTWEIGHT CONTAINER RUNTIME FOR KUBERNETES.

{{ for_centos }}

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
