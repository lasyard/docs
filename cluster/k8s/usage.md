# Use Kubernetes

## Token management

Create a token with 24h lifespan:

```console
$ kubeadm token create --ttl 24h
ksngp4.g1ig5okdn4qgqsg8
```

List all tokens:

```console
$ kubeadm token list
TOKEN                     TTL         EXPIRES                USAGES                   DESCRIPTION                                                EXTRA GROUPS
ksngp4.g1ig5okdn4qgqsg8   23h         2025-04-24T07:55:17Z   authentication,signing   <none>                                                     system:bootstrappers:kubeadm:default-node-token
```

The tokens can also be seen by:

```console
$ kubectl get secrets -n kube-system
NAME                     TYPE                            DATA   AGE
bootstrap-token-ksngp4   bootstrap.kubernetes.io/token   6      3m56s
```

Delete a token:

```console
$ kubeadm token delete ksngp4.g1ig5okdn4qgqsg8
bootstrap token "ksngp4" deleted
```

or by deleting the secret:

```console
$ kubectl delete secret bootstrap-token-ksngp4 -n kube-system
secret "bootstrap-token-ksngp4" deleted
```

## Console of pods

Run shell in the pod:

```console
$ kubectl exec -it xxxx-pod -- /bin/bash
```

Show output of a pod:

```console
$ kubectl logs xxxx-pod
```

If it contains multiple containers, you can specify one of them:

```console
$ kubectl logs xxxx-pod -c xxxx-container
```

## Use private image repositories

Create a docker registry accessing secret:

```console
$ kubectl create secret docker-registry las3-harbor --docker-server=las3:443 --docker-username=admin --docker-password=AdminPassword123
secret/las3-harbor created
$ kubectl get secret las3-harbor -oyaml
apiVersion: v1
data:
  .dockerconfigjson: eyJhdXRocyI6eyJsYXMzOjQ0MyI6eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiJBZG1pblBhc3N3b3JkMTIzIiwiYXV0aCI6IllXUnRhVzQ2UVdSdGFXNVFZWE56ZDI5eVpERXlNdz09In19fQ==
kind: Secret
metadata:
  creationTimestamp: "2025-05-22T03:47:42Z"
  name: las3-harbor
  namespace: default
  resourceVersion: "3648752"
  uid: 608f187d-29ac-4fc4-87ca-1789a1d657f2
type: kubernetes.io/dockerconfigjson
```

:::{tip}
The `data.dockerconfigjson` field is just base64 encoded docker config file, see:

```console
$ kubectl get secret las3-harbor -o "jsonpath={.data.\.dockerconfigjson}" | base64 --decode | jq
{
  "auths": {
    "las3:443": {
      "username": "admin",
      "password": "AdminPassword123",
      "auth": "YWRtaW46QWRtaW5QYXNzd29yZDEyMw=="
    }
  }
}
```

The `auth` field in the above output is also base64 encoded. to dig into it, use the following command:

```console
$ kubectl get secret las3-harbor -o "jsonpath={.data.\.dockerconfigjson}" | base64 --decode | jq -r '.auths."las3:443".auth' | base64 --decode
admin:AdminPassword123
```

:::

Then the secret can be used to pull images from a private repository. Modify the pod spec:

:::{literalinclude} /_files/macos/workspace/k8s/sleep_po_private_repo.yaml
:diff: /_files/macos/workspace/k8s/sleep_po.yaml
:::

## List API vesions

```console
$ kubectl api-versions
admissionregistration.k8s.io/v1
apiextensions.k8s.io/v1
apiregistration.k8s.io/v1
apps/v1
authentication.k8s.io/v1
authorization.k8s.io/v1
autoscaling/v1
autoscaling/v2
batch/v1
certificates.k8s.io/v1
coordination.k8s.io/v1
crd.projectcalico.org/v1
discovery.k8s.io/v1
events.k8s.io/v1
flowcontrol.apiserver.k8s.io/v1
networking.k8s.io/v1
node.k8s.io/v1
operator.tigera.io/v1
policy.networking.k8s.io/v1alpha1
policy/v1
projectcalico.org/v3
rbac.authorization.k8s.io/v1
scheduling.k8s.io/v1
storage.k8s.io/v1
v1
```

## List API resources

List API resources with no group:

```console
$ kubectl api-resources --api-group=
NAME                     SHORTNAMES   APIVERSION   NAMESPACED   KIND
bindings                              v1           true         Binding
componentstatuses        cs           v1           false        ComponentStatus
configmaps               cm           v1           true         ConfigMap
endpoints                ep           v1           true         Endpoints
events                   ev           v1           true         Event
limitranges              limits       v1           true         LimitRange
namespaces               ns           v1           false        Namespace
nodes                    no           v1           false        Node
persistentvolumeclaims   pvc          v1           true         PersistentVolumeClaim
persistentvolumes        pv           v1           false        PersistentVolume
pods                     po           v1           true         Pod
podtemplates                          v1           true         PodTemplate
replicationcontrollers   rc           v1           true         ReplicationController
resourcequotas           quota        v1           true         ResourceQuota
secrets                               v1           true         Secret
serviceaccounts          sa           v1           true         ServiceAccount
services                 svc          v1           true         Service
```

List API resources in `apps` group:

```console
$ kubectl api-resources --api-group=apps
NAME                  SHORTNAMES   APIVERSION   NAMESPACED   KIND
controllerrevisions                apps/v1      true         ControllerRevision
daemonsets            ds           apps/v1      true         DaemonSet
deployments           deploy       apps/v1      true         Deployment
replicasets           rs           apps/v1      true         ReplicaSet
statefulsets          sts          apps/v1      true         StatefulSet
```

## Label nodes

Add a label to a node:

```console
$ kubectl label node las0 node-group=default
node/las0 labeled
```

Show the specified labels:

```console
$ kubectl get node las0 -L node-group
NAME    STATUS   ROLES           AGE    VERSION   NODE-GROUP
las0    Ready    control-plane   5d1h   v1.32.3   default
```

Modify the label:

```console
$ kubectl label --overwrite node las0 node-group=test
node/las0 labeled
$ kubectl get node las0 -L node-group
NAME    STATUS   ROLES           AGE    VERSION   NODE-GROUP
las0    Ready    control-plane   5d1h   v1.32.3   test
```

Remove label:

```console
$ kubectl label node las0 node-group-
node/las0 unlabeled
$ kubectl get node las0 -L node-group
NAME    STATUS   ROLES           AGE    VERSION   NODE-GROUP
las0    Ready    control-plane   5d1h   v1.32.3
```

Show all labels of nodes:

```console
$ kubectl get node --show-labels
```

or:

```console
$ kubectl label --list node las0
```

## Selector

Get pods on a specified node:

```console
$ kubectl get po -A --field-selector spec.nodeName=las3
```

## Customize output

Get specified info of all nodes:

```console
$ kubectl get no -o custom-columns=NAME:.metadata.name,CPU:.status.capacity.cpu,MEMORY:.status.capacity.memory,GPU:.status.capacity.nvidia\\.com/gpu
```

:::{note}
There must be double `\` to escape twice.
:::
