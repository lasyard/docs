# kafka

<https://kafka.apache.org/>

:::{plat} centos
{{ cluster_las }}
:::

## Prerequisites

Install JDK on each node, see <project:/devel/java/install.md>.

Get shell scripts [`install_java_bin`](https://github.com/lasyard/coding/blob/main/shell/install_java_bin.sh).

Download java binary packages:

```sh
wget https://mirrors.tuna.tsinghua.edu.cn/apache/kafka/3.9.0/kafka_2.13-3.9.0.tgz
```

Check sum:

```console
$ sha512sum kafka_2.13-3.9.0.tgz
5324c1f44d4c84ea469712c2cc3d2d15545c3716edbb5353722df9c661fcc78b031fcf07d1c4f0309c5fdb32686665dfb0cffe55210cd3a1fe2a370538cb4e6d  kafka_2.13-3.9.0.tgz
```

Install and start <project:zookeeper.md> first.

## Deploy

Install the java packages on each node:

```sh
install_java_bin kafka kafka_2.13-3.9.0.tgz /opt
```

### Configure

```sh
sudo vi /opt/kafka/config/server.properties
```

:::{literalinclude} /_files/centos/opt/kafka/config/server.properties
:diff: /_files/centos/opt/kafka/config/server.properties.orig
:class: file-content
:::

Create the directory of `${log.dirs}` on each node:

```sh
sudo mkdir -p /opt/tmp/kafka-logs
```

### Distribute configuration files

Copy `server.properties` to all nodes and modify option `broker.id` in this file to an unique id number.

For example, on `las2`:

```sh
sudo sed -ie /broker.id=/c\\broker.id=2 /opt/kafka/config/server.properties
```

### Run

Check the version:

```console
kafka-configs.sh  --version
3.9.0
```

Start the services on each node:

```sh
sudo /opt/kafka/bin/kafka-server-start.sh -daemon /opt/kafka/config/server.properties
```

Show java processes:

:::{literalinclude} /_files/centos/console/jps/lm_zookeeper_kafka.txt
:language: console
:::

Stop the services on each node:

```sh
sudo /opt/kafka/bin/kafka-server-stop.sh
```

## Usage

Create/list/show details of a topic:

:::{literalinclude} /_files/centos/console/kafka/topics_create.txt
:language: console
:::

Delete the topic:

```sh
kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic xxxx
```

Produce messages:

```sh
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic xxxx
```

Consume messages:

```sh
kafka-console-consumer.sh --bootstrap-server localhost:9092 --from-beginning --topic xxxx
```

List the consumer groups:

```console
$ kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
console-consumer-7783
```
