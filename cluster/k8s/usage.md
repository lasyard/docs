# Kubernetes Usage

## Token management

List all tokens:

:::{literalinclude} /_files/centos/console/kubeadm/token_list.txt
:language: console
:::

The tokens can be seen also by running:

:::{literalinclude} /_files/centos/console/kubectl/get_secrets_kube_system.txt
:language: console
:::

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

:::{literalinclude} /_files/centos/work/kubectl/slurm.properties
:language: properties
:class: file-content
:::

Create a ConfigMap from it:

:::{literalinclude} /_files/centos/console/kubectl/create_cm.txt
:language: console
:::

Show ConfigMaps:

:::{literalinclude} /_files/centos/console/kubectl/get_cm.txt
:language: console
:::

See the details of the new ConfigMap:

:::{literalinclude} /_files/centos/console/kubectl/describe_cm_1.txt
:language: console
:::

Alternatively, you can check the data by:

:::{literalinclude} /_files/centos/console/kubectl/get_cm_1.txt
:language: console
:::

Remove the ConfigMap:

:::{literalinclude} /_files/centos/console/kubectl/delete_cm.txt
:language: console
:::

If you want to break the content of `.properties` file into multiple ConfigMap keys, you can use:

:::{literalinclude} /_files/centos/console/kubectl/create_cm_5.txt
:language: console
:::

:::{literalinclude} /_files/centos/console/kubectl/get_cm_5.txt
:language: console
:::

:::{literalinclude} /_files/centos/console/kubectl/describe_cm_5.txt
:language: console
:::

Note the differences.

## Console of pods

```sh
kubectl exec -it xxxx-pod -- /bin/bash
```

## crictl

Check the version:

```console
$ crictl --version
crictl version v1.30.1
```

Show config:

```sh
crictl config --list
```

:::{literalinclude} /_files/centos/console/crictl/config_list.txt
:language: text
:class: cli-output
:::

:::{tip}
Configurations are stored in `/etc/crictl.yaml`.
:::

Set config:

```sh
sudo crictl config --set image-endpoint=unix:///run/containerd/containerd.sock
sudo crictl config --set runtime-endpoint=unix:///run/containerd/containerd.sock
```

Show images:

:::{literalinclude} /_files/centos/console/crictl/images.txt
:language: console
:::

Show pods:

:::{literalinclude} /_files/centos/console/crictl/pods.txt
:language: console
:::

Show containers:

:::{literalinclude} /_files/centos/console/crictl/ps.txt
:language: console
:::

## ctr

:::{note}
`ctr` is an unsupported debug and administrative client for interacting with the containerd daemon. Because it is unsupported, the commands, options, and operations are not guaranteed to be backward compatible or stable from release to release of the containerd project.
:::

Check the version:

```console
$ ctr --version
ctr containerd.io 1.6.32
```

Import an image:

```sh
ctr -n k8s.io image import slurm-worker.tar
```
