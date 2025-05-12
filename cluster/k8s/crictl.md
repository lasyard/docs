# crictl

`crictl` is installed along with Kubernetes. Check the version:

```console
$ crictl --version
crictl version v1.32.0
```

Configurations are stored in file `/etc/crictl.yaml`. Set config:

```console
$ sudo crictl config --set image-endpoint=unix:///run/containerd/containerd.sock
$ sudo crictl config --set runtime-endpoint=unix:///run/containerd/containerd.sock
```

Now show the content of file `/etc/crictl.yaml`:

:::{literalinclude} /_files/ubuntu/etc/crictl.yaml
:language: yaml
:::

Show config:

```console
$ crictl config --list
KEY                    VALUE
runtime-endpoint       unix:///run/containerd/containerd.sock
image-endpoint         unix:///run/containerd/containerd.sock
timeout                0
debug                  false
pull-image-on-create   false
disable-pull-on-run    false
```

Show images:

```console
$ sudo crictl images
IMAGE                                                             TAG                 IMAGE ID            SIZE
docker.io/calico/apiserver                                        v3.29.3             b1960e792987d       44.5MB
docker.io/calico/cni                                              v3.29.3             a140d04be1bc9       99.3MB
docker.io/calico/csi                                              v3.29.3             4c37db5645f40       9.41MB
docker.io/calico/kube-controllers                                 v3.29.3             4e982138231b3       36.3MB
docker.io/calico/node-driver-registrar                            v3.29.3             e909e2ccf5440       15.5MB
docker.io/calico/node                                             v3.29.3             042163432abce       144MB
docker.io/calico/pod2daemon-flexvol                               v3.29.3             0ceddb3add2e9       6.86MB
docker.io/calico/typha                                            v3.29.3             bde24a3cb8851       31.9MB
quay.io/tigera/operator                                           v1.36.7             e9b19fa62f476       22MB
registry.aliyuncs.com/google_containers/coredns                   v1.11.3             c69fa2e9cbf5f       18.6MB
registry.aliyuncs.com/google_containers/etcd                      3.5.16-0            a9e7e6b294baf       57.7MB
registry.aliyuncs.com/google_containers/kube-apiserver            v1.32.0             c2e17b8d0f4a3       28.7MB
registry.aliyuncs.com/google_containers/kube-controller-manager   v1.32.0             8cab3d2a8bd0f       26.3MB
registry.aliyuncs.com/google_containers/kube-proxy                v1.32.0             040f9f8aac8cd       30.9MB
registry.aliyuncs.com/google_containers/kube-scheduler            v1.32.0             a389e107f4ff1       20.7MB
registry.aliyuncs.com/google_containers/pause                     3.10                873ed75102791       320kB
```

Show pods:

```console
$ sudo crictl pods
POD ID              CREATED             STATE               NAME                                                          NAMESPACE           ATTEMPT             RUNTIME
9cdfad75f5635       11 days ago         Ready               coredns-6766b7b6bb-54qbk                                      kube-system         78                  (default)
0609975dd7331       11 days ago         Ready               calico-apiserver-6d594967cf-6phwt                             calico-apiserver    3                   (default)
4bf5fdec55934       11 days ago         Ready               csi-node-driver-s2sf4                                         calico-system       3                   (default)
588c10517e980       11 days ago         Ready               coredns-6766b7b6bb-4x4rl                                      kube-system         78                  (default)
03ab9a1942bb0       11 days ago         Ready               calico-apiserver-6d594967cf-qdsxb                             calico-apiserver    3                   (default)
7f6a07b968105       11 days ago         Ready               calico-kube-controllers-5fd8578969-8wqx2                      calico-system       3                   (default)
29117c845f41d       11 days ago         Ready               calico-node-6gx8c                                             calico-system       0                   (default)
625e34f0589da       11 days ago         Ready               calico-typha-85cf5855fb-x9g5x                                 calico-system       0                   (default)
fda5bab7cb8ac       11 days ago         Ready               tigera-operator-789496d6f5-vqrbn                              tigera-operator     0                   (default)
bbcdf88c39fe9       11 days ago         Ready               kube-proxy-9frrn                                              kube-system         0                   (default)
93d7bea5269b3       11 days ago         Ready               kube-apiserver-las0                                           kube-system         0                   (default)
40864c5524e92       11 days ago         Ready               etcd-las0                                                     kube-system         0                   (default)
2cde635b9091f       11 days ago         Ready               kube-scheduler-las0                                           kube-system         0                   (default)
9479349afcd4a       11 days ago         Ready               kube-controller-manager-las0                                  kube-system         0                   (default)
```

Show containers:

```console
$ sudo crictl ps
CONTAINER           IMAGE               CREATED             STATE               NAME                        ATTEMPT             POD ID              POD                                                           NAMESPACE
e4092542c5ace       b1960e792987d       11 days ago         Running             calico-apiserver            0                   03ab9a1942bb0       calico-apiserver-6d594967cf-qdsxb                             calico-apiserver
305c97aa3c2ac       c69fa2e9cbf5f       11 days ago         Running             coredns                     0                   588c10517e980       coredns-6766b7b6bb-4x4rl                                      kube-system
30dc929465723       c69fa2e9cbf5f       11 days ago         Running             coredns                     0                   9cdfad75f5635       coredns-6766b7b6bb-54qbk                                      kube-system
d6ab1e9bd3784       b1960e792987d       11 days ago         Running             calico-apiserver            0                   0609975dd7331       calico-apiserver-6d594967cf-6phwt                             calico-apiserver
a60beff3039e1       4e982138231b3       11 days ago         Running             calico-kube-controllers     0                   7f6a07b968105       calico-kube-controllers-5fd8578969-8wqx2                      calico-system
8ac4bc3278310       e909e2ccf5440       11 days ago         Running             csi-node-driver-registrar   0                   4bf5fdec55934       csi-node-driver-s2sf4                                         calico-system
50850e15d30d4       4c37db5645f40       11 days ago         Running             calico-csi                  0                   4bf5fdec55934       csi-node-driver-s2sf4                                         calico-system
f87095e05e74c       042163432abce       11 days ago         Running             calico-node                 0                   29117c845f41d       calico-node-6gx8c                                             calico-system
22bd2eb8c7af7       bde24a3cb8851       11 days ago         Running             calico-typha                0                   625e34f0589da       calico-typha-85cf5855fb-x9g5x                                 calico-system
0aa0e1cc9e8a8       e9b19fa62f476       11 days ago         Running             tigera-operator             0                   fda5bab7cb8ac       tigera-operator-789496d6f5-vqrbn                              tigera-operator
17a191df384a1       040f9f8aac8cd       11 days ago         Running             kube-proxy                  0                   bbcdf88c39fe9       kube-proxy-9frrn                                              kube-system
847b032a4e570       a9e7e6b294baf       11 days ago         Running             etcd                        16                  40864c5524e92       etcd-las0                                                    kube-system
ec1a9929161d6       c2e17b8d0f4a3       11 days ago         Running             kube-apiserver              2                   93d7bea5269b3       kube-apiserver-las0                                          kube-system
e23c08cab9148       8cab3d2a8bd0f       11 days ago         Running             kube-controller-manager     2                   9479349afcd4a       kube-controller-manager-las0                                 kube-system
1c013cbbdd1e9       a389e107f4ff1       11 days ago         Running             kube-scheduler              16                  2cde635b9091f       kube-scheduler-las0                                          kube-system
```

Delete an image:

```console
$ sudo crictl rmi xxxx-image
```

Remove all unused images:

```console
$ sudo crictl rmi -q
```
