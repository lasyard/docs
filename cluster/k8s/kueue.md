# Kueue

<https://kueue.sigs.k8s.io/>

## Installation

By `helm`:

```console
$ helm pull oci://registry.k8s.io/kueue/charts/kueue
Pulled: registry.k8s.io/kueue/charts/kueue:0.15.2
Digest: sha256:7d8561f974a68965c51861ec308def52714e1bd99178c9f3d6013f489b7c8940
$ helm install kueue kueue-0.15.2.tgz --namespace kueue-system --create-namespace
NAME: kueue
LAST DEPLOYED: Tue Jan 13 14:12:04 2026
NAMESPACE: kueue-system
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

Show installed components:

```console
$ kubectl get svc,deploy -n kueue-system
NAME                                               TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
service/kueue-controller-manager-metrics-service   ClusterIP   10.110.105.166   <none>        8443/TCP   20s
service/kueue-visibility-server                    ClusterIP   10.107.10.50     <none>        443/TCP    20s
service/kueue-webhook-service                      ClusterIP   10.111.87.190    <none>        443/TCP    20s

NAME                                       READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/kueue-controller-manager   1/1     1            1           20s
```

Show installed CRDs:

```console
$ kubectl get crd | grep kueue
admissionchecks.kueue.x-k8s.io                        2026-01-13T06:12:07Z
clusterqueues.kueue.x-k8s.io                          2026-01-13T06:12:07Z
cohorts.kueue.x-k8s.io                                2026-01-13T06:12:07Z
localqueues.kueue.x-k8s.io                            2026-01-13T06:12:07Z
multikueueclusters.kueue.x-k8s.io                     2026-01-13T06:12:07Z
multikueueconfigs.kueue.x-k8s.io                      2026-01-13T06:12:07Z
provisioningrequestconfigs.kueue.x-k8s.io             2026-01-13T06:12:07Z
resourceflavors.kueue.x-k8s.io                        2026-01-13T06:12:07Z
topologies.kueue.x-k8s.io                             2026-01-13T06:12:07Z
workloadpriorityclasses.kueue.x-k8s.io                2026-01-13T06:12:07Z
workloads.kueue.x-k8s.io                              2026-01-13T06:12:07Z
```

Show installed API resources:

```console
$ kubectl api-resources --api-group=kueue.x-k8s.io
NAME                         SHORTNAMES          APIVERSION               NAMESPACED   KIND
admissionchecks                                  kueue.x-k8s.io/v1beta2   false        AdmissionCheck
clusterqueues                cq                  kueue.x-k8s.io/v1beta2   false        ClusterQueue
cohorts                                          kueue.x-k8s.io/v1beta2   false        Cohort
localqueues                  queue,queues,lq     kueue.x-k8s.io/v1beta2   true         LocalQueue
multikueueclusters                               kueue.x-k8s.io/v1beta2   false        MultiKueueCluster
multikueueconfigs                                kueue.x-k8s.io/v1beta2   false        MultiKueueConfig
provisioningrequestconfigs                       kueue.x-k8s.io/v1beta2   false        ProvisioningRequestConfig
resourceflavors              flavor,flavors,rf   kueue.x-k8s.io/v1beta2   false        ResourceFlavor
topologies                                       kueue.x-k8s.io/v1beta2   false        Topology
workloadpriorityclasses                          kueue.x-k8s.io/v1beta2   false        WorkloadPriorityClass
workloads                    wl                  kueue.x-k8s.io/v1beta2   true         Workload
```
