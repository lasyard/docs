# minikube

<https://minikube.sigs.k8s.io/>

## Install

::::{tab-set}
:::{tab-item} macOS
:sync: macos

```console
$ curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-darwin-amd64
$ sudo install minikube-darwin-amd64 /usr/local/bin/minikube
```

:::
::::

Show the version:

```console
$ minikube version
minikube version: v1.38.1
commit: c93a4cb9311efc66b90d33ea03f75f2c4120e9b0
```

## Run

Using VMWare Fusion:

```console
$ minikube config set driver vmware
❗  这些更改将在执行 minikube delete 后生效，然后执行 minikube start
```

Start a minikube cluster:

::::{tab-set}
:::{tab-item} macOS
:sync: macos

```console
$ minikube start
😄  Darwin 12.7.6 上的 minikube v1.38.1
✨  根据用户配置使用 vmware 驱动程序
❗  Starting v1.39.0, minikube will default to "containerd" container runtime. See #21973 for more info.
💿  正在下载 VM boot image...
    > minikube-v1.38.0-amd64.iso....:  65 B / 65 B [---------] 100.00% ? p/s 0s
    > minikube-v1.38.0-amd64.iso:  370.55 MiB / 370.55 MiB  100.00% 4.77 MiB p/
👍  在集群中 "minikube" 启动节点 "minikube" primary control-plane
💾  正在下载 Kubernetes v1.35.1 的预加载文件...
    > preloaded-images-k8s-v18-v1...:  272.45 MiB / 272.45 MiB  100.00% 4.40 Mi
🔥  正在创建 vmware VM（CPUs=2，内存=3072MB，磁盘=20000MB）...
🐳  正在 Docker 28.5.2 中准备 Kubernetes v1.35.1…
🔗  配置 bridge CNI (Container Networking Interface) ...
🔎  正在验证 Kubernetes 组件...
    ▪ 正在使用镜像 gcr.io/k8s-minikube/storage-provisioner:v5
🌟  启用插件： storage-provisioner, default-storageclass
🏄  完成！kubectl 现在已配置，默认使用"minikube"集群和"default"命名空间
```

:::
::::

Check status:

```console
$ minikube status
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

Destroy the cluster:

```console
$ minikube delete
🔥  正在删除 vmware 中的“minikube”…
💀  已删除所有关于 "minikube" 集群的痕迹。
```

## Usage

Load an image (saved by docker) into minikube:

```console
$ minikube image load registry.k8s.io/kueue/kueue-v0.16.2.tar.bz2
$ minikube image ls
registry.k8s.io/pause:3.10.1
registry.k8s.io/kueue/kueue:v0.16.2
registry.k8s.io/kube-scheduler:v1.35.1
registry.k8s.io/kube-proxy:v1.35.1
registry.k8s.io/kube-controller-manager:v1.35.1
registry.k8s.io/kube-apiserver:v1.35.1
registry.k8s.io/etcd:3.6.6-0
registry.k8s.io/coredns/coredns:v1.13.1
gcr.io/k8s-minikube/storage-provisioner:v5
```
