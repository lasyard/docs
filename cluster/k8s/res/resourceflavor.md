# ResourceFlavor

Install kueue first, see <https://kueue.sigs.k8s.io/>.

```sh
vi default_rf.yaml
```

:::{literalinclude} /_files/macos/work/k8s/default_rf.yaml
:language: yaml
:class: file-content
:::

```console
$ kubectl create -f default_rf.yaml 
resourceflavor.kueue.x-k8s.io/default created
```

:::{literalinclude} /_files/macos/console/kubectl/get_rf.txt
:language: console
:::
