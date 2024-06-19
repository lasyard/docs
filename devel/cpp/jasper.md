# jasper

<https://jasper-software.github.io/jasper/>

JasPer is a software toolkit for the handling of image data. The software provides a means for representing images, and facilitates the manipulation of image data, as well as the import/export of such data in numerous formats (e.g., JPEG-2000 JP2, JPEG, PNM, BMP, Sun Rasterfile, and PGX).

## Download Sources

```sh
wget https://github.com/jasper-software/jasper/releases/download/version-4.0.0/jasper-4.0.0.tar.gz
```

## Build

:::{include} /_frags/plats/macos.txt
:::

With toolchains:

- Apple clang 14.0.0
- CMake 3.29.3

Extract sources:

```sh
tar -C ~/workspace/devel -xzf jasper-4.0.0.tar.gz
cd ~/workspace/devel/jasper-4.0.0
```

### Debug

```sh
cmake -S . -B build-x86_64-darwin-debug -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=~/workspace/devel
cd build-x86_64-darwin-debug
cmake --build . --target install
```
