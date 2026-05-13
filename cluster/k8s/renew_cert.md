# Renew certificates

Check if they expire:

```console
$ sudo kubeadm certs check-expiration
[check-expiration] Reading configuration from the "kubeadm-config" ConfigMap in namespace "kube-system"...
[check-expiration] Use 'kubeadm init phase upload-config kubeadm --config your-config-file' to re-upload it.
[check-expiration] Error reading configuration from the Cluster. Falling back to default configuration

CERTIFICATE                EXPIRES                  RESIDUAL TIME   CERTIFICATE AUTHORITY   EXTERNALLY MANAGED
admin.conf                 May 12, 2026 03:47 UTC   <invalid>       ca                      no      
apiserver                  May 13, 2026 08:05 UTC   <invalid>       ca                      no      
apiserver-etcd-client      May 12, 2026 03:47 UTC   <invalid>       etcd-ca                 no      
apiserver-kubelet-client   May 12, 2026 03:47 UTC   <invalid>       ca                      no      
controller-manager.conf    May 12, 2026 03:47 UTC   <invalid>       ca                      no      
etcd-healthcheck-client    May 12, 2026 03:47 UTC   <invalid>       etcd-ca                 no      
etcd-peer                  May 12, 2026 03:47 UTC   <invalid>       etcd-ca                 no      
etcd-server                May 12, 2026 03:47 UTC   <invalid>       etcd-ca                 no      
front-proxy-client         May 12, 2026 03:47 UTC   <invalid>       front-proxy-ca          no      
scheduler.conf             May 12, 2026 03:47 UTC   <invalid>       ca                      no      
super-admin.conf           May 12, 2026 03:47 UTC   <invalid>       ca                      no      

CERTIFICATE AUTHORITY   EXPIRES                  RESIDUAL TIME   EXTERNALLY MANAGED
ca                      May 10, 2035 03:47 UTC   8y              no      
etcd-ca                 May 10, 2035 03:47 UTC   8y              no      
front-proxy-ca          May 10, 2035 03:47 UTC   8y              no
```

All have expired, so renew them all:

```console
$ sudo kubeadm certs renew all
[renew] Reading configuration from the "kubeadm-config" ConfigMap in namespace "kube-system"...
[renew] Use 'kubeadm init phase upload-config kubeadm --config your-config-file' to re-upload it.
[renew] Error reading configuration from the Cluster. Falling back to default configuration

certificate embedded in the kubeconfig file for the admin to use and for kubeadm itself renewed
certificate for serving the Kubernetes API renewed
certificate the apiserver uses to access etcd renewed
certificate for the API server to connect to kubelet renewed
certificate embedded in the kubeconfig file for the controller manager to use renewed
certificate for liveness probes to healthcheck etcd renewed
certificate for etcd nodes to communicate with each other renewed
certificate for serving etcd renewed
certificate for the front proxy client renewed
certificate embedded in the kubeconfig file for the scheduler manager to use renewed
certificate embedded in the kubeconfig file for the super-admin renewed

Done renewing certificates. You must restart the kube-apiserver, kube-controller-manager, kube-scheduler and etcd, so that they can use the new certificates.
```

For we can't access the cluster, so we can't restart the services. But we can restart `kubelet`:

```cosnole
$ sudo systemctl restart kubelet
```

You need to do this on all control-plane nodes.

Then just copy the `/etc/kubernetes/admin.conf` out or merge it with the current config:

```console
$ sudo KUBECONFIG=/etc/kubernetes/admin.conf:${HOME}/.kube/config kubectl config view --flatten > new_config
```

Note the values in the former file will take precedence over the later.
