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

Delete an image:

```sh
sudo crictl rmi xxxx-image
```

Remove all unused images:

```sh
sudo crictl rmi -q
```

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
sudo ctr -n k8s.io image import busybox.tar
```

## List API vesions

:::{literalinclude} /_files/centos/console/kubectl/api-versions.txt
:language: console
:::

## List resources

:::{literalinclude} /_files/centos/console/kubectl/api-resources-no-group.txt
:language: console
:::

:::{literalinclude} /_files/centos/console/kubectl/api-resources-apps.txt
:language: console
:::
