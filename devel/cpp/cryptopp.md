# cryptopp

## Build from sources

Download sources:

```sh
wget https://cryptopp.com/cryptopp890.zip
wget https://cryptopp.com/cryptopp890.zip.sig
```

```sh
gpg --verify cryptopp890.zip.sig
```

:::{note}
The signature has expired.
:::

::::{plat} macos
The toolchain used:

- Apple clang 14.0.0
- GNU Make 3.81

### Release

```sh
unzip -d ~/workspace/devel/cryptopp890-x86_64-darwin-release cryptopp890.zip
cd ~/workspace/devel/cryptopp890-x86_64-darwin-release
```

```sh
make all
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

See the version:

```sh
cryptest.exe V
```

{.cli-output}

```text
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
export CXXFLAGS="-DDEBUG -g -O0"
make all
make install PREFIX=~/workspace/devel
```

To uninstall:

```sh
make uninstall PREFIX=~/workspace/devel
```

::::
