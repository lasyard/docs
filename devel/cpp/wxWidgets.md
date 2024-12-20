# wxWidgets

<https://www.wxwidgets.org/>

## Build from sources

Download sources:

```sh
wget https://github.com/wxWidgets/wxWidgets/releases/download/v3.2.6/wxWidgets-3.2.6.tar.bz2
```

::::{plat} macos

:::{include} /_files/frags/toolchain/macos_clang_14.txt
:::

Extract sources:

```sh
tar -C ~/workspace/devel/ -xjf wxWidgets-3.2.6.tar.bz2
cd ~/workspace/devel/wxWidgets-3.2.6
```

### Release

```sh
cmake -S . -B build-x86_64-darwin-release -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=~
cd build-x86_64-darwin-release
cmake --build . --target install
```

Add `RPATH` for `wxrc`:

```sh
install_name_tool -add_rpath "@executable_path/../lib" ~/bin/wxrc
```

`wx-config` is used by CMake to find wxWidgets on Unix-like system, so set the path:

```sh
export PATH="${PATH}:${HOME}/bin"
```

To uninstall wxWidgets, run:

```sh
cmake --build . --target uninstall
```

Check the version:

```console
wx-config --version-full
3.2.6.0
```

Show help:

:::{literalinclude} /_files/macos/console/wx-config/no_args.txt
:language: console
:::

### Debug

```sh
cmake -S . -B build-x86_64-darwin-debug -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=~/workspace/devel
cd build-x86_64-darwin-debug
cmake --build . --target install
```

::::
