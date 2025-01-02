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

:::{literalinclude} /_files/macos/console/kubectl/get_job_owide_w.txt
:language: console
:::

:::{note}
Delete job do not produce events for the job.
:::

If we list the resources when the job was running:

:::{literalinclude} /_files/macos/console/kubectl/get_job_po_owide.txt
:language: console
:::

## Using kueue

Create a local queue first, see <project:topology_rf_cq_lq.md>.

```sh
vi sleep_job_kueue.yaml
```

:::{literalinclude} /_files/macos/work/k8s/sleep_job_kueue.yaml
:language: yaml
:class: file-content
:::

```console
$ kubectl create -f sleep_job_kueue.yaml
job.batch/sleep-job-g4s2l created
$ kubectl create -f sleep_job_kueue.yaml
job.batch/sleep-job-c8cmm created
```

Show events:

:::{literalinclude} /_files/macos/console/kubectl/get_job_owide_w_kueue.txt
:language: console
:::

Show resources:

:::{literalinclude} /_files/macos/console/kubectl/get_job_wl_po_kueue.txt
:language: console
:::
