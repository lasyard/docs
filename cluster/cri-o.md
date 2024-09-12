# CRI-O

<https://cri-o.io/>

LIGHTWEIGHT CONTAINER RUNTIME FOR KUBERNETES.

## Install

::::{plat} centos
:vers: CentOS 8.5

```sh
sudo vi /etc/yum.repos.d/cri-o.repo
```

:::{literalinclude} /_files/centos/etc/yum.repos.d/cri-o.repo
:language: ini
:class: file-content
:::

## Run

```sh
sudo systemctl enable crio --now
```

::::
