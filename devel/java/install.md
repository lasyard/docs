# Install Java Development Environment

::::{tab-set}
:::{tab-item} CentOS 8.5

Install JDK:

```console
$ sudo dnf install java-1.8.0-openjdk
$ sudo dnf install java-1.8.0-openjdk-devel
```

The latter is needed for `jps` command.

:::
:::{tab-item} Ubuntu 22.04

```console
$ sudo apt install openjdk-8-jdk
```

Check the version:

```console
$ java -version
openjdk version "1.8.0_452"
OpenJDK Runtime Environment (build 1.8.0_452-8u452-ga~us1-0ubuntu1~22.04-b09)
OpenJDK 64-Bit Server VM (build 25.452-b09, mixed mode)
```

:::
::::
