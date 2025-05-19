# ConfigMap

Create a properties file `girls.properties`:

:::{literalinclude} /_files/macos/workspace/k8s/girls.properties
:language: properties
:::

Create a ConfigMap from it:

```console
$ kubectl create cm girls --from-file=girls.properties
configmap/girls created
```

Show ConfigMaps:

```console
$ kubectl get cm
NAME                    DATA   AGE
girls                   1      58s
kube-root-ca.crt        1      7d3h
```

See the details of the new ConfigMap:

```console
$ kubectl describe cm girls
Name:         girls
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
girls.properties:
----
girl0=Alice
girl1=Betty



BinaryData
====

Events:  <none>
```

Alternatively, you can check the data by:

```console
$ kubectl get cm girls -o yaml
apiVersion: v1
data:
  girls.properties: |
    girl0=Alice
    girl1=Betty
kind: ConfigMap
metadata:
  creationTimestamp: "2025-05-19T07:37:42Z"
  name: girls
  namespace: default
  resourceVersion: "2554054"
  uid: 54f913c4-e9c6-43c9-8958-8c3c835c0cb6
```

Remove the config map:

```console
$ kubectl delete cm girls
configmap "girls" deleted
```

If you want to break the content of `.properties` file into multiple ConfigMap keys, you can use:

```console
$ kubectl create cm girls --from-env-file=girls.properties
configmap/girls created
```

Note the difference between `--from-file` and `--from-env-file`.

```console
$ kubectl get cm
NAME                    DATA   AGE
girls                   2      2m8s
kube-root-ca.crt        1      7d3h
$ kubectl describe cm girls       
Name:         girls
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
girl1:
----
Betty

girl0:
----
Alice


BinaryData
====

Events:  <none>
```

Note the differences.
