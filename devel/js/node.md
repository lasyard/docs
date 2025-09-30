# node

<https://nodejs.org/>

## Using nvm

Install `nvm`:

```console
$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
...
=> Compressing and cleaning up git repository

=> Appending nvm source string to /Users/xxxx/.zshrc
=> Appending bash_completion source string to /Users/xxxx/.zshrc
=> Close and reopen your terminal to start using nvm or run the following to use it now:

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
```

Check the version:

```console
$ nvm --version
0.40.3
```

Use `node` installed in system:

```console
$ nvm use system
```

List available version:

```console
$ nvm ls-remote
...
        v24.5.0
        v24.6.0
        v24.7.0
        v24.8.0
->      v24.9.0
```

Install a specified version:

```console
$ nvm install v24.9.0
Downloading and installing node v24.9.0...
Downloading https://nodejs.org/dist/v24.9.0/node-v24.9.0-darwin-x64.tar.xz...
############################################################################################################################################### 100.0%
Computing checksum with shasum -a 256
Checksums matched!
Now using node v24.9.0 (npm v11.6.0)
```

Show the current node version:

```console
$ nvm version
v24.9.0
$ node --version
v24.9.0
```

List all installed `node` versions:

```console
$ nvm list
->      v24.9.0
default -> node (-> v24.9.0)
iojs -> N/A (default)
unstable -> N/A (default)
node -> stable (-> v24.9.0) (default)
stable -> 24.9 (-> v24.9.0) (default)
lts/* -> lts/jod (-> N/A)
lts/argon -> v4.9.1 (-> N/A)
lts/boron -> v6.17.1 (-> N/A)
lts/carbon -> v8.17.0 (-> N/A)
lts/dubnium -> v10.24.1 (-> N/A)
lts/erbium -> v12.22.12 (-> N/A)
lts/fermium -> v14.21.3 (-> N/A)
lts/gallium -> v16.20.2 (-> N/A)
lts/hydrogen -> v18.20.8 (-> N/A)
lts/iron -> v20.19.5 (-> N/A)
lts/jod -> v22.20.0 (-> N/A)
```

Uninstall a version:

```console
$ nvm uninstall v24.5.0
Uninstalled node v24.5.0
```

## Uninstall node

If node is installed using downloaded package on macOS, run [macos_uninstall_node.sh](https://github.com/lasyard/coding/blob/main/shell/macos_uninstall_node.sh) to uninstall it.
