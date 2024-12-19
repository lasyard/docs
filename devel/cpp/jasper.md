# jasper

<https://jasper-software.github.io/jasper/>

## Build form sources

Download sources:

```sh
wget https://github.com/jasper-software/jasper/releases/download/version-4.2.4/jasper-4.2.4.tar.gz
```

::::{plat} macos
:vers: macOS Monterey

:::{include} /_files/frags/toolchain/macos_clang_llvm.txt
:::

Extract sources:

```sh
tar -C ~/workspace/devel -xzf jasper-4.2.4.tar.gz
cd ~/workspace/devel/jasper-4.2.4
```

### Debug

```sh
cmake -S . -B ../build-x86_64-darwin-debug -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=~/workspace/devel
cd ../build-x86_64-darwin-debug
cmake --build . --target install
```

::::
