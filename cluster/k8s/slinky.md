# Slinky

<https://slinky.schedmd.com/>
<https://github.com/SlinkyProject>

## Install

Install `cert-manager`:

```console
$ helm pull jetstack/cert-manager
$ helm install cert-manager cert-manager-v1.19.2.tgz --namespace cert-manager --create-namespace --set crds.enabled=true
NAME: cert-manager
LAST DEPLOYED: Mon Mar 23 11:27:19 2026
NAMESPACE: cert-manager
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
⚠️  WARNING: New default private key rotation policy for Certificate resources.
The default private key rotation policy for Certificate resources was
changed to `Always` in cert-manager >= v1.18.0.
Learn more in the [1.18 release notes](https://cert-manager.io/docs/releases/release-notes/release-notes-1.18).

cert-manager v1.19.2 has been deployed successfully!

In order to begin issuing certificates, you will need to set up a ClusterIssuer
or Issuer resource (for example, by creating a 'letsencrypt-staging' issuer).

More information on the different types of issuers and how to configure them
can be found in our documentation:

https://cert-manager.io/docs/configuration/

For information on how to configure cert-manager to automatically provision
Certificates for Ingress resources, take a look at the `ingress-shim`
documentation:

https://cert-manager.io/docs/usage/ingress/
```

Install the slurm-operator and its CRDs:

```console
$ helm pull oci://ghcr.io/slinkyproject/charts/slurm-operator-crds
Pulled: ghcr.io/slinkyproject/charts/slurm-operator-crds:1.0.2
Digest: sha256:c05bbcb08906f11c05e8088a051322f517229b9696d592e2db95c6bafc4a40d3
$ helm pull oci://ghcr.io/slinkyproject/charts/slurm-operator
Pulled: ghcr.io/slinkyproject/charts/slurm-operator:1.0.2
Digest: sha256:83773374238475c561d8dc81fc9185f442933232d3c50ebf04d94d71d3e49c0d
```

```console
$ helm install slurm-operator-crds slurm-operator-crds-1.0.2.tgz
NAME: slurm-operator-crds
LAST DEPLOYED: Mon Mar 23 11:41:41 2026
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
$ helm install slurm-operator slurm-operator-1.0.2.tgz --namespace=slinky --create-namespace
NAME: slurm-operator
LAST DEPLOYED: Mon Mar 23 11:42:18 2026
NAMESPACE: slinky
STATUS: deployed
REVISION: 1
NOTES:
CHART NAME: slurm-operator
CHART VERSION: 1.0.2
APP VERSION: 25.11
```

Show installed CRDs:

```console
$ kubectl get crd | grep slinky
accountings.slinky.slurm.net                          2026-03-23T03:41:44Z
controllers.slinky.slurm.net                          2026-03-23T03:41:44Z
loginsets.slinky.slurm.net                            2026-03-23T03:41:44Z
nodesets.slinky.slurm.net                             2026-03-23T03:41:44Z
restapis.slinky.slurm.net                             2026-03-23T03:41:44Z
tokens.slinky.slurm.net                               2026-03-23T03:41:44Z
```

Show installed workloads:

```console
$ kubectl get all -n slinky
NAME                                         READY   STATUS    RESTARTS   AGE
pod/slurm-operator-65c9c6559d-rnbfj          1/1     Running   0          116s
pod/slurm-operator-webhook-84cd7974d-46kwn   1/1     Running   0          116s

NAME                             TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)             AGE
service/slurm-operator           ClusterIP   None             <none>        8080/TCP,8081/TCP   116s
service/slurm-operator-webhook   ClusterIP   10.108.247.229   <none>        443/TCP,8081/TCP    116s

NAME                                     READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/slurm-operator           1/1     1            1           116s
deployment.apps/slurm-operator-webhook   1/1     1            1           116s

NAME                                               DESIRED   CURRENT   READY   AGE
replicaset.apps/slurm-operator-65c9c6559d          1         1         1       116s
replicaset.apps/slurm-operator-webhook-84cd7974d   1         1         1       116s
```

Slurm controller persistentw states to a volume, so there should be an default StorageClass to create PVC.

Install a cluster:

```console
$ helm pull oci://ghcr.io/slinkyproject/charts/slurm
Pulled: ghcr.io/slinkyproject/charts/slurm:1.0.2
Digest: sha256:a5c39577d1e7775d921281393ac6ee5a1a6143c0bea4a7d5609f8ad00e2f5a00
```

```console
$ helm install slurm slurm-1.0.2.tgz --namespace=slurm --create-namespace --set loginsets.slinky.enabled=true
NAME: slurm
LAST DEPLOYED: Mon Mar 23 14:13:31 2026
NAMESPACE: slurm
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
********************************************************************************

                                 SSSSSSS
                                SSSSSSSSS
                                SSSSSSSSS
                                SSSSSSSSS
                        SSSS     SSSSSSS     SSSS
                       SSSSSS               SSSSSS
                       SSSSSS    SSSSSSS    SSSSSS
                        SSSS    SSSSSSSSS    SSSS
                SSS             SSSSSSSSS             SSS
               SSSSS    SSSS    SSSSSSSSS    SSSS    SSSSS
                SSS    SSSSSS   SSSSSSSSS   SSSSSS    SSS
                       SSSSSS    SSSSSSS    SSSSSS
                SSS    SSSSSS               SSSSSS    SSS
               SSSSS    SSSS     SSSSSSS     SSSS    SSSSS
          S     SSS             SSSSSSSSS             SSS     S
         SSS            SSSS    SSSSSSSSS    SSSS            SSS
          S     SSS    SSSSSS   SSSSSSSSS   SSSSSS    SSS     S
               SSSSS   SSSSSS   SSSSSSSSS   SSSSSS   SSSSS
          S    SSSSS    SSSS     SSSSSSS     SSSS    SSSSS    S
    S    SSS    SSS                                   SSS    SSS    S
    S     S                                                   S     S
                SSS
                SSS
                SSS
                SSS
 SSSSSSSSSSSS   SSS   SSSS       SSSS    SSSSSSSSS   SSSSSSSSSSSSSSSSSSSS
SSSSSSSSSSSSS   SSS   SSSS       SSSS   SSSSSSSSSS  SSSSSSSSSSSSSSSSSSSSSS
SSSS            SSS   SSSS       SSSS   SSSS        SSSS     SSSS     SSSS
SSSS            SSS   SSSS       SSSS   SSSS        SSSS     SSSS     SSSS
SSSSSSSSSSSS    SSS   SSSS       SSSS   SSSS        SSSS     SSSS     SSSS
 SSSSSSSSSSSS   SSS   SSSS       SSSS   SSSS        SSSS     SSSS     SSSS
         SSSS   SSS   SSSS       SSSS   SSSS        SSSS     SSSS     SSSS
         SSSS   SSS   SSSS       SSSS   SSSS        SSSS     SSSS     SSSS
SSSSSSSSSSSSS   SSS   SSSSSSSSSSSSSSS   SSSS        SSSS     SSSS     SSSS
SSSSSSSSSSSS    SSS    SSSSSSSSSSSSS    SSSS        SSSS     SSSS     SSSS

********************************************************************************

CHART NAME: slurm
CHART VERSION: 1.0.2
APP VERSION: 25.11

slurm has been installed. Check its status by running:
  $ kubectl --namespace=slurm get pods -l helm.sh/chart=slurm-1.0.2 --watch

ssh via the Slurm login (slurm-login-slinky) service:
  $ SLURM_LOGIN_IP="$(kubectl get services -n slurm slurm-login-slinky -o jsonpath='{.status.loadBalancer.ingress[0].ip}')"
  $ ssh -p 22 $SLURM_LOGIN_IP

Learn more about Slurm:
  - Overview: https://slurm.schedmd.com/overview.html
  - Quickstart: https://slurm.schedmd.com/quickstart.html
  - Documentation: https://slurm.schedmd.com/documentation.html
  - Support: https://www.schedmd.com/slurm-support/our-services/
  - File Tickets: https://support.schedmd.com/

Learn more about Slinky:
  - Overview: https://www.schedmd.com/slinky/why-slinky/
  - Documentation: https://slinky.schedmd.com
```

Show running pods:

```console
$ kubectl get po -n slurm
NAME                                  READY   STATUS    RESTARTS   AGE
slurm-controller-0                    3/3     Running   0          35s
slurm-login-slinky-5c76c76644-cj9s9   1/1     Running   0          35s
slurm-restapi-6b4ccb479f-458g7        1/1     Running   0          35s
slurm-worker-slinky-0                 2/2     Running   0          35s
```

Show the created PVC:

```console
$ kubectl get pvc -n slurm
NAME                           STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
statesave-slurm-controller-0   Bound    pvc-4b9403a5-36f1-4873-baa9-2fb54598fb8b   4Gi        RWO            standard       <unset>                 6m26s
```

Show created services:

```console
$ kubectl get svc -n slurm
NAME                  TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
slurm-controller      ClusterIP      10.99.60.4       <none>        6817/TCP       114m
slurm-login-slinky    LoadBalancer   10.105.170.112   <pending>     22:30951/TCP   114m
slurm-restapi         ClusterIP      10.98.19.54      <none>        6820/TCP       114m
slurm-workers-slurm   ClusterIP      None             <none>        6818/TCP       114m
```

Since there is no external IP addresses available, we cannot access the login node from outside the cluster, but we can get a console directly by:

```console
$ kubectl exec -n slurm -it slurm-login-slinky-5c76c76644-cj9s9 -- bash
```

In the console, try:

```console
$ sinfo
PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST
slinky       up   infinite      1   idle slinky-0
all*         up   infinite      1   idle slinky-0
```
