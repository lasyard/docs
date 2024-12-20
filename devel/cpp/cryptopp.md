# cryptopp

## Build from sources

Download sources:

```sh
wget https://cryptopp.com/cryptopp890.zip
```

::::{plat} macos

:::{include} /_files/frags/toolchain/macos_clang_14.txt
:::

### Release

```sh
unzip -d ~/workspace/devel/cryptopp890-x86_64-darwin-release cryptopp890.zip
cd ~/workspace/devel/cryptopp890-x86_64-darwin-release
```

```sh
make -j all
make install PREFIX=~
```

Do this if you do not want to install:

```sh
# Fix dylib id
install_name_tool -id $(pwd)/libcryptopp.dylib libcryptopp.dylib
```

To uninstall:

```sh
make uninstall PREFIX=~
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

```sh
unzip -d ~/workspace/devel/cryptopp890-x86_64-darwin-debug cryptopp890.zip
cd ~/workspace/devel/cryptopp890-x86_64-darwin-debug
```

```sh
export CXXFLAGS="${CXXFLAGS} -DDEBUG -g -O0"
make -j all
make install PREFIX=~/workspace/devel
```

To uninstall:

```sh
make uninstall PREFIX=~/workspace/devel
```

::::
