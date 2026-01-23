# Kubeflow Trainer

## Install

```console
$ helm pull oci://ghcr.io/kubeflow/charts/kubeflow-trainer
Pulled: ghcr.io/kubeflow/charts/kubeflow-trainer:2.1.0
Digest: sha256:2659823a63034cdd091ef70621c2d631a2ab64de5ec07ce2d5848f74baa5ee60
```

```console
$ helm install kubeflow-trainer kubeflow-trainer-2.1.0.tgz --namespace kubeflow-system --create-namespace
NAME: kubeflow-trainer
LAST DEPLOYED: Fri Jan 23 15:56:02 2026
NAMESPACE: kubeflow-system
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

Show deployed workloads:

```console
$ kubectl get all -n kubeflow-system
NAME                                                       READY   STATUS    RESTARTS   AGE
pod/jobset-controller-996545cf5-qhpvv                      0/1     Running   0          12s
pod/kubeflow-trainer-controller-manager-589f5f5945-gpgdg   0/1     Running   0          12s

NAME                                          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)            AGE
service/jobset-metrics-service                ClusterIP   10.103.19.211   <none>        8443/TCP           12s
service/jobset-webhook-service                ClusterIP   10.105.141.64   <none>        443/TCP            12s
service/kubeflow-trainer-controller-manager   ClusterIP   10.104.36.240   <none>        8080/TCP,443/TCP   12s

NAME                                                  READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/jobset-controller                     0/1     1            0           12s
deployment.apps/kubeflow-trainer-controller-manager   0/1     1            0           12s

NAME                                                             DESIRED   CURRENT   READY   AGE
replicaset.apps/jobset-controller-996545cf5                      1         1         0       12s
replicaset.apps/kubeflow-trainer-controller-manager-589f5f5945   1         1         0       12s
```

Show installed API resources:

```console
$ kubectl api-resources --api-group=trainer.kubeflow.org
NAME                      SHORTNAMES   APIVERSION                      NAMESPACED   KIND
clustertrainingruntimes                trainer.kubeflow.org/v1alpha1   false        ClusterTrainingRuntime
trainingruntimes                       trainer.kubeflow.org/v1alpha1   true         TrainingRuntime
trainjobs                              trainer.kubeflow.org/v1alpha1   true         TrainJob
```

## Install runtimes

```console
$ kubectl apply --server-side -k "https://github.com/kubeflow/trainer.git/manifests/overlays/runtimes?ref=master"
clustertrainingruntime.trainer.kubeflow.org/deepspeed-distributed serverside-applied
clustertrainingruntime.trainer.kubeflow.org/mlx-distributed serverside-applied
clustertrainingruntime.trainer.kubeflow.org/torch-distributed serverside-applied
clustertrainingruntime.trainer.kubeflow.org/torchtune-llama3.2-1b serverside-applied
clustertrainingruntime.trainer.kubeflow.org/torchtune-llama3.2-3b serverside-applied
clustertrainingruntime.trainer.kubeflow.org/torchtune-qwen2.5-1.5b serverside-applied
```

These ClusterTrainingRuntimes are installed:

```console
$ kubectl get clustertrainingruntimes
NAME                     AGE
deepspeed-distributed    78s
mlx-distributed          78s
torch-distributed        78s
torchtune-llama3.2-1b    78s
torchtune-llama3.2-3b    78s
torchtune-qwen2.5-1.5b   78s
```

The definition of `torch-distributed`:

````console
$ kubectl get clustertrainingruntimes torch-distributed -oyaml
apiVersion: trainer.kubeflow.org/v1alpha1
kind: ClusterTrainingRuntime
metadata:
  creationTimestamp: "2026-01-23T08:28:34Z"
  generation: 1
  labels:
    trainer.kubeflow.org/framework: torch
  name: torch-distributed
  resourceVersion: "82949790"
  uid: 189c4800-c269-4f7d-84e8-10ec27c8dbbf
spec:
  mlPolicy:
    numNodes: 1
    torch:
      numProcPerNode: auto
  template:
    spec:
      replicatedJobs:
      - groupName: default
        name: node
        replicas: 1
        template:
          metadata:
            labels:
              trainer.kubeflow.org/trainjob-ancestor-step: trainer
          spec:
            template:
              spec:
                containers:
                - image: pytorch/pytorch:2.9.1-cuda12.8-cudnn9-runtime
                  name: node
```

## Run a TrainJob

Submit a TrainJob:

:::{literalinclude} /_files/macos/workspace/k8s/kf_trainjob.yaml
:::

Show running workloads:

```console
$ kubectl get trainjob,jobset,job,pod -owide
NAME                                 STATE   AGE
trainjob.trainer.kubeflow.org/test           20s

NAME                          TERMINALSTATE   RESTARTS   COMPLETED   SUSPENDED   AGE
jobset.jobset.x-k8s.io/test                   0                      false       20s

NAME                    STATUS    COMPLETIONS   DURATION   AGE   CONTAINERS   IMAGES                 SELECTOR
job.batch/test-node-0   Running   0/3           20s        20s   node         busybox:1.37.0-glibc   batch.kubernetes.io/controller-uid=6fa15312-46fd-43f4-bb85-b73bd74fe079

NAME                      READY   STATUS    RESTARTS   AGE   IP                NODE   NOMINATED NODE   READINESS GATES
pod/test-node-0-0-bxjmh   1/1     Running   0          20s   192.168.185.5     las3   <none>           <none>
pod/test-node-0-1-xjszt   1/1     Running   0          20s   192.168.67.135    las2   <none>           <none>
pod/test-node-0-2-bgvx4   1/1     Running   0          20s   192.168.221.136   las1   <none>           <none>
```

## Integrate with Kueue

Kueue support TrainJob by default, just add the label:

:::{literalinclude} /_files/macos/workspace/k8s/kf_trainjob_kueue.yaml
:diff: /_files/macos/workspace/k8s/kf_trainjob.yaml
:::
