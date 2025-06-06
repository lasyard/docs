# vCluster

<https://www.vcluster.com/>

## Install vCluster CLI command

```console
$ curl -LO https://github.com/loft-sh/vcluster/releases/download/v0.25.1-rc.3/vcluster-linux-amd64
```

```console
$ sudo install -c -m 0755 vcluster-linux-amd64 /usr/local/bin/vcluster
```

Check the version:

```console
$ vcluster --version
vcluster version 0.25.1
```

## Deploy a vcluster

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
