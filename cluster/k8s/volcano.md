# volcano

<https://volcano.sh/en/>

## Install

Using `helm` to install:

:::{literalinclude} /_files/centos/console/helm/install_volcano.txt
:language: console
:::

## Queue

A default queue has been created after installation:

```console
$ kubectl get queues
NAME      AGE
default   31m
```

:::{tip}
Shortname of `queue` is `q`.
:::

Show details abount queue default:

:::{literalinclude} /_files/centos/console/kubectl/describe_q_default.txt
:language: console
:::

Create a queue configuration file, like this:

:::{literalinclude} /_files/centos/work/kubectl/test_q.yaml
:language: yaml
:class: file-content
:::

Then create the queue:

```console
$ kubectl apply -f test_q.yaml
queue.scheduling.volcano.sh/test created
```
