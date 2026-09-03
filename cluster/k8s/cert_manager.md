# cert-manager

<https://cert-manager.io/>

## Install

Add repository:

```console
$ helm repo add jetstack https://charts.jetstack.io
"jetstack" has been added to your repositories
$ helm repo update
```

Download:

```console
$ helm pull jetstack/cert-manager
```

Install:

```console
$ helm install cert-manager cert-manager-v1.21.1.tgz --namespace cert-manager --create-namespace --set crds.enabled=true
NAME: cert-manager
LAST DEPLOYED: Mon Aug 31 19:00:37 2026
NAMESPACE: cert-manager
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
cert-manager v1.21.1 has been deployed successfully!

In order to begin issuing certificates, you will need to set up a ClusterIssuer
or Issuer resource (for example, by creating a 'letsencrypt-staging' issuer).

More information on the different types of issuers and how to configure them
can be found in our documentation:

https://cert-manager.io/docs/configuration/

For information on how to configure cert-manager to automatically provision
Certificates for Ingress resources, take a look at the `ingress-shim`
documentation:

https://cert-manager.io/docs/usage/ingress/

For information on how to configure cert-manager to automatically provision
Certificates for Gateway API resources, take a look at the `gateway resource`
documentation:

https://cert-manager.io/docs/usage/gateway/
```
