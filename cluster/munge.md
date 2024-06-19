# munge

<https://dun.github.io/munge/>

MUNGE (MUNGE Uid 'N' Gid Emporium) is an authentication service for creating and validating credentials.

## Deploy

:::{include} /_frags/plats/centos.txt
:::

:::{include} /_frags/nodes/las.txt
:::

### Install

For each node:

```sh
dnf install munge
```

### Configure

On one node (las1):

```sh
create-munge-key
```

Copy the generated key to all nodes:

```sh
scp /etc/munge/munge.key las2:/etc/munge
scp /etc/munge/munge.key las3:/etc/munge
```

### Run

```sh
systemctl enable munge --now
```

## Usage

```sh
munge -n
```

{.cli-output}

```text
MUNGE:AwQFAADjb5/o31f4eJ5qFK9EAdAAuWjNCuI8olcSS93IDFo8owJiPZBu7XmNy/42t3jSmTOwqNjCqtSW0Hk7gYy/xkFCHSWtEEv7Mofiqf3DnHYwyj+BqDa02KlgXfLEajeOdvg=:
```

```sh
munge -n -t 10 | ssh las2 unmunge
```

:::{literalinclude} /_files/centos/output/munge/n_unmunge.txt
:language: text
:class: cli-output
:::
