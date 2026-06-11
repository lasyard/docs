# vCluster

<https://www.vcluster.com/>

## Install vCluster CLI command

```console
$ curl -LO https://github.com/loft-sh/vcluster/releases/download/v0.25.1/vcluster-linux-amd64
```

```console
$ sudo install -c -m 0755 vcluster-linux-amd64 /usr/local/bin/vcluster
```

Check the version:

```console
$ vcluster --version
vcluster version 0.25.1
```

## Deploy a vcluster using CLI command

Before deployment, dowload this file to see which images are required:

```console
$ curl -LO https://github.com/loft-sh/vcluster/releases/download/v0.25.1/vcluster-images-k8s-1.32.txt
```

The contents of this file:

:::{literalinclude} /_files/macos/workspace/vcluster/vcluster-images-k8s-1.32.txt
:::

:::{tip}
You may need to prepare these images on each node in advance to accelerate the deployment, for example:

```console
$ sudo crictl pull ghcr.io/loft-sh/vcluster-pro:0.25.1
Image is up to date for sha256:0fec489cb9567ea62da1e369e2d4704836ae2c3f15c1a1a758e542a352977dae
```

:::{note}
A default StorageClass in the host cluster is needed to provision data volumes for vcluster pod.
:::

Deploy a vcluster:

```console
$ vcluster create my-vcluster --namespace team-x
10:38:56 info Creating namespace team-x
10:38:56 info Create vcluster my-vcluster...
10:38:56 info execute command: helm upgrade my-vcluster /tmp/vcluster-0.25.1.tgz-2892035011 --create-namespace --kubeconfig /tmp/2857282657 --namespace team-x --install --repository-config='' --values /tmp/2399122440
10:38:57 done Successfully created virtual cluster my-vcluster in namespace team-x
10:38:59 info Waiting for vcluster to come up...
...
10:45:30 done vCluster is up and running
Forwarding from 127.0.0.1:12893 -> 8443
Forwarding from [::1]:12893 -> 8443
Handling connection for 12893
10:45:30 done Switched active kube context to vcluster_my-vcluster_team-x_kubernetes-admin@las
10:45:30 warn Since you are using port-forwarding to connect, you will need to leave this terminal open
- Use CTRL+C to return to your previous kube context
- Use `kubectl get namespaces` in another terminal to access the vcluster
```

If the above command exits, you can redo port-forwarding by:

```console
$ vcluster connect my-vcluster
11:02:52 done vCluster is up and running
Forwarding from 127.0.0.1:10880 -> 8443
Forwarding from [::1]:10880 -> 8443
Handling connection for 10880
11:02:52 done Switched active kube context to vcluster_my-vcluster_team-x_kubernetes-admin@las
11:02:52 warn Since you are using port-forwarding to connect, you will need to leave this terminal open
- Use CTRL+C to return to your previous kube context
- Use `kubectl get namespaces` in another terminal to access the vcluster
```

:::{note}
The `.kube/config` is also altered on the host where the above command runs.
:::

List vclusters:

```console
$ vcluster list
  
       NAME     | NAMESPACE | STATUS  | VERSION | CONNECTED |  AGE    
  --------------+-----------+---------+---------+-----------+---------
    my-vcluster | team-x    | Running | 0.25.1  | True      | 59m12s  
  
11:38:08 info Run `vcluster disconnect` to switch back to the parent context
```

Switch back to the host cluster by:

```console
$ vcluster disconnect
10:56:12 info Successfully disconnected and switched back to the original context: kubernetes-admin@las
```

## Reconfigure

Apply new configuration file `vcluster.yaml`:

```console
$ vcluster create --upgrade my-vcluster -n team-x -f vcluster.yaml
11:09:49 info Upgrade vcluster my-vcluster...
11:09:49 info execute command: helm upgrade my-vcluster /tmp/vcluster-0.25.1.tgz-349102250 --create-namespace --kubeconfig /tmp/2765579640 --namespace team-x --install --repository-config='' --values /tmp/866114727 --values vcluster.yaml
11:09:50 done Successfully upgraded virtual cluster my-vcluster in namespace team-x
11:09:52 info Waiting for vcluster to come up...
11:10:28 done vCluster is up and running
Forwarding from 127.0.0.1:11027 -> 8443
Forwarding from [::1]:11027 -> 8443
Handling connection for 11027
11:10:29 done Switched active kube context to vcluster_my-vcluster_team-x_kubernetes-admin@las
11:10:29 warn Since you are using port-forwarding to connect, you will need to leave this terminal open
- Use CTRL+C to return to your previous kube context
- Use `kubectl get namespaces` in another terminal to access the vcluster
```

## Delete

Delete the vcluster:

```console
$ vcluster delete my-vcluster --namespace team-x
09:41:01 info Delete vcluster my-vcluster...
09:41:02 done Successfully deleted virtual cluster my-vcluster in namespace team-x
09:41:02 done Successfully deleted virtual cluster namespace team-x
09:41:02 info Waiting for virtual cluster to be deleted...
09:41:14 done Virtual Cluster is deleted
```

## Manage vcluster by helm

Add the repository:

```console
$ helm repo add vcluster https://charts.loft.sh
$ helm repo update
```

Get the chart:

```console
$ helm pull vcluster/vcluster --version 0.30.0
```

Install a new vcluster:

```console
$ helm upgrade --install my-vcluster vcluster-0.30.0.tgz --namespace team-x --create-namespace
Release "my-vcluster" does not exist. Installing it now.
NAME: my-vcluster
LAST DEPLOYED: Tue Jun  9 11:27:57 2026
NAMESPACE: team-x
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

> [!NOTE]
> Need a default StorageClass to provision pv for etcd storage.

Show the workloads:

```console
$ kubectl get all -n team-x
NAME                                                     READY   STATUS    RESTARTS   AGE
pod/coredns-75bb76df-xpxdh-x-kube-system-x-my-vcluster   1/1     Running   0          42s
pod/my-vcluster-0                                        1/1     Running   0          13m

NAME                                           TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                  AGE
service/kube-dns-x-kube-system-x-my-vcluster   ClusterIP   10.96.99.177     <none>        53/UDP,53/TCP,9153/TCP   42s
service/my-vcluster                            ClusterIP   10.100.32.158    <none>        443/TCP,10250/TCP        13m
service/my-vcluster-headless                   ClusterIP   None             <none>        443/TCP                  13m
service/my-vcluster-node-las1                  ClusterIP   10.106.189.191   <none>        10250/TCP                42s

NAME                           READY   AGE
statefulset.apps/my-vcluster   1/1     13m
```

A secret stores the kubeconfig to access the vcluster:

```console
$ kubectl get secret vc-my-vcluster -n team-x
NAME             TYPE     DATA   AGE
vc-my-vcluster   Opaque   5      5m1s
```

Get the kubeconfig:

```console
$ kubectl get secret vc-my-vcluster -n team-x -ojsonpath='{.data.config}' | base64 -D
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: ...
    server: https://localhost:8443
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: kubernetes-super-admin
  name: kubernetes-super-admin@kubernetes
current-context: kubernetes-super-admin@kubernetes
kind: Config
users:
- name: kubernetes-super-admin
  user:
    client-certificate-data: ...
    client-key-data: ...
```

Save the output to a file, named to `kubeconfig`. Port forwarding the Kube API service to the server address in the kubeconfig:

```console
$ kubectl port-forward service/my-vcluster 8443:443 -n team-x
Forwarding from 127.0.0.1:8443 -> 8443
Forwarding from [::1]:8443 -> 8443
```

Show cluster info:

```console
$ KUBECONFIG=kubeconfig kubectl cluster-info
Kubernetes control plane is running at https://localhost:8443
CoreDNS is running at https://localhost:8443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
$ KUBECONFIG=kubeconfig kubectl get no -owide
NAME   STATUS   ROLES    AGE     VERSION   INTERNAL-IP      EXTERNAL-IP   OS-IMAGE                KERNEL-VERSION      CONTAINER-RUNTIME
las1   Ready    <none>   4h45m   v1.34.0   10.106.189.191   <none>        Fake Kubernetes Image   4.19.76-fakelinux   docker://19.3.12
```

## Customization

By setting values when installing with helm, we can customize the new vcluster. But many features are restricted by licenses.

An example of value file:

:::{literalinclude} /_files/macos/workspace/vcluster/my_vcluster.yaml
:::

Name it to `my_vcluster.yaml`, install a new vcluster by:

```console
$ helm upgrade --install my-vcluster vcluster-0.30.0.tgz --namespace team-x --create-namespace -f my_vcluster.yaml
```

By adjust the startup command args, we turn on debug logs for `api-server`, `controller-manager`, `scheduler` and `kine`.
