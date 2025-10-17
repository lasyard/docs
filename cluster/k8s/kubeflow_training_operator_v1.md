# Kubeflow Training Operator V1

## Install

```console
$ kubectl apply --server-side -k "github.com/kubeflow/trainer.git/manifests/overlays/standalone?ref=v1.9.3"
namespace/kubeflow serverside-applied
customresourcedefinition.apiextensions.k8s.io/jaxjobs.kubeflow.org serverside-applied
customresourcedefinition.apiextensions.k8s.io/mpijobs.kubeflow.org serverside-applied
customresourcedefinition.apiextensions.k8s.io/paddlejobs.kubeflow.org serverside-applied
customresourcedefinition.apiextensions.k8s.io/pytorchjobs.kubeflow.org serverside-applied
customresourcedefinition.apiextensions.k8s.io/tfjobs.kubeflow.org serverside-applied
customresourcedefinition.apiextensions.k8s.io/xgboostjobs.kubeflow.org serverside-applied
serviceaccount/training-operator serverside-applied
clusterrole.rbac.authorization.k8s.io/training-operator serverside-applied
clusterrolebinding.rbac.authorization.k8s.io/training-operator serverside-applied
secret/training-operator-webhook-cert serverside-applied
service/training-operator serverside-applied
deployment.apps/training-operator serverside-applied
validatingwebhookconfiguration.admissionregistration.k8s.io/validator.training-operator.kubeflow.org serverside-applied
```

Show depolyed workloads:

```console
$ kubectl get all -n kubeflow
NAME                                     READY   STATUS    RESTARTS   AGE
pod/training-operator-6577bb88bf-tgqz9   1/1     Running   0          73s

NAME                        TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)            AGE
service/training-operator   ClusterIP   10.100.99.45   <none>        8080/TCP,443/TCP   73s

NAME                                READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/training-operator   1/1     1            1           73s

NAME                                           DESIRED   CURRENT   READY   AGE
replicaset.apps/training-operator-6577bb88bf   1         1         1       73s
```

Show installed CRDs:

```console
$ kubectl get crd | grep kubeflow
jaxjobs.kubeflow.org                                  2025-10-13T08:27:15Z
mpijobs.kubeflow.org                                  2025-10-13T08:27:15Z
paddlejobs.kubeflow.org                               2025-10-13T08:27:16Z
pytorchjobs.kubeflow.org                              2025-10-13T08:27:16Z
tfjobs.kubeflow.org                                   2025-10-13T08:27:16Z
xgboostjobs.kubeflow.org                              2025-10-13T08:27:16Z
```

## Testing

Edit file `kf_pytorchjob.yaml`:

:::{literalinclude} /_files/macos/workspace/k8s/kf_pytorchjob.yaml
:::

Apply to the cluster:

```console
$ kubectl apply -f kf_pytorchjob.yaml 
pytorchjob.kubeflow.org/pytest created
```

Trace the state of job and pods:

```console
$ kubectl get pytorchjob -owide -w
NAME     STATE   AGE
pytest           0s
pytest   Created   0s
pytest   Running   1s
pytest   Running   5s
pytest   Running   5s
pytest   Running   5s
pytest   Succeeded   33s
pytest   Succeeded   33s
```

```console
$ kubectl get po -owide -w
NAME              READY   STATUS    RESTARTS   AGE   IP       NODE     NOMINATED NODE   READINESS GATES
pytest-master-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-master-0   0/1     Pending   0          0s    <none>   las3     <none>           <none>
pytest-worker-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-master-0   0/1     ContainerCreating   0          0s    <none>   las3     <none>           <none>
pytest-worker-0   0/1     Pending             0          0s    <none>   las2     <none>           <none>
pytest-worker-1   0/1     Pending             0          0s    <none>   <none>   <none>           <none>
pytest-worker-1   0/1     Pending             0          0s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Pending             0          0s    <none>   <none>   <none>           <none>
pytest-worker-2   0/1     Pending             0          0s    <none>   las3     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          0s    <none>   las2     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          0s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          0s    <none>   las3     <none>           <none>
pytest-master-0   0/1     ContainerCreating   0          1s    <none>   las3     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          1s    <none>   las3     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          1s    <none>   las2     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          1s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          1s    192.168.221.177   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          1s    192.168.185.45    las3     <none>           <none>
pytest-master-0   1/1     Running             0          1s    192.168.185.20    las3     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          2s    192.168.67.160    las2     <none>           <none>
pytest-worker-0   0/1     PodInitializing     0          4s    192.168.67.160    las2     <none>           <none>
pytest-worker-1   0/1     PodInitializing     0          4s    192.168.221.177   las1     <none>           <none>
pytest-worker-2   0/1     PodInitializing     0          4s    192.168.185.45    las3     <none>           <none>
pytest-worker-0   1/1     Running             0          5s    192.168.67.160    las2     <none>           <none>
pytest-worker-1   1/1     Running             0          5s    192.168.221.177   las1     <none>           <none>
pytest-worker-2   1/1     Running             0          5s    192.168.185.45    las3     <none>           <none>
pytest-master-0   0/1     Completed           0          31s   192.168.185.20    las3     <none>           <none>
pytest-master-0   0/1     Completed           0          33s   192.168.185.20    las3     <none>           <none>
pytest-master-0   0/1     Completed           0          33s   192.168.185.20    las3     <none>           <none>
pytest-worker-0   0/1     Completed           0          35s   192.168.67.160    las2     <none>           <none>
pytest-worker-1   0/1     Completed           0          35s   192.168.221.177   las1     <none>           <none>
pytest-worker-2   0/1     Completed           0          35s   192.168.185.45    las3     <none>           <none>
pytest-worker-0   0/1     Completed           0          36s   192.168.67.160    las2     <none>           <none>
pytest-worker-0   0/1     Completed           0          36s   192.168.67.160    las2     <none>           <none>
pytest-worker-1   0/1     Completed           0          36s   192.168.221.177   las1     <none>           <none>
pytest-worker-2   0/1     Completed           0          37s   192.168.185.45    las3     <none>           <none>
pytest-worker-1   0/1     Completed           0          37s   192.168.221.177   las1     <none>           <none>
pytest-worker-2   0/1     Completed           0          37s   192.168.185.45    las3     <none>           <none>
```

## Using volcano scheduler

Add an argument to the command of training operator:

```console
$ kubectl edit deployment.apps/training-operator -n kubeflow
deployment.apps/training-operator edited
```

The contents added:

:::{literalinclude} /_files/macos/console/kubectl/get_deploy_training_operator_kubeflow_volcano.txt
:diff: /_files/macos/console/kubectl/get_deploy_training_operator_kubeflow.txt
:::

After editing, the pods are restarted automatically. Then commit the job again and trace the state.

```console
$ kubectl get pytorchjob -owide -w
NAME     STATE   AGE
pytest           0s
pytest   Created   0s
pytest   Created   1s
pytest   Running   3s
pytest   Running   6s
pytest   Running   7s
pytest   Running   7s
pytest   Succeeded   35s
pytest   Succeeded   35s
```

```console
$ kubectl get podgroup -owide -w
NAME     STATUS   MINMEMBER   RUNNINGS   AGE   QUEUE
pytest            4                      0s    default
pytest   Inqueue   4                      0s    default
pytest   Running   4                      1s    default
pytest   Running   4           1          3s    default
pytest   Running   4           2          6s    default
pytest   Running   4           4          7s    default
pytest   Running   4           4          35s   default
```

```console
$ kubectl get po -owide -w
NAME              READY   STATUS    RESTARTS   AGE   IP       NODE     NOMINATED NODE   READINESS GATES
pytest-master-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-0   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-1   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-2   0/1     Pending   0          0s    <none>   <none>   <none>           <none>
pytest-worker-0   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-master-0   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Pending   0          1s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1   0          1s    <none>   las1     <none>           <none>
pytest-master-0   0/1     ContainerCreating   0          1s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          1s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          1s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          2s    <none>   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          2s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          2s    <none>   las1     <none>           <none>
pytest-master-0   0/1     ContainerCreating   0          2s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          2s    192.168.221.145   las1     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          2s    192.168.221.150   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          3s    192.168.221.144   las1     <none>           <none>
pytest-master-0   1/1     Running             0          3s    192.168.221.188   las1     <none>           <none>
pytest-worker-2   0/1     PodInitializing     0          5s    192.168.221.144   las1     <none>           <none>
pytest-worker-0   0/1     PodInitializing     0          5s    192.168.221.145   las1     <none>           <none>
pytest-worker-1   0/1     PodInitializing     0          5s    192.168.221.150   las1     <none>           <none>
pytest-worker-0   1/1     Running             0          6s    192.168.221.145   las1     <none>           <none>
pytest-worker-2   1/1     Running             0          6s    192.168.221.144   las1     <none>           <none>
pytest-worker-1   1/1     Running             0          6s    192.168.221.150   las1     <none>           <none>
pytest-master-0   0/1     Completed           0          34s   192.168.221.188   las1     <none>           <none>
pytest-master-0   0/1     Completed           0          35s   192.168.221.188   las1     <none>           <none>
pytest-master-0   0/1     Completed           0          35s   192.168.221.188   las1     <none>           <none>
pytest-worker-0   0/1     Completed           0          37s   192.168.221.145   las1     <none>           <none>
pytest-worker-1   0/1     Completed           0          37s   192.168.221.150   las1     <none>           <none>
pytest-worker-2   0/1     Completed           0          37s   192.168.221.144   las1     <none>           <none>
pytest-worker-1   0/1     Completed           0          38s   192.168.221.150   las1     <none>           <none>
pytest-worker-0   0/1     Completed           0          38s   192.168.221.145   las1     <none>           <none>
pytest-worker-2   0/1     Completed           0          38s   192.168.221.144   las1     <none>           <none>
pytest-worker-1   0/1     Completed           0          38s   192.168.221.150   las1     <none>           <none>
pytest-worker-0   0/1     Completed           0          38s   192.168.221.145   las1     <none>           <none>
pytest-worker-2   0/1     Completed           0          38s   192.168.221.144   las1     <none>           <none>
```

We can see a PodGroup of the same name is generated with correct `minMember` set, and all pods were scheduled to one node because of binpack policy.
