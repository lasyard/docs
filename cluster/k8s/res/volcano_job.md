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

Watch events:

:::{literalinclude} /_files/macos/console/kubectl/get_vj_sleep_owide_w.txt
:language: console
:::

If we list the podgroups and pods when the job was running:

:::{literalinclude} /_files/macos/console/kubectl/get_pg_po_owide_vj_sleep.txt
:language: console
:::
