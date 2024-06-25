# maven

<http://maven.apache.org/>

Apache Maven is a software project management and comprehension tool. Based on the concept of a project object model (POM), Maven can manage a project's build, reporting and documentation from a central piece of information.

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
