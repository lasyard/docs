# 从外网访问 k8s 集群发生认证错误

## 版本

```console
$ kubectl version
Client Version: v1.32.3
Kustomize Version: v5.5.0
Server Version: v1.32.0
```

## 问题

在外网的一台主机上获得内网 k8s 的配置 (`/etc/kubernetes/admin.conf`) 并修改 `cluster.server` 为外部 IP, 访问时发生错误：

```console
$ kubectl get nodes
E0422 17:19:49.305258   18755 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"https://10.220.70.56:6443/api?timeout=32s\": tls: failed to verify certificate: x509: certificate is valid for 10.96.0.1, 10.225.4.51, not 10.220.70.56"
E0422 17:19:49.314452   18755 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"https://10.220.70.56:6443/api?timeout=32s\": tls: failed to verify certificate: x509: certificate is valid for 10.96.0.1, 10.225.4.51, not 10.220.70.56"
E0422 17:19:49.324279   18755 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"https://10.220.70.56:6443/api?timeout=32s\": tls: failed to verify certificate: x509: certificate is valid for 10.96.0.1, 10.225.4.51, not 10.220.70.56"
E0422 17:19:49.332572   18755 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"https://10.220.70.56:6443/api?timeout=32s\": tls: failed to verify certificate: x509: certificate is valid for 10.96.0.1, 10.225.4.51, not 10.220.70.56"
E0422 17:19:49.343653   18755 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"https://10.220.70.56:6443/api?timeout=32s\": tls: failed to verify certificate: x509: certificate is valid for 10.96.0.1, 10.225.4.51, not 10.220.70.56"
Unable to connect to the server: tls: failed to verify certificate: x509: certificate is valid for 10.96.0.1, 10.225.4.51, not 10.220.70.56
```

## 原因

在 control-plane 节点上执行以下命令解析 apiserver 证书：

```console
$ openssl x509 -noout -text -in /etc/kubernetes/pki/apiserver.crt | grep IP
                DNS:k8ctl, DNS:kubernetes, DNS:kubernetes.default, DNS:kubernetes.default.svc, DNS:kubernetes.default.svc.cluster.local, IP Address:10.96.0.1, IP Address:10.225.4.51
```

可见认证的 IP 地址不包括我们使用的外部 IP, 这就是失败的原因。

## 解决方案

首先删除旧的证书：

```console
sudo rm /etc/kubernetes/pki/apiserver.*
```

重新生成证书：

```console
$ sudo kubeadm init phase certs apiserver --apiserver-cert-extra-sans 10.220.70.56
[certs] Generating "apiserver" certificate and key
[certs] apiserver serving cert is signed for DNS names [k8ctl kubernetes kubernetes.default kubernetes.default.svc kubernetes.default.svc.cluster.local] and IPs [10.96.0.1 10.225.4.51 10.220.70.56]
```

再次解析证书可见外部 IP 确实被加进去了：

```console
$ openssl x509 -noout -text -in /etc/kubernetes/pki/apiserver.crt | grep IP
                DNS:k8ctl, DNS:kubernetes, DNS:kubernetes.default, DNS:kubernetes.default.svc, DNS:kubernetes.default.svc.cluster.local, IP Address:10.96.0.1, IP Address:10.225.4.51, IP Address:10.220.70.56
```

现在可以从外网访问了：

```console
$ kubectl cluster-info
Kubernetes control plane is running at https://10.220.70.56:6443
CoreDNS is running at https://10.220.70.56:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```
