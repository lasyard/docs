# Build on macOS Tahoe (Apple silicon)

:::{include} /_files/frags/toolchain/macos_clang_21.txt
:::

Download sources:

```console
$ curl -LO https://github.com/wxWidgets/wxWidgets/releases/download/v3.3.2/wxWidgets-3.3.2.tar.bz2
```

Extract sources:

```console
$ tar -C ~/workspace/devel/ -xjf wxWidgets-3.3.2.tar.bz2
$ cd ~/workspace/devel/wxWidgets-3.3.2
```

## Release

```console
$ cmake -S . -B build-arm64-darwin-release -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=~
-- The C compiler identification is AppleClang 21.0.0.21000099
-- The CXX compiler identification is AppleClang 21.0.0.21000099
-- The OBJCXX compiler identification is AppleClang 21.0.0.21000099
...
-- Which libraries should wxWidgets use?
    wxUSE_REGEX:      builtin  (enable support for wxRegEx class)
    wxUSE_ZLIB:       sys      (use zlib for LZW compression)
    wxUSE_EXPAT:      sys      (use expat for XML parsing)
    wxUSE_LIBJPEG:    builtin  (use libjpeg (JPEG file format))
    wxUSE_LIBPNG:     builtin  (use libpng (PNG image format))
    wxUSE_LIBTIFF:    builtin  (use libtiff (TIFF file format))
    wxUSE_LIBWEBP:    builtin  (use libwebp (WebP file format))
    wxUSE_NANOSVG:    builtin  (use NanoSVG for rasterizing SVG)
    wxUSE_LUNASVG:    OFF      (use LunaSVG for rasterizing SVG (C++17 minimum))
    wxUSE_LIBLZMA:    OFF      (use liblzma for LZMA compression)
    wxUSE_LIBSDL:     OFF      (use SDL for audio on Unix)
    wxUSE_LIBMSPACK:  OFF      (use libmspack (CHM help files loading))
    wxUSE_WEBVIEW:    ON       (enable wxWebview with WebKit)

-- Configured wxWidgets 3.3.2 for Darwin
    Min OS Version required at runtime:                macOS 10.10 arm64
    Which GUI toolkit should wxWidgets use?            osx_cocoa  
    Should wxWidgets be compiled into single library?  OFF
    Should wxWidgets be linked as a shared library?    ON
    Which wxWidgets API compatibility should be used?  3.2
-- Configuring done (11.1s)
-- Generating done (0.2s)
-- Build files have been written to: /Users/xxxx/workspace/devel/wxWidgets-3.3.2/build-arm64-darwin-release
$ cd build-arm64-darwin-release
$ cmake --build . --target install
```

:::{note}
`RPATH` for `wxrc` need to be fixed:

```console
$ install_name_tool -add_rpath "@executable_path/../lib" ~/bin/wxrc
```

:::

`wx-config` is used by CMake to find wxWidgets on Unix-like system, so set the path:

```sh
export PATH="${PATH}:${HOME}/bin"
```

Check the version:

```console
$ wx-config --version-full
3.3.2.0
```

## Debug

```console
$ cmake -S . -B build-arm64-darwin-debug -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=~/workspace/devel
...
-- Build files have been written to: /Users/xxxx/workspace/devel/wxWidgets-3.3.1/build-x86_64-darwin-debug
$ cd build-arm64-darwin-debug
$ cmake --build . --target install
```
