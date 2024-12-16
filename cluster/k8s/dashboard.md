# Dashboard of Kubernetes

## Prerequisites

Install `helm` first, See "<project:../helm.md>".

## Install

Add `helm` repository:

```console
$ helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
"kubernetes-dashboard" has been added to your repositories
```

Then install it using `helm`:

:::{literalinclude} /_files/centos/console/helm/upgrade_dashboard.txt
:language: console
:::

## Service account

Create service account configuration:

```sh
vi admin_user.yaml
```

```{literalinclude} /_files/centos/work/kubectl/admin_user_sa.yaml
:language: yaml
:class: file-content
```

Create role binding configuration:

```sh
vi admin_user_role_binding.yaml
```

:::{literalinclude} /_files/centos/work/kubectl/admin_user_cluster_role_binding.yaml
:language: yaml
:class: file-content
:::

Apply these resources:

```console
$ kubectl apply -f admin_user_sa.yaml
serviceaccount/admin-user created
$ kubectl apply -f admin_user_cluster_role_binding.yaml
clusterrolebinding.rbac.authorization.k8s.io/admin-user created
```

## Expose the service

Check the dashboard services:

:::{literalinclude} /_files/centos/console/kubectl/get_svc_dashboard.txt
:language: console
:::

Expose the `kong-proxy` service:

```sh
kubectl -n kubernetes-dashboard port-forward --address=0.0.0.0 svc/kubernetes-dashboard-kong-proxy 8443:443
```

:::{note}
Port forwarding will be ceased if the command quit.
:::

Open the dashboard in your browser by the URL `https://las0:8443/`.

![Dashboard Login](/_images/cluster/k8s/dashboard_login.png/)

Generate a token for the user:

```sh
kubectl -n kubernetes-dashboard create token admin-user
```

Paste the output token into the login page.

:::{tip}
Restart `coredns` may solve some network problem:

```console
$ kubectl rollout restart deployment -n kube-system coredns
deployment.apps/coredns restarted
```

:::
