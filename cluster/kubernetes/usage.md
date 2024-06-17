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
