# Secret

Create a docker registry accessing secret:

```console
$ kubectl create secret docker-registry xxxx-habor --docker-server=habor.xxxx.org --docker-username=xxxx --docker-password=xxxxxxxx
secret/xxxx-habor created
```

:::{literalinclude} /_files/centos/console/kubectl/get_secret_oyaml.txt
:language: console
:::

The `.dockerconfigjson` field is just base64 encoded docker config file, see:

```console
$ kubectl get secret xxxx-habor -o "jsonpath={.data.\.dockerconfigjson}" | base64 --decode
{"auths":{"habor.xxxx.org":{"username":"xxxx","password":"xxxxxxxx","auth":"eHh4eDp4eHh4eHh4eA=="}}}
```
