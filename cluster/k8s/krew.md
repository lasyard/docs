# Krew

<https://krew.sigs.k8s.io/>

## Install

::::{tab-set}
:::{tab-item} macOS

```sh
(
  set -x; cd "$(mktemp -d)" &&
  OS="$(uname | tr '[:upper:]' '[:lower:]')" &&
  ARCH="$(uname -m | sed -e 's/x86_64/amd64/' -e 's/\(arm\)\(64\)\?.*/\1\2/' -e 's/aarch64$/arm64/')" &&
  KREW="krew-${OS}_${ARCH}" &&
  curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/latest/download/${KREW}.tar.gz" &&
  tar zxvf "${KREW}.tar.gz" &&
  ./"${KREW}" install krew
)
```

The output:

```console
...
./krew-darwin_amd64 install krew
Adding "default" plugin index from https://github.com/kubernetes-sigs/krew-index.git.
Updated the local copy of plugin index.
Installing plugin: krew
Installed plugin: krew
\
 | Use this plugin:
 | 	kubectl krew
 | Documentation:
 | 	https://krew.sigs.k8s.io/
 | Caveats:
 | \
 |  | krew is now installed! To start using kubectl plugins, you need to add
 |  | krew's installation directory to your PATH:
 |  | 
 |  |   * macOS/Linux:
 |  |     - Add the following to your ~/.bashrc or ~/.zshrc:
 |  |         export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"
 |  |     - Restart your shell.
 |  | 
 |  |   * Windows: Add %USERPROFILE%\.krew\bin to your PATH environment variable
 |  | 
 |  | To list krew commands and to get help, run:
 |  |   $ kubectl krew
 |  | For a full list of available plugins, run:
 |  |   $ kubectl krew search
 |  | 
 |  | You can find documentation at
 |  |   https://krew.sigs.k8s.io/docs/user-guide/quickstart/.
 | /
/
```

Show the version:

```console
$ kubectl krew version  
OPTION            VALUE
GitTag            v0.4.5
GitCommit         e7e5b61
IndexURI          https://github.com/kubernetes-sigs/krew-index.git
BasePath          /Users/xxxx/.krew
IndexPath         /Users/xxxx/.krew/index/default
InstallPath       /Users/xxxx/.krew/store
BinPath           /Users/xxxx/.krew/bin
DetectedPlatform  darwin/amd64
```

:::
::::

## Usage

Upgrade krew:

```console
$ kubectl krew upgrade
Updated the local copy of plugin index.
Upgrading plugin: krew
Skipping plugin krew, it is already on the newest version
```

Update the index:

```console
$ kubectl krew update
Updated the local copy of plugin index.
```

Search plugins:

```console
$ kubectl krew search kueue
```

Install a plugin:

```console
$ kubectl krew install kueue
```
