# Cilium

<https://cilium.io/>

## Install Cilium CLI

:::::{tab-set}
::::{tab-item} macOS
:sync: macos

Download the tar ball:

```console
$ curl -LO https://github.com/cilium/cilium-cli/releases/download/v0.20.1/cilium-darwin-arm64.tar.gz
$ curl -LO https://github.com/cilium/cilium-cli/releases/download/v0.20.1/cilium-darwin-arm64.tar.gz.sha256sum
$ shasum -a 256 -c cilium-darwin-arm64.tar.gz.sha256sum 
cilium-darwin-arm64.tar.gz: OK
```

Install:

```console
$ sudo tar -C /usr/local/bin -xzf cilium-darwin-arm64.tar.gz
```

::::
:::::

```console
$ cilium version
cilium-cli: v0.20.1 compiled with go1.27.1 on darwin/arm64
cilium image (default): v1.20.1
cilium image (stable): v1.20.4
cilium image (running): 1.20.1
```

## Install Cilium In Current {{k8s}}

```console
$ cilium install 1.20.4
ℹ️  Using Cilium version 1.20.1
🔮 Auto-detected cluster name: las
🔮 Auto-detected kube-proxy has been installed
```

This means `kube-proxy` is already installed. Cilium can co-exist with `kube-proxy`, or replace it totally.

Now uninstall Cilium:

```console
$ cilium uninstall
🔥 Deleting pods in cilium-test namespace...
🔥 Deleting cilium-test namespace...
⌛ Uninstalling Cilium
🔥 Deleting pods in cilium-test namespace...
🔥 Deleting cilium-test namespace...
🔥 Cleaning up Cilium node annotations...
```

Remove `kube-proxy` from the cluster:

```console
$ kubectl -n kube-system delete ds kube-proxy
daemonset.apps "kube-proxy" deleted from kube-system namespace
$ kubectl -n kube-system delete cm kube-proxy
configmap "kube-proxy" deleted from kube-system namespace
```

Reinstall Cilium:

```console
$ cilium install 1.20.4
ℹ️  Using Cilium version 1.20.1
🔮 Auto-detected cluster name: las
🔮 Auto-detected kube-proxy has not been installed
ℹ️  Cilium will fully replace all functionalities of kube-proxy
```

In this case, the duty of `kube-proxy` is taken over by Cilium. Verify it in the Cilium config:

```console
$ kubectl get cm cilium-config -n kube-system -ojsonpath='{.data.kube-proxy-replacement}'
true
```

Or run the debug utility to see the config:

```console
$ kubectl -n kube-system exec ds/cilium -- cilium-dbg status
```

> [!TIP]
> Add `--verbose` to the above command to see more useful info.

The installation command actually use `helm` to install:

```console
$ helm list -n kube-system
NAME    NAMESPACE   REVISION    UPDATED                                 STATUS      CHART           APP VERSION
cilium  kube-system 1           2026-11-04 17:55:52.767124 +0800 CST    deployed    cilium-1.20.1   1.20.1
```

Installed workloads:

```console
$ kubectl get svc,ds,deploy -n kube-system
NAME                   TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                  AGE
service/cilium-envoy   ClusterIP   None            <none>        9964/TCP                 7m53s
service/hubble-peer    ClusterIP   10.104.202.33   <none>        443/TCP                  7m53s
service/kube-dns       ClusterIP   10.96.0.10      <none>        53/UDP,53/TCP,9153/TCP   62d

NAME                          DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
daemonset.apps/cilium         2         2         2       2            2           kubernetes.io/os=linux   7m53s
daemonset.apps/cilium-envoy   2         2         2       2            2           kubernetes.io/os=linux   7m53s

NAME                              READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/cilium-operator   1/1     1            1           7m53s
deployment.apps/coredns           2/2     2            2           62d
```

## Hubble

### Enable Hubble

```console
$ cilium hubble enable
```

### Disable Hubble

```console
$ cilium hubble disable
```

### Install Hubble CLI

:::::{tab-set}
::::{tab-item} macOS
:sync: macos

Download the binaries:

```console
$ curl -LO https://github.com/cilium/hubble/releases/download/v1.20.2/hubble-darwin-arm64.tar.gz
$ curl -LO https://github.com/cilium/hubble/releases/download/v1.20.2/hubble-darwin-arm64.tar.gz.sha256sum
$ shasum -a 256 -c hubble-darwin-arm64.tar.gz.sha256sum
hubble-darwin-arm64.tar.gz: OK
```

Install:

```console
$ sudo tar -C /usr/local/bin -xzf hubble-darwin-arm64.tar.gz
```

::::
:::::

Check the status:

```console
$ hubble status -P
Healthcheck (via 127.0.0.1:4245): Ok
Current/Max Flows: 8,190/8,190 (100.00%)
Flows/s: 125.15
Connected Nodes: 2/2
```

> [!TIP]
> The `-P` is for port-forward. You can omit it if you do forwarding in another console:
>
> ```console
> $ cilium hubble port-forward
> ℹ️  Hubble Relay is available at 127.0.0.1:4245
> ```

### Enable Hubble UI

```console
$ cilium hubble enable --ui
```

Then open the UI:

```console
$ cilium hubble ui
ℹ️  Opening "http://localhost:12000" in your browser...
```

## Status

Now the status of Cilium:

```console
$ cilium status
    /¯¯\
 /¯¯\__/¯¯\    Cilium:             OK
 \__/¯¯\__/    Operator:           OK
 /¯¯\__/¯¯\    Envoy DaemonSet:    OK
 \__/¯¯\__/    Hubble Relay:       OK
    \__/       ClusterMesh:        disabled

DaemonSet              cilium                   Desired: 2, Ready: 2/2, Available: 2/2
DaemonSet              cilium-envoy             Desired: 2, Ready: 2/2, Available: 2/2
Deployment             cilium-operator          Desired: 1, Ready: 1/1, Available: 1/1
Deployment             hubble-relay             Desired: 1, Ready: 1/1, Available: 1/1
Deployment             hubble-ui                Desired: 1, Ready: 1/1, Available: 1/1
Containers:            cilium                   Running: 2
                       cilium-envoy             Running: 2
                       cilium-operator          Running: 1
                       clustermesh-apiserver    
                       hubble-relay             Running: 1
                       hubble-ui                Running: 1
Cluster Pods:          4/4 managed by Cilium
Helm chart version:    1.20.1
Image versions         cilium             quay.io/cilium/cilium:v1.20.1@sha256:ae9ea21f7427fe24bc6ea7247eb552157a1b0a431744045d3f641545ca71d11b: 2
                       cilium-envoy       quay.io/cilium/cilium-envoy:v1.37.5-1786810558-766ccfb37260a43e9d228837aa84ce3faf9f64e7@sha256:75b8094c7127736a2ffd2dce3945e0931cb6df21b0372ff661940eca26730b91: 2
                       cilium-operator    quay.io/cilium/operator-generic:v1.20.1@sha256:6c3885fc7b629099fdbe2a5c87869c86feb825fa18fae299eac0f61918d16ecf: 1
                       hubble-relay       quay.io/cilium/hubble-relay:v1.20.1@sha256:59be0ae7d475ab9011a5e954618c0f27b5778b17140381425b308b55ba4917f4: 1
                       hubble-ui          quay.io/cilium/hubble-ui-backend:v0.13.5@sha256:fac0c300ae119274edca11fd89b1ad23c788792d8bc4ea2ba631c709e8d3c688: 1
                       hubble-ui          quay.io/cilium/hubble-ui:v0.13.5@sha256:f7d514fc54d784ed6df9d58cf0e97648b143f92b766dd1780ed3fc845bd4c516: 1
```

## IPAM mode

If you set `networking.podSubnet` when doing `kubeadm init` to deploy the cluster, for each node, there will be specs of `podCIDR` and `podCIDRs`:

```console
$ kubectl get no -o custom-columns='NAME:.metadata.name,POD-CIDR:spec.podCIDR,POD-CIDRS:spec.podCIDRs'
NAME   POD-CIDR         POD-CIDRS
las0   192.168.0.0/24   [192.168.0.0/24]
las1   192.168.1.0/24   [192.168.1.0/24]
```

But Cilium's default IPAM mode is `cluster-pool`, which ignores these specs. You can check the `CiliumNode` resources to see the actual IPs:

```console
$ kubectl get cn
NAME   CILIUMINTERNALIP   INTERNALIP    AGE
las0   10.0.1.188         10.225.4.51   13m
las1   10.0.0.66          10.225.4.52   13m
```

And the IPs of each Cilium managed pods by checking `CiliumEndpoint`:

```console
$ kubectl get cep -n kube-system
NAME                            SECURITY IDENTITY   ENDPOINT STATE   IPV4         IPV6
coredns-77b678d576-c9rsp        30461               ready            10.0.0.117   
coredns-77b678d576-p6drq        30461               ready            10.0.1.220   
hubble-relay-79b5b4b5f4-lq26s   60659               ready            10.0.0.67    
hubble-ui-74b4645b7f-8rkv7      9497                ready            10.0.0.253
```

Note the default CIDR for pods overlaps with `serviceSubnet` of the cluster:

```console
$ kubectl -n kube-system get cm cilium-config -ojsonpath='{.data.cluster-pool-ipv4-cidr}'
10.0.0.0/8
```

To respect the specs, IPAM mode must be set to `kubernetes`. You can do this when installing Cilium, or upgrade it:

```console
$ cilium upgrade --set ipam.mode=kubernetes  
ℹ️  Using Cilium version 1.20.1
🔮 Auto-detected cluster name: las
🔮 Auto-detected kube-proxy has not been installed
ℹ️  Cilium will fully replace all functionalities of kube-proxy
⚠️  You maybe need to restart Cilium pods for configmap changes to take effect
```

Then restart all Cilium components:

```console
$ kubectl -n kube-system rollout restart ds/cilium deploy/cilium-operator
daemonset.apps/cilium restarted
deployment.apps/cilium-operator restarted
```

These are `CiliumNode` resources created for each node. These must be deleted and will be created automatically when needed:

```console
$ kubeclt delete cn --all
ciliumnode.cilium.io "las0" deleted
ciliumnode.cilium.io "las1" deleted
```

Then restart each pod managed by Cilium to get new IPs.

## Best Practise

Need not set `podSubnet` when deploy {{k8s}}. Keep IPAM mode `cluster-pool` but set the ip pool explicitly to avoid collision with service CIDR:

```console
$ cilium install 1.20.4 \
  --set ipam.mode=cluster-pool \
  --set ipam.operator.clusterPoolIPv4PodCIDRList='{192.168.0.0/16}' \
  --set ipam.operator.clusterPoolIPv4MaskSize=24
```
