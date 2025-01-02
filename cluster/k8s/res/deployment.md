# Deployment

```sh
vi sleep_deploy.yaml
```

:::{literalinclude} /_files/macos/work/k8s/sleep_deploy.yaml
:language: yaml
:class: file-content
:::

:::{note}

- `restartPolicy` must be `Always`, the default value
- `selector` must be set and match the labels of template

:::

```console
$ kubectl create -f sleep_deploy.yaml
deployment.apps/sleep-deploy created
```

Watch events:

:::{literalinclude} /_files/macos/console/kubectl/get_deploy_owide_w.txt
:language: console
:::

If we list the resources when the deployment was 3/3 ready:

:::{literalinclude} /_files/macos/console/kubectl/get_deploy_rs_po_owide.txt
:language: console
:::
