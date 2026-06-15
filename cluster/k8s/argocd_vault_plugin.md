# argocd-vault-plugin

<https://argocd-vault-plugin.readthedocs.io/>

## The CLI

Donwload the binary of `argocd-vault-plugin`:

```console
$ curl -LO https://github.com/argoproj-labs/argocd-vault-plugin/releases/download/v1.18.1/argocd-vault-plugin_1.18.1_linux_amd64
```

`argocd-vault-plugin` can be used in CLI directly. Let's try:

```console
$ sudo install argocd-vault-plugin_1.18.1_linux_amd64 /usr/local/bin/argocd-vault-plugin
```

```console
$ argocd-vault-plugin version
argocd-vault-plugin v1.18.1 (fc452cdd8d4727b412ce3de61ee0416efd75050d) BuildDate: 2024-06-07T03:17:37Z
```

Put the vault configurations into a file, like this:

```yaml
AVP_TYPE: vault
VAULT_ADDR: https://localhost:8200
AVP_AUTH_TYPE: token
VAULT_TOKEN: root
```

Suppose the file is named `vault.yaml`, you can generate substituted json/yaml file as:

```console
$ argocd-vault-plugin generate path_to_yaml -c vault.yaml
```

> [!CAUTION]
>
> - We must provide the path to the secret in the placeholder, like `<path:secret/data/foo#bar>`.
> - It will serach and parse the `yaml` files and check if it is valid (at least the `kind` field is required), so do not put `vault.yaml` in the same directory of `path_to_yaml`. A single `yaml` is also supported.

Environments are also supported to provide vault configurations:

```console
$ export $(sed 's/: */=/' vault.yaml)
```

Now the `-c` arguments can be ommited:

```console
$ argocd-vault-plugin generate path_to_yaml
```

## Integrate it to ArgoCD

There's no official released image for `argocd-vault-plugin`, so we need to DIY. Write a docker file as:

:::{literalinclude} /_files/macos/workspace/argocd/Dockerfile.vault-plugin
:language: sh
:::

Put it with the `argocd-vault-plugin` binary in the same (dedicated) directory, then build and push the image to a repository:

```console
$ docker build . -t ghcr.io/lasyard/argocd-vault-plugin:v1.18.1
$ docker push ghcr.io/lasyard/argocd-vault-plugin:v1.18.1
```

The plugin need to be run as a sidecar of `argocd-repo-server`. You can do this by create a helm values file `argocd_vault_plugin_values.yaml` first:

:::{literalinclude} /_files/macos/workspace/argocd/argocd_vault_plugin_values.yaml
:::

You can see there should be a ConfigMap mounted in the sidecar. So create it before the installation:

:::{literalinclude} /_files/macos/workspace/argocd/argocd_vault_plugin_cm.yaml
:::

Note the startup command of the sidecar `/var/run/argocd/argocd-cmp-server` is not existing in our image. It is mounted in from the main container. This command will read the ConfigMap, create a socket file to communicate with the main container.

Now install ArgoCD using the new values file:

```console
$ helm install argocd argo-cd-9.5.17.tgz --namespace argocd --create-namespace --set global.domain=las1 -f argocd_vault_plugin_values.yaml
```

For we didn't provide any information about the vault in the `argocd_vault_plugin` command of the plugin, it can only get those by environments. So we must set the environments for the plugin sidecar:

```console
$ kubectl set env -n argocd deploy argocd-repo-server -c argocd-vault-plugin $(sed 's/: */=/' vault.yaml)
deployment.apps/argocd-repo-server env updated
```

Now it works! This method is just for test, and there are more practical ways to inform `argocd_vault_plugin` of vault settings.

> [!TIP]
> When working in kubernetes, the path of the vault secret can be provided by `metadata.annotations."avp.kubernetes.io/path"` of each resource.
