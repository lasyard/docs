# Install Kubernetes Packages

## By package manager

::::{tab-set}
:::{tab-item} Ubuntu 22.04

Add the Kubernetes repository:

```console
$ curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.32/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
$ echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.32/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
```

Install `kubelet`, `kubeadm` and `kubectl`, and pin their versions:

```console
$ sudo apt update
$ sudo apt install -y kubelet kubeadm kubectl
$ sudo apt-mark hold kubelet kubeadm kubectl
```

```console
$ kubeadm version -o yaml
clientVersion:
  buildDate: "2025-03-11T19:57:38Z"
  compiler: gc
  gitCommit: 32cc146f75aad04beaaa245a7157eb35063a9f99
  gitTreeState: clean
  gitVersion: v1.32.3
  goVersion: go1.23.6
  major: "1"
  minor: "32"
  platform: linux/amd64
```

Default output style is Go style, which is why `-o yaml` is needed.

:::
::::

## Dowload kubectl manually

`kubectl` can be installed anywhere to access k8s system.

```console
$ curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl"
```

Check the versions:

```console
$ kubectl version
Client Version: v1.32.0
Kustomize Version: v5.5.0
Server Version: v1.32.0
```
