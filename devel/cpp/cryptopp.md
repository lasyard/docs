# cryptopp

## Download sources

```console
$ curl -LO https://cryptopp.com/cryptopp890.zip
```

## Build

:::::{tabs}
::::{tab} macOS Monterey
:::{include} /_files/frags/toolchain/macos_clang_14.txt
:::

### Release

```console
$ unzip -d ~/workspace/devel/cryptopp890-x86_64-darwin-release cryptopp890.zip
$ cd ~/workspace/devel/cryptopp890-x86_64-darwin-release
```

```console
$ make -j all
$ make install PREFIX=~
```

Do this to fix dylib id if you do not want to install:

```console
$ install_name_tool -id $(pwd)/libcryptopp.dylib libcryptopp.dylib
```

To uninstall:

```console
$ make uninstall PREFIX=~
```

Show the version:

```console
$ cryptest.exe V
8.9.0
```

:::{note}
It is strange to have `.exe` suffix executable on macOS.
:::

### Debug

```console
$ unzip -d ~/workspace/devel/cryptopp890-x86_64-darwin-debug cryptopp890.zip
$ cd ~/workspace/devel/cryptopp890-x86_64-darwin-debug
```

```console
$ export CXXFLAGS="${CXXFLAGS} -DDEBUG -g -O0"
$ make -j all
$ make install PREFIX=~/workspace/devel
```

To uninstall:

```console
$ make uninstall PREFIX=~/workspace/devel
```

::::
:::::
