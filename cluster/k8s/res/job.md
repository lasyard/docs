# Job

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
