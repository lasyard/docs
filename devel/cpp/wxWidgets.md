# wxWidgets

<https://www.wxwidgets.org/>

## Download sources

```console
$ curl -LO https://github.com/wxWidgets/wxWidgets/releases/download/v3.2.6/wxWidgets-3.2.6.tar.bz2
```

## Build

:::::{tabs}
::::{tab} macOS Monterey
:::{include} /_files/frags/toolchain/macos_clang_14.txt
:::

Extract sources:

```console
$ tar -C ~/workspace/devel/ -xjf wxWidgets-3.2.6.tar.bz2
$ cd ~/workspace/devel/wxWidgets-3.2.6
```

### Release

```console
$ cmake -S . -B build-x86_64-darwin-release -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=~
$ cd build-x86_64-darwin-release
$ cmake --build . --target install
```

Add `RPATH` for `wxrc`:

```console
$ install_name_tool -add_rpath "@executable_path/../lib" ~/bin/wxrc
```

`wx-config` is used by CMake to find wxWidgets on Unix-like system, so set the path:

```sh
export PATH="${PATH}:${HOME}/bin"
```

To uninstall wxWidgets, run:

```console
$ cmake --build . --target uninstall
```

Check the version:

```console
$ wx-config --version-full
3.2.6.0
```

### Debug

```console
$ cmake -S . -B build-x86_64-darwin-debug -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=~/workspace/devel
$ cd build-x86_64-darwin-debug
$ cmake --build . --target install
```

::::
:::::

## Help messages

```console
wx-config 

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
