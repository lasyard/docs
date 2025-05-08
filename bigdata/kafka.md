# kafka

<https://kafka.apache.org/>

## Prerequisites

Get shell script [`install_java_bin`](https://github.com/lasyard/coding/blob/main/shell/install_java_bin.sh).

Download java binary packages:

```console
$ curl -LO https://mirrors.tuna.tsinghua.edu.cn/apache/kafka/3.9.0/kafka_2.13-3.9.0.tgz
```

Check sum:

```console
$ sha512sum kafka_2.13-3.9.0.tgz
5324c1f44d4c84ea469712c2cc3d2d15545c3716edbb5353722df9c661fcc78b031fcf07d1c4f0309c5fdb32686665dfb0cffe55210cd3a1fe2a370538cb4e6d  kafka_2.13-3.9.0.tgz
```

Install and start [zookeeper](project:zookeeper.md) first.

## Deploy

Install the java packages on each node:

```console
$ install_java_bin kafka kafka_2.13-3.9.0.tgz /opt
$ sudo chown ubuntu:ubuntu /opt/kafka
```

### Configure

Edit file `/opt/kafka/config/server.properties`:

:::{literalinclude} /_files/ubuntu/opt/kafka/config/server.properties
:diff: /_files/ubuntu/opt/kafka/config/server.properties.orig
:::

This file need to be copied to all nodes to the same path. On each node, the `broker.id` option in the config file must be reset to an unique number, for example, on host `las2`:

```console
$ sudo sed -ie /broker.id=/c\\broker.id=2 /opt/kafka/config/server.properties
```

Create the directory of `${log.dirs}` on each node:

```console
$ sudo mkdir -p /opt/tmp/kafka-logs
$ sudo chown ubuntu:ubuntu /opt/tmp/kafka-logs
```

### Run

Check the version:

```console
$ kafka-configs.sh --version
3.9.0
```

Start the services on each node:

```console
$ kafka-server-start.sh -daemon /opt/kafka/config/server.properties
```

Show java processes:

```console
$ jps -lm
3332661 kafka.Kafka /opt/kafka/config/server.properties
3335576 sun.tools.jps.Jps -lm
3178940 org.apache.zookeeper.server.quorum.QuorumPeerMain /opt/zookeeper/bin/../conf/zoo.cfg
```

Stop the services on each node:

```console
$ kafka-server-stop.sh
```

## Usage

Create, list and show details of a topic:

```console
$ kafka-topics.sh --bootstrap-server localhost:9092 --create --topic xxxx --partitions 3 --replication-factor 1
Created topic xxxx.
$ kafka-topics.sh --bootstrap-server localhost:9092 --list
xxxx
$ kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic xxxx
Topic: xxxx TopicId: 6LCwAbkHTlSz9usG_YDaaw PartitionCount: 3   ReplicationFactor: 1    Configs: 
    Topic: xxxx Partition: 0    Leader: 1   Replicas: 1 Isr: 1  Elr: N/A    LastKnownElr: N/A
    Topic: xxxx Partition: 1    Leader: 0   Replicas: 0 Isr: 0  Elr: N/A    LastKnownElr: N/A
    Topic: xxxx Partition: 2    Leader: 2   Replicas: 2 Isr: 2  Elr: N/A    LastKnownElr: N/A
```

Delete the topic:

```console
$ kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic xxxx
```

Produce messages:

```console
$ kafka-console-producer.sh --bootstrap-server localhost:9092 --topic xxxx
```

Consume messages:

```console
$ kafka-console-consumer.sh --bootstrap-server localhost:9092 --from-beginning --topic xxxx
```

List the consumer groups:

```console
$ kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
console-consumer-79209
```
