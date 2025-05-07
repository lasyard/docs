# maven

<http://maven.apache.org/>

## Help

```console
$ mvn help:describe -Dplugin=help
$ mvn help:describe -Dplugin=help -Ddetail
```

## Info

```console
$ mvn help:effective-pom
$ mvn help:effective-settings
```

## Build

```console
$ mvn compile
$ mvn test
$ mvn verify
$ mvn package
$ mvn package -DskipTests
$ mvn clean
```

## Install

```console
$ mvn install
$ mvn install -Dmaven.javadoc.skip=true
```
