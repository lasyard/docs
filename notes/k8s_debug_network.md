# K8s 网络诊断

准备一个包含基本网络工具的 Pod:

:::{literalinclude} /_files/macos/workspace/k8s/dnsutils.yaml
:::

将其应用到网络。

解析域名：

```console
$ kubectl exec -it dnsutils -- nslookup kubernetes
;; Got recursion not available from 10.96.0.10
Server:     10.96.0.10
Address:    10.96.0.10#53

Name:   kubernetes.default.svc.cluster.local
Address: 10.96.0.1
;; Got recursion not available from 10.96.0.10
```
