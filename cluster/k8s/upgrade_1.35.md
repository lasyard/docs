# 升级到 1.35

`kubelet 1.35` 的启动参数有以下改动：

- `--container-runtime-endpoint`: 已弃用，改到了配置文件中
- `--pod-infra-container-image`: 不再支持

所以需要修改以下配置（适用于 `kubeadm` 安装的集群）：

1. 修改 `/var/lib/kubelet/kubeadm-flags.env`
   :::{literalinclude} /_files/ubuntu/var/lib/kubelet/kubeadm-flags.env
   :diff: /_files/ubuntu/var/lib/kubelet/kubeadm-flags.env.orig
   :::

1. 修改 `/var/lib/kubelet/config.yaml`
   :::{literalinclude} /_files/ubuntu/var/lib/kubelet/config.yaml
   :diff: /_files/ubuntu/var/lib/kubelet/config.yaml.orig
   :::

然后更换各个组件的映像。

1. `kube-apiserver`, 修改 `/etc/kubernetes/manifests/kube-apiserver.yaml`:
   :::{literalinclude} /_files/ubuntu/etc/kubernetes/manifests/kube-apiserver_1.35.yaml
   :diff: /_files/ubuntu/etc/kubernetes/manifests/kube-apiserver_1.34.yaml
   :::

1. `kube-scheduler`, 修改 `/etc/kubernetes/manifests/kube-scheduler.yaml`:
   :::{literalinclude} /_files/ubuntu/etc/kubernetes/manifests/kube-scheduler_1.35.yaml
   :diff: /_files/ubuntu/etc/kubernetes/manifests/kube-scheduler_1.34.yaml
   :::

1. `kube-controller-manager`, 修改 `/etc/kubernetes/manifests/kube-controller-manager.yaml`:
   :::{literalinclude} /_files/ubuntu/etc/kubernetes/manifests/kube-controller-manager_1.35.yaml
   :diff: /_files/ubuntu/etc/kubernetes/manifests/kube-controller-manager_1.34.yaml
   :::

1. `kube-proxy`, 运行命令：

   ```console
   $ kubectl -n kube-system set image daemonset/kube-proxy kube-proxy=registry.aliyuncs.com/google_containers/kube-proxy:v1.35.0
   daemonset.apps/kube-proxy image updated
   ```

以上配置同时启用了特性门 `GenericWorkload`.

重启 `kubelet` 服务成功以后：

```console
$ kubectl get no
NAME   STATUS   ROLES           AGE    VERSION
las0   Ready    control-plane   242d   v1.35.0
las1   Ready    <none>          242d   v1.35.0
las2   Ready    <none>          242d   v1.35.0
las3   Ready    <none>          238d   v1.35.0
```

查询 kubelet 特性门是否启用：

```console
$ kubectl get --raw "/api/v1/nodes/las1/proxy/configz" | jq '.kubeletconfig.featureGates'
{
  "GenericWorkload": true
}
```
