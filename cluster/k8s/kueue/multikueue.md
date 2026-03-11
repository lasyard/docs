# 使用 MultiKueue 特性分发作业到多集群

利用 Kueue 的 MultiKueue 特性可以将作业从管理集群分发到工作集群，基本过程如下：

1. 用户提交作业到管理集群
2. 管理集群的 Kueue 控制器拦截作业，并向工作集群提交相同的作业
3. 工作集群按正常流程处理和运行作业

![multikueue.png](/_generated_images/cluster/k8s/kueue/multikueue.png)

相同的作业在两个集群都要提交一次，因此作业所在的命名空间和队列必须在两个集群中都存在。

目前 Kueue 0.16.2 不支持向管理集群自身分发作业。

工作集群的队列设置与使用 MultiKueue 之前相同，不需要特殊设置，以下是实体关系图（没有使用 Topology）：

```{mermaid}
erDiagram

LocalQueue }o--|| ClusterQueue: ""
ClusterQueue }o--|{ ResourceFlavor: ""
```

管理集群的 ClusterQueue 需要增加一个特殊的 AdmissionCheck 属性，以下为其实体关系图：

```{mermaid}
erDiagram

LocalQueue }o--|| ClusterQueue: ""
ClusterQueue }o--|{ ResourceFlavor: ""
ClusterQueue }o--o{ AdmissionCheck : ""
AdmissionCheck }o--o| MultikueueConfig : ""
MultikueueConfig }o--|{ MultikueueCluster : ""
MultikueueCluster }o--|| Secret : ""
```

可见增加的属性经过多层引用后最终指向了一个 Secret, 这个 Secret 存放着工作集群的 kubeconfig. 这是管理集群中的 Kueue 访问工作集群的依据。

## 配置

参考 <https://kueue.sigs.k8s.io/docs/tasks/manage/setup_multikueue/>.

管理集群和工作集群安装同一版本的 Kueue.

在工作集群创建队列不需要额外设置，如下：

:::{literalinclude} /_files/macos/workspace/k8s/kueue/worker_lq.yaml
:::

在管理集群创建队列，需要在 ClusterQueue 上设置 AdmissionCheck, 以下展示的是与工作集群队列的差异：

:::{literalinclude} /_files/macos/workspace/k8s/kueue/master_lq.yaml
:diff: /_files/macos/workspace/k8s/kueue/worker_lq.yaml
:::

注意我们故意修改了 ClusterQueue 的名称，这是为了说明 MultiKueue 分发的原则是相同 namespace, 相同 LocalQueue. 两者之间 ClusterQueue 的设置可以不一致。

在管理集群中创建工作集群的准入设置：

:::{literalinclude} /_files/macos/workspace/k8s/kueue/worker_admissioncheck.yaml
:::

这里面 MultiKueueCluster 中的 `spec.clusterSource.kubeConfig` 引用了一个存放工作集群 kubeconfig 的 Secret, 需要借助一个脚本来产生。脚本的下载地址：<https://kueue.sigs.k8s.io/examples/multikueue/create-multikueue-kubeconfig.sh>.

这个脚本的作用如下：

1. 在工作集群中创建 ServiceAccount, ClusterRole, ClusterRoleBinding 以便管理集群对工作集群进行操作
2. 为新的 ServiceAccount 创建证书
3. 从当前 kubectl 上下文中提取集群信息，结合生成的证书，创建 kubeconfig 文件

因此它应该在 kubectl 上下文指向工作集群的时候运行。注意 ServiceAccount 和 证书 Secret 需要创建在 Kueue 安装的命名空间内。

运行脚本产生 kubeconfig 文件：

```console
$ ./create-multikueue-kubeconfig.sh worker1.kubeconfig
serviceaccount/multikueue-sa created
clusterrole.rbac.authorization.k8s.io/multikueue-sa-role created
clusterrolebinding.rbac.authorization.k8s.io/multikueue-sa-crb created
secret/multikueue-sa created
Writing kubeconfig in worker1.kubeconfig
```

在管理集群中，创建 Secret 存放这个 kubeconfig 文件：

```console
$ kubectl create secret generic worker1-secret -n kueue-system --from-file=kubeconfig=worker1.kubeconfig
secret/worker1-secret created
```

检查状态：

```console
$ kubectl get cq to-worker1 -o jsonpath="{range .status.conditions[?(@.type == \"Active\")]}CQ - Active: {@.status} Reason: {@.reason} Message: {@.message}{'\n'}{end}"
CQ - Active: True Reason: Ready Message: Can admit new workloads
$ kubectl get admissioncheck worker1-admission-check -o jsonpath="{range .status.conditions[?(@.type == \"Active\")]}AC - Active: {@.status} Reason: {@.reason} Message: {@.message}{'\n'}{end}"
AC - Active: True Reason: Active Message: The admission check is active
$ kubectl get multikueuecluster worker1 -o jsonpath="{range .status.conditions[?(@.type == \"Active\")]}MC - Active: {@.status} Reason: {@.reason} Message: {@.message}{'\n'}{end}"
MC - Active: True Reason: Active Message: Connected
```

这说明工作集群连接成功，可以向队列提交工作负载了。

不成功的可能原因：

- 管理集群中 Kueue 支持的工作负载类型必须在工作集群中存在

## 提交作业

提交以下作业：

:::{literalinclude} /_files/macos/workspace/k8s/kueue/sleep_job_kueue.yaml
:::

在管理集群上监视作业状态：

```console
$ kubectl get job -w       
NAME           STATUS    COMPLETIONS   DURATION   AGE
sleep-normal   Running   0/3                      0s
sleep-normal   Running   0/3                      0s
sleep-normal   Running   0/3           0s         0s
sleep-normal   Running   0/3           3s         3s
sleep-normal   Running   2/3           33s        33s
sleep-normal   Complete   3/3           34s        34s
```

同时在工作集群上监视作业状态：

```console
$ kubectl get job  -w
NAME           STATUS    COMPLETIONS   DURATION   AGE
sleep-normal   Running   0/3                      0s
sleep-normal   Suspended   0/3                      0s
sleep-normal   Suspended   0/3                      0s
sleep-normal   Running     0/3           0s         0s
sleep-normal   Running     0/3           3s         3s
sleep-normal   Running     0/3           32s        32s
sleep-normal   Running     2/3           33s        33s
sleep-normal   SuccessCriteriaMet   3/3           34s        34s
sleep-normal   Complete             3/3           34s        34s
sleep-normal   Complete             3/3           34s        34s
```

另外可以发现：

- 管理集群内没有为 Job 创建 Pod, 工作集群中的 Job 按正常流程运行
- 当作业完成后，工作集群内的 Job 被删除，而管理集群内的 Job 仍然保留
