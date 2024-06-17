# wxWidgets

<https://www.wxwidgets.org/>

wxWidgets is a C++ library that lets developers create applications for Windows, macOS, Linux and other platforms with a single code base.

## Download Sources

```sh
wget https://github.com/wxWidgets/wxWidgets/releases/download/v3.2.5/wxWidgets-3.2.5.tar.bz2
```

## Build

### macOS

:CPU: x86-64 * 2
:OS: macOS Monterey
:Toolchain: Apple clang 14.0.0, CMake 3.29.3
:wxWidgets: 3.2.5

Extract sources:

```sh
tar -C ~/workspace/devel/ -xjf wxWidgets-3.2.5.tar.bz2
cd ~/workspace/devel/wxWidgets-3.2.5
```

#### Release

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

#### Debug

```sh
cmake -S . -B build-x86_64-darwin-debug -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=~/workspace/devel
cd build-x86_64-darwin-debug
cmake --build . --target install
```
