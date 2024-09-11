# munge

<https://dun.github.io/munge/>

MUNGE (MUNGE Uid 'N' Gid Emporium) is an authentication service for creating and validating credentials.

## Deploy

::::{plat} centos
{{ cluster_las }}

### Install packages

For each node:

```sh
sudo dnf install munge
```

### Configure

On one node (las1):

```sh
sudo create-munge-key
```

Copy the generated key to all nodes:

```sh
sudo scp /etc/munge/munge.key las2:/etc/munge
sudo scp /etc/munge/munge.key las3:/etc/munge
```

### Run

```sh
sudo systemctl enable munge --now
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

::::
