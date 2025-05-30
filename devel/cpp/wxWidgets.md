# wxWidgets

<https://www.wxwidgets.org/>

## Download sources

```console
$ curl -LO https://github.com/wxWidgets/wxWidgets/releases/download/v3.2.8/wxWidgets-3.2.8.tar.bz2
```

## Build

Extract sources:

```console
$ tar -C ~/workspace/devel/ -xjf wxWidgets-3.2.8.tar.bz2
$ cd ~/workspace/devel/wxWidgets-3.2.8
```

### Release

:::::{tab-set}
::::{tab-item} macOS Monterey

:::{include} /_files/frags/toolchain/macos_clang_18.txt
:::

```console
$ cmake -S . -B build-x86_64-darwin-release -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=~
-- The C compiler identification is Clang 18.1.8
-- The CXX compiler identification is Clang 18.1.8
-- The OBJCXX compiler identification is Clang 18.1.8
...
-- Which libraries should wxWidgets use?
    wxUSE_STL:        OFF      (use C++ STL classes)
    wxUSE_REGEX:      builtin  (enable support for wxRegEx class)
    wxUSE_ZLIB:       sys      (use zlib for LZW compression)
    wxUSE_EXPAT:      sys      (use expat for XML parsing)
    wxUSE_LIBJPEG:    builtin  (use libjpeg (JPEG file format))
    wxUSE_LIBPNG:     builtin  (use libpng (PNG image format))
    wxUSE_LIBTIFF:    builtin  (use libtiff (TIFF file format))
    wxUSE_NANOSVG:    builtin  (use NanoSVG for rasterizing SVG)
    wxUSE_LIBLZMA:    OFF      (use liblzma for LZMA compression)
    wxUSE_LIBSDL:     OFF      (use SDL for audio on Unix)
    wxUSE_LIBMSPACK:  OFF      (use libmspack (CHM help files loading))

-- Configured wxWidgets 3.2.8 for Darwin
    Min OS Version required at runtime:                macOS 10.10 x86_64
    Which GUI toolkit should wxWidgets use?            osx_cocoa  
    Should wxWidgets be compiled into single library?  OFF
    Should wxWidgets be linked as a shared library?    ON
    Should wxWidgets support Unicode?                  ON
    What wxWidgets compatibility level should be used? 3.0
-- Configuring done (53.7s)
-- Generating done (1.2s)
-- Build files have been written to: /Users/xxxx/workspace/devel/wxWidgets-3.2.8/build-x86_64-darwin-release
$ cd build-x86_64-darwin-release
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
3.2.8.0
```

:::{tip}
To uninstall wxWidgets, run:

```console
$ cmake --build . --target uninstall
```

:::

::::
:::::

### Debug

:::::{tab-set}
::::{tab-item} macOS Monterey

:::{include} /_files/frags/toolchain/macos_clang_18.txt
:::

```console
$ cmake -S . -B build-x86_64-darwin-debug -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=~/workspace/devel
...
-- Build files have been written to: /Users/xxxx/workspace/devel/wxWidgets-3.2.8/build-x86_64-darwin-debug
$ cd build-x86_64-darwin-debug
$ cmake --build . --target install
```

::::
:::::

## Help messages

```console
$ wx-config

 wx-config [--prefix[=DIR]] [--exec-prefix[=DIR]] [--release] [--version-full]
           [--list] [--selected-config] [--host=HOST] [--toolkit=TOOLKIT]
           [--universal[=yes|no]] [--unicode[=yes|no]] [--static[=yes|no]]
           [--debug[=yes|no]] [--version[=VERSION]] [--flavour=FLAVOUR]
           [--basename] [--cc] [--cxx]
           [--cppflags [base]] [--cxxflags [base]] [--cflags]
           [--rescomp] [--linkdeps] [--ld] [--utility=UTIL]
           [--libs [LIBS...]] [--optional-libs [LIBS...]]

    wx-config returns information about the wxWidgets libraries available on
  your system.  It may be used to retrieve the information required to build
  applications using these libraries using --cppflags, --cxxflags, --cflags,
  and --libs options. And you may query the properties of this configuration
  using  --query-{host,toolkit,widgetset,chartype,debugtype,version,flavour,
  linkage}.

    NOTE:    Usage of --debug and --query-debugtype are only relevant if you
  have any  versions prior to 2.9 installed  and use the --version option to
  select an earlier version.

    If multiple builds of wxWidgets  are available,  you can use the options
  --prefix, --host, --toolkit,  --unicode, --static, --universal,  --version
  or --flavour to select from them.  The --selected-config option shows  the
  name of the current configuration and --list  shows available alternatives
  which match specified criteria.  The --utility option  returns the correct
  version of  UTIL to use with  the selected build.  The  --linkdeps  option
  returns only static libraries for your makefile link rule dependencies.

    The LIBS arguments (comma or space separated) may be used to specify the
  wxWidgets libraries that  you wish to use. The "std" label may be used  to
  import all libraries that would be used by default if none were  specified
  explicitly, e.g. wx-config --libs core,base. The "all" label may  be  used
  to  import  all libraries that have been compiled which are shown  in  the
  list  below.  The  --optional-libs parameter should be followed by  a list
  of  libs that should be linked to, but only if they are available.

  Available libraries in this build are:
  xrc webview stc richtext ribbon propgrid aui gl media html qa adv core xml net base
```
