# Metrics Server

## Install

Using helm:

```console
$ helm pull metrics-server/metrics-server --version 3.12.2
$ helm upgrade --install metrics-server metrics-server-3.12.2.tgz -n metrics-server --create-namespace --set args="{\"--kubelet-insecure-tls\"}"
Release "metrics-server" does not exist. Installing it now.
NAME: metrics-server
LAST DEPLOYED: Fri Dec 19 16:39:57 2025
NAMESPACE: metrics-server
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
***********************************************************************
* Metrics Server                                                      *
***********************************************************************
  Chart version: 3.12.2
  App version:   0.7.2
  Image tag:     registry.k8s.io/metrics-server/metrics-server:v0.7.2
***********************************************************************
```

:::{note}
Argument `--kubelet-insecure-tls` is to skip TLS verify, because the cert is self signed if the cluster is depolyed by `kubeadm`.
:::

## Usage

```console
$ kubectl top no
NAME   CPU(cores)   CPU(%)   MEMORY(bytes)   MEMORY(%)   
las0   284m         1%       7489Mi          23%         
las1   209m         1%       5726Mi          17%         
las2   376m         2%       5283Mi          16%         
las3   114m         0%       15325Mi         47%         
$ kubectl top po
NAME                 CPU(cores)   MEMORY(bytes)   
small-sleep-task-0   0m           0Mi             
small-sleep-task-1   0m           0Mi             
small-sleep-task-2   0m           0Mi  
```
