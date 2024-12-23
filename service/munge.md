# munge

<https://dun.github.io/munge/>

## Deploy

::::{plat} centos
:vers: CentOS 8.5

### Install packages

For each node:

```sh
sudo dnf install munge
```

Check the version:

```console
$ munge --version
munge-0.5.13 (2017-09-26)
```

### Configure

On one node (las0):

```sh
sudo create-munge-key
```

Copy the generated key to all nodes:

```sh
sudo scp /etc/munge/munge.key las1:/etc/munge
sudo scp /etc/munge/munge.key las2:/etc/munge
```

### Run

```sh
sudo systemctl enable munge --now
```

## Usage

Test it:

```console
$ munge -n
MUNGE:AwQFAAAbcm3gKhmzzkLdUwxGfwUx/PJjXYyA3FXM9WBJ5ufqSPXNPkQWonypxNF7uk1fk8WQAi08mnywDOGA4HlYtkTazLtLT63MP+eIAAGC1hBrMCBNNep2KYrR+dNbxPyjd5k=:
```

Remote authentication:

:::{literalinclude} /_files/centos/console/munge/n_ssh_unmunge.txt
:language: console
:::

::::
