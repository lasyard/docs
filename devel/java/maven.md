# maven

<http://maven.apache.org/>

## Install

### By package manager

:::::{tab-set}
::::{tab-item} Ubuntu
:sync: ubuntu

```console
$ sudo apt install maven
```

```console
$ mvn -version
Apache Maven 3.6.3
Maven home: /usr/share/maven
Java version: 1.8.0_492, vendor: Private Build, runtime: /usr/lib/jvm/java-8-openjdk-amd64/jre
Default locale: en, platform encoding: UTF-8
OS name: "linux", version: "5.15.0-176-generic", arch: "amd64", family: "unix"
```

A little old!

::::
:::::

### From release binaries

Download the binaries:

```console
$ curl -LO https://dlcdn.apache.org/maven/maven-3/3.9.16/binaries/apache-maven-3.9.16-bin.tar.gz
```

Get shell script [`install_java_bin`](https://github.com/lasyard/coding/blob/main/shell/install_java_bin.sh).

```console
$ install_java_bin maven apache-maven-3.9.16-bin.tar.gz /opt
'/opt/maven' -> '/opt/apache-maven-3.9.16'
PATH="/opt/maven/bin:${PATH}"
"/opt/maven/bin" added to "/etc/profile.d/maven.sh".
"/opt/maven/sbin" is not a directory.
```

After relogin, check the version:

```console
$ mvn -version
Apache Maven 3.9.16 (2bdd9fddda4b155ebf8000e807eb73fd829a51d5)
Maven home: /opt/maven
Java version: 1.8.0_492, vendor: Private Build, runtime: /usr/lib/jvm/java-8-openjdk-amd64/jre
Default locale: en, platform encoding: UTF-8
OS name: "linux", version: "5.15.0-176-generic", arch: "amd64", family: "unix"
```

## Usage

### Help

```console
$ mvn help:describe -Dplugin=help
$ mvn help:describe -Dplugin=help -Ddetail
```

### Info

```console
$ mvn help:effective-pom
$ mvn help:effective-settings
```

### Build

```console
$ mvn compile
$ mvn test
$ mvn verify
$ mvn package
$ mvn package -DskipTests
$ mvn clean
```

### Install packages

```console
$ mvn install
$ mvn install -Dmaven.javadoc.skip=true
```
