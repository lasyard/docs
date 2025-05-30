# helm

<https://helm.sh/>

## Prerequisites

Install `git` first, see "<project:/devel/git.md#install-git>".

## Install

::::{tab-set}
:::{tab-item} Linux

```console
$ curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
$ chmod +x get_helm.sh
$ sudo ./get_helm.sh
Downloading https://get.helm.sh/helm-v3.17.3-linux-amd64.tar.gz
Verifying checksum... Done.
Preparing to install helm into /usr/local/bin
helm installed into /usr/local/bin/helm
```

Check the version:

```console
$ helm version
version.BuildInfo{Version:"v3.17.3", GitCommit:"e4da49785aa6e6ee2b86efd5dd9e43400318262b", GitTreeState:"clean", GoVersion:"go1.23.7"}
```

:::
:::{tab-item} macOS

```console
$ curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
$ chmod +x get_helm.sh
$ ./get_helm.sh
Downloading https://get.helm.sh/helm-v3.16.4-darwin-amd64.tar.gz
Verifying checksum... Done.
Preparing to install helm into /usr/local/bin
helm installed into /usr/local/bin/helm
```

Check the version:

```console
$ helm version
version.BuildInfo{Version:"v3.16.4", GitCommit:"7877b45b63f95635153b29a42c0c2f4273ec45ca", GitTreeState:"clean", GoVersion:"go1.22.7"}
```

:::
::::

## Usage

Show repositories:

```console
$ helm repo list
NAME        URL                                     
volcano-sh  https://volcano-sh.github.io/helm-charts
```

Pull charts:

```console
$ helm pull volcano-sh/volcano
$ ls *.tgz
volcano-1.11.1.tgz
```

List (deployed) releases in all namespaces:

```console
$ helm list -A
NAME    NAMESPACE       REVISION    UPDATED                                 STATUS      CHART           APP VERSION
volcano volcano-system  1           2025-04-22 03:47:04.391250411 +0000 UTC deployed    volcano-1.11.1  1.11.1
```

Uninstall a release:

```console
$ helm uninstall volcano -n volcano-system
release "volcano" uninstalled
```

Get manifest files of a release:

```console
$ helm get manifest xxxx-release
```
