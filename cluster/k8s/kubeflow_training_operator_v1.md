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
pytest   Running   4s
pytest   Running   5s
pytest   Running   5s
pytest   Succeeded   33s
pytest   Succeeded   33s
```

```console
$ kubectl get po -w
NAME              READY   STATUS    RESTARTS   AGE
pytest-master-0   0/1     Pending   0          0s
pytest-master-0   0/1     Pending   0          0s
pytest-worker-0   0/1     Pending   0          0s
pytest-master-0   0/1     ContainerCreating   0          0s
pytest-worker-0   0/1     Pending             0          0s
pytest-worker-1   0/1     Pending             0          0s
pytest-worker-1   0/1     Pending             0          0s
pytest-worker-2   0/1     Pending             0          0s
pytest-worker-0   0/1     Init:0/1            0          0s
pytest-worker-2   0/1     Pending             0          0s
pytest-worker-1   0/1     Init:0/1            0          0s
pytest-worker-2   0/1     Init:0/1            0          0s
pytest-master-0   0/1     ContainerCreating   0          0s
pytest-worker-1   0/1     Init:0/1            0          0s
pytest-worker-2   0/1     Init:0/1            0          0s
pytest-worker-0   0/1     Init:0/1            0          0s
pytest-worker-0   0/1     Init:0/1            0          1s
pytest-worker-1   0/1     Init:0/1            0          1s
pytest-master-0   1/1     Running             0          1s
pytest-worker-2   0/1     Init:0/1            0          1s
pytest-worker-2   0/1     PodInitializing     0          3s
pytest-worker-0   0/1     PodInitializing     0          4s
pytest-worker-1   0/1     PodInitializing     0          4s
pytest-worker-2   1/1     Running             0          4s
pytest-worker-0   1/1     Running             0          5s
pytest-worker-1   1/1     Running             0          5s
pytest-master-0   0/1     Completed           0          31s
pytest-master-0   0/1     Completed           0          33s
pytest-master-0   0/1     Completed           0          33s
pytest-worker-2   0/1     Completed           0          34s
pytest-worker-0   0/1     Completed           0          35s
pytest-worker-1   0/1     Completed           0          35s
pytest-worker-2   0/1     Completed           0          35s
pytest-worker-2   0/1     Completed           0          36s
pytest-worker-0   0/1     Completed           0          36s
pytest-worker-0   0/1     Completed           0          36s
pytest-worker-1   0/1     Completed           0          36s
pytest-worker-1   0/1     Completed           0          36s
```

## Using volcano scheduler

To use volcano scheduler, `schedulerName` must be specified on each Pod (`template.spec`):

:::{literalinclude} /_files/macos/workspace/k8s/kf_pytorchjob_volcano.yaml
:diff: /_files/macos/workspace/k8s/kf_pytorchjob.yaml
:::

Then you can see the podgroup created:

```console
$ kubectl get podgroup -owide -w
NAME                                            STATUS    MINMEMBER   RUNNINGS   AGE   QUEUE
podgroup-ba6f1707-0bad-4b0e-9002-9519e504a87c   Pending   1                      0s    default
podgroup-ba6f1707-0bad-4b0e-9002-9519e504a87c   Running   1                      0s    default
podgroup-ba6f1707-0bad-4b0e-9002-9519e504a87c   Running   1           1          2s    default
podgroup-ba6f1707-0bad-4b0e-9002-9519e504a87c   Running   1           2          4s    default
podgroup-ba6f1707-0bad-4b0e-9002-9519e504a87c   Running   1           4          6s    default
podgroup-ba6f1707-0bad-4b0e-9002-9519e504a87c   Running   1           3          33s   default
podgroup-ba6f1707-0bad-4b0e-9002-9519e504a87c   Running   1           2          35s   default
podgroup-ba6f1707-0bad-4b0e-9002-9519e504a87c   Completed   1                      37s   default
```
