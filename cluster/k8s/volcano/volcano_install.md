# 在 Kubernetes 集群中安装 Volcano 调度器

## 使用 helm 安装

添加官网仓库并更新：

```console
$ helm repo add volcano-sh https://volcano-sh.github.io/helm-charts
"volcano-sh" has been added to your repositories
$ helm repo update
Hang tight while we grab the latest from your chart repositories️...
...Successfully got an update from the "volcano-sh" chart repository
Update Complete. ⎈Happy Helming!⎈
```

拉取文件：

```console
$ helm pull volcano-sh/volcano
```

安装：

```console
$ helm install volcano volcano-1.12.2.tgz -n volcano-system --create-namespace
NAME: volcano
LAST DEPLOYED: Thu Aug 28 15:47:17 2025
NAMESPACE: volcano-system
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
Thank you for installing volcano.

Your release is named volcano.

For more information on volcano, visit:
https://volcano.sh/
```

以上安装的是当前最新 Release 版本 `1.12.2`.

检查以下 Pod 是否正常运行：

```console
$ kubectl get po -n volcano-system
NAME                                   READY   STATUS    RESTARTS   AGE
volcano-admission-5dd7897d96-x8897     1/1     Running   0          62s
volcano-controllers-7c58d44b88-p7n5v   1/1     Running   0          62s
volcano-scheduler-986f77795-csmdd      1/1     Running   0          62s
```

查看是否有以下默认队列：

```console
$ kubectl get q
NAME      PARENT
default   root
root
```

以下是 `1.11.2` 版本的输出，对比可发现，不知为何加了 `PARENT` 但是把 `AGE` 去掉了。

```console
$ kubectl get q
NAME      AGE
default   16h
root      16h
```

## 配置

安装成功后修改调度器配置：

```console
$ kubectl edit cm volcano-scheduler-configmap -n volcano-system
configmap/volcano-scheduler-configmap edited
```

参考以下配置：

:::{literalinclude} /_files/macos/workspace/k8s/volcano/volcano_scheduler_config.yaml
:::

## 问题解决

### 没有外网怎么办

需要在有外网的主机上下载以上 helm chart 以及以下几个映像：

```text
docker.io/volcanosh/vc-controller-manager:v1.12.2
docker.io/volcanosh/vc-scheduler:v1.12.2
docker.io/volcanosh/vc-webhook-manager:v1.12.2
```

以下为 Volcano helm chart 的一些基本 Values 的配置：

```yaml
basic:
  controller_image_name: "volcanosh/vc-controller-manager"
  scheduler_image_name: "volcanosh/vc-scheduler"
  admission_image_name: "volcanosh/vc-webhook-manager"
  image_pull_secret: ""
  image_pull_policy: "Always"
  image_tag_version: "v1.12.2"
  image_registry: "docker.io"
```

安装时可以通过 `--set` 参数改变默认值，例如：

```console
$ helm install volcano volcano-1.12.2.tgz -n volcano-system --create-namespace --set basic.image_pull_policy=IfNotPresent --set basic.image_registry=harbor.hd-03.zetyun.cn
```
