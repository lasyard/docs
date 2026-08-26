# Kamaji

<https://kamaji.clastix.io/>

## 用 helm 安装

下载 helm 安装包：

```console
$ helm repo add jetstack https://charts.jetstack.io
$ helm repo update
$ helm pull clastix/kamaji --version=0.0.0+latest
```

库里面有版本号的包其实非常旧，非订阅用户只能下载最新版，不支持指定版本号。

安装：

```console
$ helm install kamaji kamaji-0.0.0+latest.tgz --version 0.0.0+latest --namespace kamaji-system --create-namespace --set datastore.enabled=true
NAME: kamaji
LAST DEPLOYED: Tue Aug 25 11:30:32 2026
NAMESPACE: kamaji-system
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
List the available CRDs installed by Kamaji:
  kubectl get customresourcedefinitions.apiextensions.k8s.io

List all the Tenant Control Plane resources deployed in your cluster:
  kubectl get tenantcontrolplanes.kamaji.clastix.io --all-namespaces
```

安装后的工作负载：

```console
$ kubectl get all -n kamaji-system
NAME                          READY   STATUS    RESTARTS   AGE
pod/kamaji-6d59c9bd6d-cqgt9   1/1     Running   0          4m29s
pod/kamaji-etcd-0             1/1     Running   0          4m29s
pod/kamaji-etcd-1             1/1     Running   0          4m19s
pod/kamaji-etcd-2             1/1     Running   0          4m7s

NAME                             TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)             AGE
service/kamaji-etcd              ClusterIP   None             <none>        2379/TCP,2380/TCP   4m29s
service/kamaji-etcd-client       ClusterIP   10.108.182.121   <none>        2379/TCP,2381/TCP   4m29s
service/kamaji-metrics-service   ClusterIP   10.98.207.182    <none>        8080/TCP            4m29s
service/kamaji-webhook-service   ClusterIP   10.100.67.74     <none>        443/TCP             4m29s

NAME                     READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/kamaji   1/1     1            1           4m29s

NAME                                DESIRED   CURRENT   READY   AGE
replicaset.apps/kamaji-6d59c9bd6d   1         1         1       4m29s

NAME                           READY   AGE
statefulset.apps/kamaji-etcd   3/3     4m29s
```

安装的 CRDs:

```console
$ kubectl api-resources --api-group kamaji.clastix.io
NAME                   SHORTNAMES   APIVERSION                   NAMESPACED   KIND
datastores                          kamaji.clastix.io/v1alpha1   false        DataStore
kubeconfiggenerators   kc           kamaji.clastix.io/v1alpha1   false        KubeconfigGenerator
tenantcontrolplanes    tcp          kamaji.clastix.io/v1alpha1   true         TenantControlPlane
```

因为指定了 `--set datastore.enabled=true`, 因此生成了一个 DataStore:

```console
$ kubectl get datastore -n kamaji-system
NAME      DRIVER   READY   AGE
default   etcd     true    4m25s
```

没有 DataStore 将无法创建控制平面。

## 创建一个控制平面

控制平面由 TenantControlPlane 代表：

:::{literalinclude} /_files/macos/workspace/k8s/kamaji/tcp.yaml
:::

> [!IMPORTANT]
> 此处使用了 NodePort 类型的服务，实际还可以是 ClusterIP 或 LoadBanlancer. 注意当使用 NodePort 类型时，需要设置 `spec.networkProfile.address` 并且端口号必须在 30000-32767 范围内。其他两种则不需要设置 `address` 也不限制端口号。

将以上内容保存为文件 `tcp.yaml`, 应用到集群：

```console
$ kubectl create ns tenant-ns
namespace/tenant-ns created
$ kubectl apply -f tcp.yaml
tenantcontrolplane.kamaji.clastix.io/user-tcp created
```

结果：

```console
$ kubectl get tcp -n tenant-ns
NAME       VERSION   INSTALLED VERSION   STATUS   CONTROL-PLANE ENDPOINT   KUBECONFIG                  DATASTORE   AGE
user-tcp   v1.35.0   v1.35.0             Ready    10.220.70.56:30443       user-tcp-admin-kubeconfig   default     101s
```

Kamaji 根据 TenantControlPlane 的信息创建了控制平面的工作负载：

```console
$ kubectl get all -n tenant-ns
NAME                            READY   STATUS    RESTARTS   AGE
pod/user-tcp-664ffdf7d4-rkgxh   4/4     Running   0          3m7s
pod/user-tcp-664ffdf7d4-rtw68   4/4     Running   0          3m7s
pod/user-tcp-664ffdf7d4-tzpps   4/4     Running   0          3m7s

NAME               TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)           AGE
service/user-tcp   NodePort   10.99.115.123   <none>        30443:30443/TCP   3m25s

NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/user-tcp   3/3     3            3           3m9s

NAME                                  DESIRED   CURRENT   READY   AGE
replicaset.apps/user-tcp-664ffdf7d4   3         3         3       3m8s
replicaset.apps/user-tcp-67f69568f8   0         0         0       3m9s
replicaset.apps/user-tcp-6c46bfc594   0         0         0       3m9s
replicaset.apps/user-tcp-7f49c7b5b4   0         0         0       3m9s
```

Deployment 的详细信息：

```console
$ kubectl get deploy user-tcp -owide
NAME       READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS                                                                  IMAGES                                                                                                                                                                                 SELECTOR
user-tcp   3/3     3            3           4m13s   kube-apiserver,kube-scheduler,kube-controller-manager,konnectivity-server   registry.k8s.io/kube-apiserver:v1.35.0,registry.k8s.io/kube-scheduler:v1.35.0,registry.k8s.io/kube-controller-manager:v1.35.0,registry.k8s.io/kas-network-proxy/proxy-server:v0.35.0   kamaji.clastix.io/name=user-tcp
```

可见每一个 Pod 都包含了控制平面需要的所有组件，并且创建了 3 个副本。

## 访问新集群

虽然指定了控制平面的 IP, 但由于是 NodePort 类型的服务，实际上用任意节点 IP 都能访问到：

```console
$ curl -k https://10.220.70.56:30443/healthz
ok
$ curl -k https://10.220.70.56:30443/version 
{
  "major": "1",
  "minor": "35",
  "emulationMajor": "1",
  "emulationMinor": "35",
  "minCompatibilityMajor": "1",
  "minCompatibilityMinor": "34",
  "gitVersion": "v1.35.0",
  "gitCommit": "66452049f3d692768c39c797b21b793dce80314e",
  "gitTreeState": "clean",
  "buildDate": "2025-12-17T12:32:07Z",
  "goVersion": "go1.25.5",
  "compiler": "gc",
  "platform": "linux/amd64"
}
```

获得 admin kubeconfig:

```console
$ kubectl get secret user-tcp-admin-kubeconfig -n tenant-ns -ojsonpath='{.data.admin\.conf}' | base64 -D
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: ...
    server: https://10.220.70.56:6443
  name: user-tcp
contexts:
- context:
    cluster: user-tcp
    user: kubernetes-admin
  name: kubernetes-admin@user-tcp
current-context: kubernetes-admin@user-tcp
kind: Config
users:
- name: kubernetes-admin
  user:
    client-certificate-data: ...
    client-key-data: ...
```

将以上 kubeconfig 保存成文件 `user.kubeconfig`, 然后可以访问集群了：

```console
$ kubectl cluster-info --kubeconfig=user.kubeconfig
Kubernetes control plane is running at https://10.220.70.56:30443
CoreDNS is running at https://10.220.70.56:30443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
$ kubectl get ns --kubeconfig=user.kubeconfig
NAME              STATUS   AGE
default           Active   11m
kube-node-lease   Active   11m
kube-public       Active   11m
kube-system       Active   11m
$ kubectl get svc --kubeconfig=user.kubeconfig
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   11m
$ kubectl get no --kubeconfig=user.kubeconfig
No resources found
```

最后的信息表明集群内还没有 Worker 节点。可以用已知的方式向新的控制平面添加节点，比如用 `kubeadm`.
