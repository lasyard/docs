# Volcano Job

Create a volcano queue first, see <project:queue.md>.

```sh
vi sleep_vj.yaml
```

:::{literalinclude} /_files/macos/work/k8s/sleep_vj.yaml
:language: yaml
:class: file-content
:::

```console
$ kubectl create -f sleep_vj.yaml
job.batch.volcano.sh/sleep-vj created
```

:::{note}
The job will be in `PENDING` state if the underlying pods were not running succcessfuly, which may not caused by lack of resources.
:::

Watch events:

:::{literalinclude} /_files/macos/console/kubectl/get_vj_owide_w.txt
:language: console
:::

If we list the resources when the job was running:

:::{literalinclude} /_files/macos/console/kubectl/get_vj_pg_po.txt
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
