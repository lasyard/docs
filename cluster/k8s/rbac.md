# RBAC (Role-Based Access Control)

## Create an user

The user name is `xxxx`.

Create private key and sign certificate for the user (on the node of control-plane):

```console
$ openssl genrsa -out xxxx.key 2048
$ openssl req -new -key xxxx.key -out xxxx.csr -subj "/O=las/CN=xxxx"
$ sudo openssl x509 -req -in xxxx.csr -CA /etc/kubernetes/pki/ca.crt -CAkey /etc/kubernetes/pki/ca.key -CAcreateserial -out xxxx.crt -days 365
Certificate request self-signature ok
subject=O = las, CN = xxxx
```

Create kubeconfig for the user:

```console
$ kubectl config set-cluster las --kubeconfig=xxxx.config --embed-certs --certificate-authority=/etc/kubernetes/pki/ca.crt --server=https://10.225.4.51:6443
Cluster "las" set.
$ kubectl config set-credentials xxxx --kubeconfig=xxxx.config --embed-certs --client-certificate=xxxx.crt --client-key=xxxx.key
User "xxxx" set.
$ kubectl config set-context xxxx@las --kubeconfig=xxxx.config --cluster=las --user=xxxx
Context "xxxx@las" created.
$ kubectl config use-context xxxx@las --kubeconfig=xxxx.config
Switched to context "xxxx@las".
```

Try to access the cluster with the new config:

```console
$ kubectl get po --kubeconfig=xxxx.config
Error from server (Forbidden): pods is forbidden: User "xxxx" cannot list resource "pods" in API group "" in the namespace "default"
```

Failed! Because the new user has no privileges.

## Grant user privileges

Create a role:

```console
$ kubectl create role pod-reader --verb=get,list,watch --resource=pods
role.rbac.authorization.k8s.io/pod-reader created
$ kubectl get role pod-reader
NAME         CREATED AT
pod-reader   2025-07-01T02:52:44Z
```

Bind the user to the role:

```console
$ kubectl create rolebinding xxxx-pod-reader --role=pod-reader --user=xxxx
rolebinding.rbac.authorization.k8s.io/xxxx-pod-reader created
$ kubectl get rolebinding -owide
NAME              ROLE              AGE     USERS   GROUPS   SERVICEACCOUNTS
xxxx-pod-reader   Role/pod-reader   18s     xxxx
```

Now the user can do what he can using the kube config:

```console
$ kubectl get po --kubeconfig=xxxx.config
No resources found in default namespace.
```
