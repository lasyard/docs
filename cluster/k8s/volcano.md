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

## Job

Create a job configuration file, like this:

:::{literalinclude} /_files/centos/work/kubectl/sleep_vj.yaml
:language: yaml
:class: file-content
:::

Then create the job:

```console
$ kubectl create -f sleep_vj.yaml
job.batch.volcano.sh/sleep-job created
```

:::{note}
The job will be in `PENDING` state if the underlying pods were not running succcessfuly, which may not caused by lack of resources.
:::

Show the job and the pods:

:::{literalinclude} /_files/centos/console/kubectl/get_vj.txt
:language: console
:::

Delete the job:

```console
$ k delete vj sleep-job
job.batch.volcano.sh "sleep-job" deleted
```

:::{note}
Delete the job will also delete all task pods.
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
