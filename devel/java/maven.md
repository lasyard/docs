# maven

<http://maven.apache.org/>

## Usage

### Help

```sh
mvn help:describe -Dplugin=help
mvn help:describe -Dplugin=help -Ddetail
```

### Info

```sh
mvn help:effective-pom
mvn help:effective-settings
```

### Build

```sh
mvn compile
mvn test
mvn verify
mvn package
mvn package -DskipTests
mvn clean
```

### Install

```sh
mvn install
mvn install -Dmaven.javadoc.skip=true
```
