# Flux

<https://fluxcd.io/>

## Install CLI

:::::{tab-set}
::::{tab-item} macOS

```console
$ brew install fluxcd/tap/flux
```

::::
:::::

## Usage

Check to see if your cluster is compatible:

```console
$ flux check --pre
► checking prerequisites
✔ Kubernetes 1.35.8 >=1.33.0-0
✔ prerequisites checks passed
```

Bootstrap from a git repo:

```console
$ flux bootstrap git --url=ssh://git@las0/home/git/repos/flux.git
► cloning branch "main" from Git repository "ssh://git@las0/home/git/repos/flux.git"
✔ cloned repository
► generating component manifests
✔ generated component manifests
✔ component manifests are up to date
✔ reconciled components
► determining if source secret "flux-system/flux-system" exists
✔ source secret up to date
► generating sync manifests
✔ generated sync manifests
✔ sync manifests are up to date
► applying sync manifests
✔ reconciled sync configuration
◎ waiting for GitRepository "flux-system/flux-system" to be reconciled
✔ GitRepository reconciled successfully
◎ waiting for Kustomization "flux-system/flux-system" to be reconciled
✔ Kustomization reconciled successfully
► confirming components are healthy
✔ helm-controller: deployment ready
✔ kustomize-controller: deployment ready
✔ notification-controller: deployment ready
✔ source-controller: deployment ready
✔ all components are healthy
```

Now you can do full check with `flux check`.

Created workloads in the cluster:

```console
$ kubectl get svc -n flux-system
NAME                      TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
notification-controller   ClusterIP   10.99.175.226    <none>        80/TCP    178m
source-controller         ClusterIP   10.101.61.27     <none>        80/TCP    178m
webhook-receiver          ClusterIP   10.111.157.113   <none>        80/TCP    178m
$ kubectl get deploy -n flux-system
NAME                      READY   UP-TO-DATE   AVAILABLE   AGE
helm-controller           1/1     1            1           178m
kustomize-controller      1/1     1            1           178m
notification-controller   1/1     1            1           178m
source-controller         1/1     1            1           178m
```

Created GitRepository and Kustomization:

```console
$ kubectl get gitrepo -n flux-system
NAME          URL                                      AGE    READY   STATUS
flux-system   ssh://git@las0/home/git/repos/flux.git   175m   True    stored artifact for revision 'main@sha1:12fd21d1d1311bd889625b6cfbcf9d79a23bff69'
$ kubectl get ks -n flux-system
NAME          AGE    READY   STATUS
flux-system   175m   True    Applied revision: main@sha1:12fd21d1d1311bd889625b6cfbcf9d79a23bff69
```

The spec of the Kustomization:

```console
$ kubectl get ks flux-system -n flux-system -ojsonpath='{.spec}' | jq
{
  "force": false,
  "interval": "10m0s",
  "path": "./",
  "prune": true,
  "sourceRef": {
    "kind": "GitRepository",
    "name": "flux-system"
  }
}
```

We didn't specify the `--path` parameter, so the path is the root of repository. That is, any change to the repo will be reconciled.

Source of the created resources are put into `flux-system` dir in the git repo.

The credential to access git repo is stored in a Secret:

```console
$ kubectl get secret flux-system -o yaml
apiVersion: v1
data:
  identity: ...
  identity.pub: ...
  known_hosts: ...
kind: Secret
metadata: ...
type: Opaque
```

If you can't wait for recociling, do it mannually:

```console
$ flux reconcile kustomization flux-system --with-source
► annotating GitRepository flux-system in flux-system namespace
✔ GitRepository annotated
◎ waiting for GitRepository reconciliation
✔ fetched revision main@sha1:d4fe04470bb6422cd43ca34e364a68fb15d57df4
► annotating Kustomization flux-system in flux-system namespace
✔ Kustomization annotated
◎ waiting for Kustomization reconciliation
✔ applied revision main@sha1:d4fe04470bb6422cd43ca34e364a68fb15d57df4
```
