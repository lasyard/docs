# jasper

<https://jasper-software.github.io/jasper/>

## Download sources

```sh
curl -LO https://github.com/jasper-software/jasper/releases/download/version-4.2.4/jasper-4.2.4.tar.gz
```

## Build

Extract sources:

```console
$ tar -C ~/workspace/devel -xzf jasper-4.2.4.tar.gz
$ cd ~/workspace/devel/jasper-4.2.4
```

### Debug

:::::{tab-set}
::::{tab-item} macOS Monterey

:::{include} /_files/frags/toolchain/macos_clang_14.txt
:::

```console
$ cmake -S . -B ../jasper-4.2.4-build-x86_64-darwin-debug -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=~/workspace/devel
$ cd ../jasper-4.2.4-build-x86_64-darwin-debug
$ cmake --build . --target install
```

::::
:::::
