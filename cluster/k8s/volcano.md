# volcano

<https://volcano.sh/en/>

## Install

Using `helm` to install:

:::{literalinclude} /_files/centos/console/helm/install_volcano.txt
:language: console
:::

A default queue has been created after installation:

```console
$ kubectl get queues
NAME      AGE
default   31m
```

:::{tip}
Shortname of `queue` is `q`.
:::

Show details about queue default:

:::{literalinclude} /_files/centos/console/kubectl/describe_q_default.txt
:language: console
:::

:::{seealso}

See <project:res/queue.md> and <project:res/volcano_job.md>.
:::

## vcctl

```sh
git clone -b v1.10.0 git@github.com:volcano-sh/volcano.git
make vcctl
cp _output/bin/vcctl ${HOME}/bin
```

Show queue list:

:::{literalinclude} /_files/centos/console/vcctl/queue_list.txt
:language: console
:::

Show job list:

:::{literalinclude} /_files/centos/console/vcctl/job_list.txt
:language: console
:::
