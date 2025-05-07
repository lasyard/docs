# ctr

`ctr` is installed along with `containerd`. Check the version:

```console
$ ctr --version
ctr containerd.io 1.7.27
```

Import an image from a tar ball (for use in Kubernetes):

```console
$ sudo ctr -n k8s.io image import busybox.tar
```
