# KubeRay Operator

## Install

### By Helm

```console
$ helm repo add kuberay https://ray-project.github.io/kuberay-helm/
"kuberay" has been added to your repositories
$ helm repo update
$ helm pull kuberay/kuberay-operator
```

```console
$ helm install kuberay kuberay-operator-1.6.0.tgz -n kuberay --create-namespace
NAME: kuberay
LAST DEPLOYED: Tue Apr  7 14:59:15 2026
NAMESPACE: kuberay
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

Show installed workloads:

```console
$ kubectl get all -n kuberay
NAME                                    READY   STATUS    RESTARTS   AGE
pod/kuberay-operator-7c458bbb56-lf8ql   1/1     Running   0          33s

NAME                       TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
service/kuberay-operator   ClusterIP   10.106.211.164   <none>        8080/TCP   33s

NAME                               READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/kuberay-operator   1/1     1            1           33s

NAME                                          DESIRED   CURRENT   READY   AGE
replicaset.apps/kuberay-operator-7c458bbb56   1         1         1       33s
```

Show installed API resources:

```console
$ kubectl api-resources --api-group=ray.io   
NAME          SHORTNAMES   APIVERSION   NAMESPACED   KIND
rayclusters                ray.io/v1    true         RayCluster
raycronjobs                ray.io/v1    true         RayCronJob
rayjobs                    ray.io/v1    true         RayJob
rayservices                ray.io/v1    true         RayService
```

## Install a ray cluster

Again, by helm:

```console
$ helm pull kuberay/ray-cluster
```

Install (with autoscaler enabled):

```console
$ helm install ray-cluster ray-cluster-1.6.0.tgz --set head.rayStartParams.num-cpus=0 --set worker.rayStartParams.num-cpus=1 --set head.enableInTreeAutoscaling=true --set worker.replicas=0 --set worker.maxReplicas=50
NAME: ray-cluster
LAST DEPLOYED: Tue Apr  7 15:58:39 2026
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

Show the workloads:

```console
$ kubectl get raycluster,po
NAME                                    DESIRED WORKERS   AVAILABLE WORKERS   CPUS   MEMORY   GPUS   STATUS   AGE
raycluster.ray.io/ray-cluster-kuberay   1                 1                   1      5Gi      0      ready    58s

NAME                                               READY   STATUS    RESTARTS   AGE
pod/ray-cluster-kuberay-head-ftv6k                 2/2     Running   0          58s
pod/ray-cluster-kuberay-workergroup-worker-xldnq   1/1     Running   0          58s
```

:::{note}

- The autoscaler run as a sidecar in the head pod, so there are two containers.
- Though `worker.replicas` set to 1, there is still one worker started.

:::

Show the service:

```console
$ kubectl get svc -lapp.kubernetes.io/name=kuberay
NAME                           TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)                                         AGE
ray-cluster-kuberay-head-svc   ClusterIP   None         <none>        10001/TCP,8265/TCP,6379/TCP,8080/TCP,8000/TCP   2m
```

Check ray status on the head node:

```console
$ kubectl exec -it $(kubectl get pods --selector=ray.io/node-type=head -o custom-columns=POD:metadata.name --no-headers) -- ray status
efaulted container "ray-head" out of: ray-head, autoscaler
======== Autoscaler status: 2026-04-07 02:41:37.379691 ========
Node status
---------------------------------------------------------------
Active:
 (no active nodes)
Idle:
 1 headgroup
 1 workergroup
Pending:
 (no pending nodes)
Recent failures:
 (no failures)

Resources
---------------------------------------------------------------
Total Usage:
 0.0/1.0 CPU
 0B/6.00GiB memory
 0B/1.52GiB object_store_memory

From request_resources:
 (none)
Pending Demands:
 (no resource demands)
```

## Submit a job

Forward the service port:

```console
$ kubectl port-forward service/ray-cluster-kuberay-head-svc 8265:8265 > /dev/null &
```

Then submit a job:

```console
$ ray job submit --address http://localhost:8265 --working-dir . -- python count_hosts.py
```

You will see the number of workers increased when running and decreased after the job is done.
