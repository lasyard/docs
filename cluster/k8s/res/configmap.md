# ConfigMap

Create a properties file:

```sh
vi slurm.properties
```

:::{literalinclude} /_files/centos/work/kubectl/slurm.properties
:language: properties
:class: file-content
:::

Create a config map from it:

:::{literalinclude} /_files/centos/console/kubectl/create_cm.txt
:language: console
:::

:::{tip}
Shortname of `configmap` is `cm`.
:::

Show config maps:

:::{literalinclude} /_files/centos/console/kubectl/get_cm.txt
:language: console
:::

See the details of the new config map:

:::{literalinclude} /_files/centos/console/kubectl/describe_cm_1.txt
:language: console
:::

Alternatively, you can check the data by:

:::{literalinclude} /_files/centos/console/kubectl/get_cm_1.txt
:language: console
:::

Remove the config map:

:::{literalinclude} /_files/centos/console/kubectl/delete_cm.txt
:language: console
:::

If you want to break the content of `.properties` file into multiple config map keys, you can use:

:::{literalinclude} /_files/centos/console/kubectl/create_cm_5.txt
:language: console
:::

:::{literalinclude} /_files/centos/console/kubectl/get_cm_5.txt
:language: console
:::

:::{literalinclude} /_files/centos/console/kubectl/describe_cm_5.txt
:language: console
:::

Note the differences.
