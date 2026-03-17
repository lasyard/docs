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

## 说明

- volcano 调度器安装成功后会建立两个默认的队列：`root` 和 `default`. `root` 代表调度器可以使用的全部资源，`default` 是 `root` 的子队列。新建的队列如果不指定则父队列为 `root`
- `root` 队列的容量不可以修改，但 `default` 队列的容量可以通过 `kubectl edit` 修改
- `root` 和 `default` 队列不能删除
- 非 volcano 系的 Workload (例如 Pod) 可以指定调度器为 volcano, 但是因为其 Spec 不支持 `queue` 字段，所以不能指定队列，这时消耗的是 `default` 队列的资源

队列的资源设置：

```yaml
spec:
  capability: 队列的资源上限
  deserved: 队列保留的资源数量，空闲时可以借用给其他队列，但本队列的任务优先使用
  guarantee:
    resource: 队列独占的资源数量，即使空闲也不能被其他队列借用，注意其定义多一层 resource
  reclaimable: 如果设置为 true, 当本队列有任务提交但是资源被其他队列借用导致资源不够时，可以强制退出其他队列的任务以释放资源；如果为 false, 只能等待其他队列任务主动退出
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
$ helm install volcano volcano-1.12.2.tgz -n volcano-system --create-namespace --set basic.image_pull_policy=IfNotPresent --set basic.image_registry=harbor.address
```
