# kafka

<https://kafka.apache.org/>

Apache Kafka is an open-source distributed event streaming platform used by thousands of companies for high-performance data pipelines, streaming analytics, data integration, and mission-critical applications.

:::{plat} centos
{{ cluster_las }}
:::

## Prerequisites

Get shell scripts:

- [install_java_bin](https://github.com/lasyard/coding/blob/main/shell/install_java_bin.sh)

Download java binary packages:

```sh
wget https://mirrors.tuna.tsinghua.edu.cn/apache/kafka/3.7.0/kafka_2.13-3.7.0.tgz
```

Check sum:

```sh
sha512sum kafka_2.13-3.7.0.tgz
```

{.cli-output}

```text
b8679283a2d8dab86e7c636b2c688fe9d9e64ac437241f65ef7a1733f4d26a2bd415eefa04f09f1911373bcd2a5dbc3838c76347f68656425c09202cd290ce91  kafka_2.13-3.7.0.tgz
```

Install and start [zookeeper](project:zookeeper.md) first.

## Deploy

Install the java packages on each node:

```sh
install_java_bin kafka kafka_2.13-3.7.0.tgz /opt
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

```sh
kafka-configs.sh  --version
```

{.cli-output}

```text
3.7.0
```

Start the services on each node:

```sh
sudo /opt/kafka/bin/kafka-server-start.sh -daemon /opt/kafka/config/server.properties
```

```sh
sudo jps -lm
```

:::{literalinclude} /_files/centos/output/jps/lm_zookeeper_kafka.txt
:language: text
:class: cli-output
:::

Stop the services on each node:

```sh
sudo /opt/kafka/bin/kafka-server-stop.sh
```

## Usage

Create a topic:

```sh
kafka-topics.sh --bootstrap-server localhost:9092 --create --topic xxxx --partitions 3 --replication-factor 1
```

List the topics:

```sh
kafka-topics.sh --bootstrap-server localhost:9092 --list
```

Show the details of the topic:

```sh
kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic xxxx
```

:::{literalinclude} /_files/centos/output/kafka/topics_describe.txt
:language: text
:class: cli-output
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

```sh
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
```

Will print out something like:

{.cli-output}

```text
console-consumer-64306
```
