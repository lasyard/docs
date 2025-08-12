# KAI Scheduler

<https://github.com/NVIDIA/KAI-Scheduler>

## Install

Using `helm`. Download the chart:

```console
$ helm pull oci://ghcr.io/nvidia/kai-scheduler/kai-scheduler --version v0.7.12
Pulled: ghcr.io/nvidia/kai-scheduler/kai-scheduler:v0.7.12
Digest: sha256:1287e121e6c0b01c6e874fd104f8d36487ce0b773880bdc80d95ec5ab7f2c94a
```

Install:

```console
$ helm upgrade -i kai-scheduler -n kai-scheduler --create-namespace kai-scheduler-v0.7.12.tgz
Release "kai-scheduler" does not exist. Installing it now.
NAME: kai-scheduler
LAST DEPLOYED: Mon Aug 11 14:42:24 2025
NAMESPACE: kai-scheduler
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

Show the resources:

```console
$ kubectl get all -n kai-scheduler
NAME                                       READY   STATUS    RESTARTS   AGE
pod/binder-55549f8c66-4qltk                1/1     Running   0          7m55s
pod/podgroup-controller-7f57b65444-42d8m   1/1     Running   0          7m55s
pod/podgrouper-d4b78b659-zcjnf             1/1     Running   0          7m55s
pod/queuecontroller-89dcbd6d4-ss5tp        1/1     Running   0          7m55s
pod/scheduler-5f8dd8d9c9-9448w             1/1     Running   0          7m55s

NAME                      TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)            AGE
service/binder            ClusterIP   10.103.78.230    <none>        443/TCP,8080/TCP   7m55s
service/queuecontroller   ClusterIP   10.109.35.28     <none>        443/TCP,8080/TCP   7m55s
service/scheduler         ClusterIP   10.106.100.152   <none>        8080/TCP           7m55s

NAME                                  READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/binder                1/1     1            1           7m55s
deployment.apps/podgroup-controller   1/1     1            1           7m55s
deployment.apps/podgrouper            1/1     1            1           7m55s
deployment.apps/queuecontroller       1/1     1            1           7m55s
deployment.apps/scheduler             1/1     1            1           7m55s

NAME                                             DESIRED   CURRENT   READY   AGE
replicaset.apps/binder-55549f8c66                1         1         1       7m55s
replicaset.apps/podgroup-controller-7f57b65444   1         1         1       7m55s
replicaset.apps/podgrouper-d4b78b659             1         1         1       7m55s
replicaset.apps/queuecontroller-89dcbd6d4        1         1         1       7m55s
replicaset.apps/scheduler-5f8dd8d9c9             1         1         1       7m55s
```

## Usage

### Create queues

Create file `default_test_queue.yaml` for queues:

:::{literalinclude} /_files/macos/workspace/k8s/default_test_queue.yaml
:::

Apply it:

```console
$ kubectl apply -f default_test_queue.yaml
queue.scheduling.run.ai/default created
queue.scheduling.run.ai/test created
```

Show the created queues:

```console
$ kubectl get queue       
NAME      PRIORITY   PARENT    CHILDREN   DISPLAYNAME
default                        ["test"]   
test                 default          
```

### Create pods

Create file `sleep_po_kai.yaml`, based on the pod config in <project:res/pod.md>, with these modifications:

:::{literalinclude} /_files/macos/workspace/k8s/sleep_po_kai.yaml
:diff: /_files/macos/workspace/k8s/sleep_po.yaml
:::

Apply it:

```console
$ kubectl apply -f sleep_po_kai.yaml
pod/sleep created
```
