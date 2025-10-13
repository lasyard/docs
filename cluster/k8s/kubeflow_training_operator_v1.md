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
pytest   Running   4s
pytest   Succeeded   63s
pytest   Succeeded   63s
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
pytest-worker-0   0/1     Init:0/1            0          0s    <none>   las2     <none>           <none>
pytest-worker-2   0/1     Pending             0          0s    <none>   las3     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          0s    <none>   las1     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          0s    <none>   las3     <none>           <none>
pytest-master-0   0/1     ContainerCreating   0          0s    <none>   las3     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          0s    <none>   las3     <none>           <none>
pytest-worker-1   0/1     Init:0/1            0          0s    <none>   las1     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          0s    <none>   las2     <none>           <none>
pytest-worker-2   0/1     Init:0/1            0          1s    192.168.185.36   las3     <none>           <none>
pytest-master-0   1/1     Running             0          1s    192.168.185.8    las3     <none>           <none>
pytest-worker-0   0/1     Init:0/1            0          1s    192.168.67.130   las2     <none>           <none>
pytest-worker-2   0/1     PodInitializing     0          3s    192.168.185.36   las3     <none>           <none>
pytest-worker-0   0/1     PodInitializing     0          3s    192.168.67.130   las2     <none>           <none>
pytest-worker-2   1/1     Running             0          4s    192.168.185.36   las3     <none>           <none>
pytest-worker-0   1/1     Running             0          4s    192.168.67.130   las2     <none>           <none>
pytest-master-0   0/1     Completed           0          61s   192.168.185.8    las3     <none>           <none>
pytest-master-0   0/1     Completed           0          62s   192.168.185.8    las3     <none>           <none>
pytest-master-0   0/1     Completed           0          63s   192.168.185.8    las3     <none>           <none>
pytest-worker-2   0/1     Completed           0          64s   192.168.185.36   las3     <none>           <none>
pytest-worker-0   0/1     Completed           0          65s   192.168.67.130   las2     <none>           <none>
pytest-worker-2   0/1     Completed           0          65s   192.168.185.36   las3     <none>           <none>
pytest-worker-2   0/1     Completed           0          66s   192.168.185.36   las3     <none>           <none>
pytest-worker-0   0/1     Completed           0          66s   192.168.67.130   las2     <none>           <none>
pytest-worker-0   0/1     Completed           0          66s   192.168.67.130   las2     <none>           <none>
```
