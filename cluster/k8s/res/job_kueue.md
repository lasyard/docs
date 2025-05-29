# Job with kueue

Install kueue first, see <https://kueue.sigs.k8s.io/>. By `helm`:

```console
$ helm pull oci://registry.k8s.io/kueue/charts/kueue --version=0.11.4
Pulled: registry.k8s.io/kueue/charts/kueue:0.11.4
Digest: sha256:0c58ed6e88716c90da94dce0351694b8788552421c63f0c30739ed5bc8bb659c
$ helm install kueue kueue-0.11.4.tgz --namespace kueue-system --create-namespace
NAME: kueue
LAST DEPLOYED: Sun Apr 27 03:49:12 2025
NAMESPACE: kueue-system
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

Create file `topology_rf_cq_lq.yaml` for some `kueue` staffs:

:::{literalinclude} /_files/macos/workspace/k8s/topology_rf_cq_lq.yaml
:::

:::{note}
For `ResourceFlavor`, At least one of `nodeLabels` is required if `topologyName` is set. That means, the correct label must be set to schedule pods on the expected nodes before running jobs:

```console
$ kubectl label node --all node-group=default
node/las1 labeled
node/las2 labeled
node/las0 labeled
node/las3 labeled
```

:::

Apply to the cluster:

```console
$ kubectl apply -f topology_rf_cq_lq.yaml
topology.kueue.x-k8s.io/default created
resourceflavor.kueue.x-k8s.io/default created
clusterqueue.kueue.x-k8s.io/test created
localqueue.kueue.x-k8s.io/test created
```

See what are created:

```console
$ kubectl get topology,rf,cq,lq -owide
NAME                              AGE
topology.kueue.x-k8s.io/default   2m20s

NAME                                    AGE
resourceflavor.kueue.x-k8s.io/default   2m20s

NAME                               COHORT   STRATEGY         PENDING WORKLOADS   ADMITTED WORKLOADS
clusterqueue.kueue.x-k8s.io/test            BestEffortFIFO   0                   0

NAME                             CLUSTERQUEUE   PENDING WORKLOADS   ADMITTED WORKLOADS
localqueue.kueue.x-k8s.io/test   test           0                   0
```

Now create file `sleep_job_kueue.yaml`:

:::{literalinclude} /_files/macos/workspace/k8s/sleep_job_kueue.yaml
:::

Apply to the cluster:

```console
$ kubectl create -f sleep_job_kueue.yaml
job.batch/sleep-85sck created
$ kubectl create -f sleep_job_kueue.yaml
job.batch/sleep-mrbcc created
```

Show events:

```console
$ kubectl get job -owide -w
NAME          STATUS      COMPLETIONS   DURATION   AGE   CONTAINERS      IMAGES                 SELECTOR
sleep-85sck   Running     0/3           0s         0s    sleep-busybox   busybox:1.37.0-glibc   batch.kubernetes.io/controller-uid=2eb95f91-11df-43a0-9285-b180904f7030
sleep-mrbcc   Suspended   0/3                      0s    sleep-busybox   busybox:1.37.0-glibc   batch.kubernetes.io/controller-uid=49f34454-601a-4a40-a9bb-dcfd457b0bb0
sleep-85sck   Running     0/3           1s         1s    sleep-busybox   busybox:1.37.0-glibc   batch.kubernetes.io/controller-uid=2eb95f91-11df-43a0-9285-b180904f7030
sleep-85sck   Running     0/3           2s         2s    sleep-busybox   busybox:1.37.0-glibc   batch.kubernetes.io/controller-uid=2eb95f91-11df-43a0-9285-b180904f7030
sleep-85sck   Running     0/3           62s        62s   sleep-busybox   busybox:1.37.0-glibc   batch.kubernetes.io/controller-uid=2eb95f91-11df-43a0-9285-b180904f7030
sleep-85sck   Running     2/3           63s        63s   sleep-busybox   busybox:1.37.0-glibc   batch.kubernetes.io/controller-uid=2eb95f91-11df-43a0-9285-b180904f7030
sleep-mrbcc   Suspended   0/3                      63s   sleep-busybox   busybox:1.37.0-glibc   batch.kubernetes.io/controller-uid=49f34454-601a-4a40-a9bb-dcfd457b0bb0
sleep-mrbcc   Running     0/3           0s         63s   sleep-busybox   busybox:1.37.0-glibc   batch.kubernetes.io/controller-uid=49f34454-601a-4a40-a9bb-dcfd457b0bb0
sleep-85sck   Running     3/3           64s        64s   sleep-busybox   busybox:1.37.0-glibc   batch.kubernetes.io/controller-uid=2eb95f91-11df-43a0-9285-b180904f7030
sleep-85sck   Complete    3/3           64s        64s   sleep-busybox   busybox:1.37.0-glibc   batch.kubernetes.io/controller-uid=2eb95f91-11df-43a0-9285-b180904f7030
sleep-mrbcc   Running     0/3           1s         64s   sleep-busybox   busybox:1.37.0-glibc   batch.kubernetes.io/controller-uid=49f34454-601a-4a40-a9bb-dcfd457b0bb0
sleep-mrbcc   Running     0/3           2s         65s   sleep-busybox   busybox:1.37.0-glibc   batch.kubernetes.io/controller-uid=49f34454-601a-4a40-a9bb-dcfd457b0bb0
```
