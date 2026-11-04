# Cilium

<https://cilium.io/>

## Install CLI

:::::{tab-set}
::::{tab-item} macOS
:sync: macos

Download the tar ball:

```console
$ curl -LO https://github.com/cilium/cilium-cli/releases/download/v0.20.1/cilium-darwin-arm64.tar.gz
$ curl -LO https://github.com/cilium/cilium-cli/releases/download/v0.20.1/cilium-darwin-arm64.tar.gz.sha256sum
$ shasum -a 256 -c cilium-darwin-arm64.tar.gz.sha256sum 
cilium-darwin-arm64.tar.gz: OK
```

Install:

```console
$ sudo tar -C /usr/local/bin -xzf cilium-darwin-arm64.tar.gz
```

::::
:::::

## Install Cilium In Current {{k8s}}

```console
$ cilium install 1.20.4
ℹ️  Using Cilium version 1.20.1
🔮 Auto-detected cluster name: las
🔮 Auto-detected kube-proxy has been installed
```

This means `kube-proxy` is already installed. Cilium can co-exist with `kube-proxy`, or replace it totally.

Now uninstall Cilium:

```console
$ cilium uninstall
🔥 Deleting pods in cilium-test namespace...
🔥 Deleting cilium-test namespace...
⌛ Uninstalling Cilium
🔥 Deleting pods in cilium-test namespace...
🔥 Deleting cilium-test namespace...
🔥 Cleaning up Cilium node annotations...
```

Remove `kube-proxy` from the cluster:

```console
$ kubectl -n kube-system delete ds kube-proxy
daemonset.apps "kube-proxy" deleted from kube-system namespace
$ kubectl -n kube-system delete cm kube-proxy
configmap "kube-proxy" deleted from kube-system namespace
```

Reinstall Cilium:

```console
$ cilium install 1.20.4
ℹ️  Using Cilium version 1.20.1
🔮 Auto-detected cluster name: las
🔮 Auto-detected kube-proxy has not been installed
ℹ️  Cilium will fully replace all functionalities of kube-proxy
```

This command actually use `helm` to install:

```console
$ helm list -n kube-system
NAME    NAMESPACE   REVISION    UPDATED                                 STATUS      CHART           APP VERSION
cilium  kube-system 1           2026-11-04 17:55:52.767124 +0800 CST    deployed    cilium-1.20.1   1.20.1
```

Installed workloads:

```console
$ kubectl get svc,ds,deploy -n kube-system
NAME                   TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                  AGE
service/cilium-envoy   ClusterIP   None            <none>        9964/TCP                 7m53s
service/hubble-peer    ClusterIP   10.104.202.33   <none>        443/TCP                  7m53s
service/kube-dns       ClusterIP   10.96.0.10      <none>        53/UDP,53/TCP,9153/TCP   62d

NAME                          DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
daemonset.apps/cilium         2         2         2       2            2           kubernetes.io/os=linux   7m53s
daemonset.apps/cilium-envoy   2         2         2       2            2           kubernetes.io/os=linux   7m53s

NAME                              READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/cilium-operator   1/1     1            1           7m53s
deployment.apps/coredns           2/2     2            2           62d
```
