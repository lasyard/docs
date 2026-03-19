# Prometheus Operator

## Install

```console
$ helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
"prometheus-community" has been added to your repositories
$ helm pull prometheus-community/kube-prometheus-stack
```

prometheus-node-exporter 默认使用 `hostNetwork` 方式绑定端口 9100, 如果宿主机的 9100 端口已被占用，就需要修改端口。为了方便，先创建一个文件 `values_port.yaml`:

:::{literalinclude} /_files/macos/workspace/k8s/prometheus/values_port.yaml
:::

然后安装：

```console
$ helm install monitoring kube-prometheus-stack-82.10.5.tgz -n monitoring --create-namespace -f values_port.yaml
W0317 18:00:42.549581   68287 warnings.go:70] unknown field "spec.hostNetwork"
NAME: monitoring
LAST DEPLOYED: Tue Mar 17 18:00:30 2026
NAMESPACE: monitoring
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
kube-prometheus-stack has been installed. Check its status by running:
  kubectl --namespace monitoring get pods -l "release=monitoring"

Get Grafana 'admin' user password by running:

  kubectl --namespace monitoring get secrets monitoring-grafana -o jsonpath="{.data.admin-password}" | base64 -d ; echo

Access Grafana local instance:

  export POD_NAME=$(kubectl --namespace monitoring get pod -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=monitoring" -oname)
  kubectl --namespace monitoring port-forward $POD_NAME 3000

Get your grafana admin user password by running:

  kubectl get secret --namespace monitoring -l app.kubernetes.io/component=admin-secret -o jsonpath="{.items[0].data.admin-password}" | base64 --decode ; echo


Visit https://github.com/prometheus-operator/kube-prometheus for instructions on how to create & configure Alertmanager and Prometheus instances using the Operator.
```
