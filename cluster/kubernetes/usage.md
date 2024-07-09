# Kubernetes Usage

## Token management

List all tokens:

```sh
kubeadm token list
```

{.cli-output}

```text
TOKEN                     TTL         EXPIRES                USAGES                   DESCRIPTION                                                EXTRA GROUPS
abcdef.0123456789abcdef   23h         2024-05-31T07:17:11Z   authentication,signing   <none>                                                     system:bootstrappers:kubeadm:default-node-token
```

The tokens can be seen also by running:

```sh
kubectl get secrets -n kube-system
```

{.cli-output}

```text
NAME                     TYPE                            DATA   AGE
bootstrap-token-abcdef   bootstrap.kubernetes.io/token   6      12m
```

Delete a token:

```sh
kubeadm token delete abcdef.0123456789abcdef
```

or by deleting the secret:

```sh
kubectl delete secret bootstrap-token-abcdef -n kube-system
```

Create a new token with a 24-hour expiration and print the `join` command:

```sh
kubeadm token create --print-join-command --ttl 24h
```

## ConfigMap

Create a properties file:

```sh
vi slurm.properties
```

:::{literalinclude} /_files/common/work/slurm.properties
:language: properties
:class: file-content
:::

Create a ConfigMap from it:

```sh
kubectl create configmap slurm-config --from-file=slurm.properties
```

Show ConfigMaps:

```sh
kubectl get configmaps
```

:::{literalinclude} /_files/centos/output/kubectl/get_configmaps_1.txt
:language: text
:class: cli-output
:::

See the details of the new ConfigMap:

```sh
kubectl describe configmap slurm-config
```

:::{literalinclude} /_files/centos/output/kubectl/describe_configmap_1.txt
:language: text
:class: cli-output
:::

Alternatively, you can check the data by:

```sh
kubectl get configmap slurm-config -o yaml
```

:::{literalinclude} /_files/centos/output/kubectl/get_configmap.yaml
:language: yaml
:class: cli-output
:::

If you want to break the content of `.properties` file into multiple ConfigMap keys, you can use:

```sh
kubectl create configmap slurm-config --from-env-file=slurm.properties
```

```sh
kubectl get configmaps
```

:::{literalinclude} /_files/centos/output/kubectl/get_configmaps_5.txt
:language: text
:class: cli-output
:::

```sh
kubectl describe configmap slurm-config
```

:::{literalinclude} /_files/centos/output/kubectl/describe_configmap_5.txt
:language: text
:class: cli-output
:::

Note the difference.

## Console of pods

```sh
kubectl exec -it slurm-client -- /bin/bash
```

## crictl

```sh
crictl --version
```

{.cli-output}

```text
crictl version v1.30.0
```

Set config:

```sh
crictl config --set image-endpoint=unix:///run/containerd/containerd.sock
crictl config --set runtime-endpoint=unix:///run/containerd/containerd.sock
```

Show config:

```sh
crictl config --list
```

:::{literalinclude} /_files/centos/output/crictl/config_list.txt
:language: text
:class: cli-output
:::

:::{tip}
Configurations are stored in `/etc/crictl.yaml`.
:::

Show images:

```sh
crictl images
```

Show pods:

```sh
crictl pods
```

Show containers:

```sh
crictl ps
```

## ctr

`ctr` is an unsupported debug and administrative client for interacting with the containerd daemon. Because it is unsupported, the commands, options, and operations are not guaranteed to be backward compatible or stable from release to release of the containerd project.

```sh
ctr --version
```

{.cli-output}

```text
ctr containerd.io 1.6.32
```

Import an image:

```sh
ctr -n k8s.io image import slurm-ubuntu-client.tar
```
