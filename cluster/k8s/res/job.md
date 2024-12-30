# Job

## Common

```sh
vi sleep_job.yaml
```

:::{literalinclude} /_files/macos/work/k8s/sleep_job.yaml
:language: yaml
:class: file-content
:::

```console
$ kubectl create -f sleep_job.yaml
job.batch/sleep-job created
```

Watch events:

:::{literalinclude} /_files/macos/console/kubectl/get_job_sleep_owide_w.txt
:language: console
:::

:::{note}
Delete job do not produce events for the job.
:::

If we list the pods when the job was running:

:::{literalinclude} /_files/macos/console/kubectl/get_po_job_sleep.txt
:language: console
:::

## Using kueue

Create a local queue first, see <project:localqueue.md>.

```sh
vi sleep_job_kueue.yaml
```

:::{literalinclude} /_files/macos/work/k8s/sleep_job_kueue.yaml
:language: yaml
:class: file-content
:::

:::{literalinclude} /_files/macos/console/kubectl/create_sleep_job_kueue.txt
:language: console
:::

Show events:

:::{literalinclude} /_files/macos/console/kubectl/get_job_sleep_kueue_owide_w.txt
:language: console
:::

Show workloads and pods:

:::{literalinclude} /_files/macos/console/kubectl/get_wl_po_owide_sleep_job_kueue.txt
:language: console
:::
