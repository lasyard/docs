# node

<https://nodejs.org/>

## Using nvm

Install `nvm`:

```sh
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

Check the version:

```console
$ nvm --version
0.39.7
```

Show current node version:

```console
$ nvm version
v23.4.0
```

List all installed `node` versions:

:::{literalinclude} /_files/macos/console/nvm/list.txt
:language: console
:::

Use `node` installed in system:

```sh
nvm use system
```

Install latest `node`:

```sh
nvm install node
```

Uninstall a version:

```sh
nvm uninstall 22.7.0
```

## Uninstall node

If node is installed using downloaded package on macOS, run [macos_uninstall_node.sh](https://github.com/lasyard/coding/blob/main/shell/macos_uninstall_node.sh) to uninstall it.
