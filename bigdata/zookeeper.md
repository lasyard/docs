# zookeeper

<https://zookeeper.apache.org/>

## Prerequisites

Install JDK on each node, see "<project:/devel/java/install.md>".

Get shell script [`install_java_bin`](https://github.com/lasyard/coding/blob/main/shell/install_java_bin.sh).

Download the java binary packages:

```console
curl -LO https://mirrors.tuna.tsinghua.edu.cn/apache/zookeeper/zookeeper-3.9.3/apache-zookeeper-3.9.3-bin.tar.gz
```

Check sum:

```console
$ sha512sum apache-zookeeper-3.9.3-bin.tar.gz 
d44d870c1691662efbf1a8baf1859c901b820dc5ff163b36e81beb27b6fbf3cd31b5f1f075697edaaf6d3e7a4cb0cc92f924dcff64b294ef13d535589bdaf143  apache-zookeeper-3.9.3-bin.tar.gz
```

## Deploy

Install the java packages on each node:

```console
$ install_java_bin zookeeper apache-zookeeper-3.9.3-bin.tar.gz /opt
$ sudo chown ubuntu:ubuntu /opt/zookeeper
```

### Configure

Copy file `/opt/zookeeper/conf/zoo_sample.cfg` to `/opt/zookeeper/conf/zoo.cfg` and edit it:

:::{literalinclude} /_files/ubuntu/opt/zookeeper/conf/zoo.cfg
:diff: /_files/ubuntu/opt/zookeeper/conf/zoo.cfg.orig
:::

This file need to be copied to all nodes to the same path.

Create the directory for `${dataDir}` on each node:

```console
$ sudo mkdir -p /opt/tmp/zookeeper
$ sudo chown ubuntu:ubuntu /opt/tmp/zookeeper
```

Create file `myid` whose content is an unique ID number in directory `/opt/tmp/zookeeper` for each node. For example, on host `las1`:

```console
$ echo 1 >/opt/tmp/zookeeper/myid
```

### Run

Check version:

```console
$ zkServer.sh version
ZooKeeper JMX enabled by default
Using config: /opt/zookeeper/bin/../conf/zoo.cfg
Apache ZooKeeper, version 3.9.3 2024-10-17 23:21 UTC
```

Start the service on each node:

```console
$ zkServer.sh start
ZooKeeper JMX enabled by default
Using config: /opt/zookeeper/bin/../conf/zoo.cfg
Starting zookeeper ... STARTED
```

Show java processes:

```console
$ jps -lm
3155810 org.apache.zookeeper.server.quorum.QuorumPeerMain /opt/zookeeper/bin/../conf/zoo.cfg
3157879 sun.tools.jps.Jps -lm
```

Check service status:

```console
$ zkServer.sh status
ZooKeeper JMX enabled by default
Using config: /opt/zookeeper/bin/../conf/zoo.cfg
Client port found: 2181. Client address: localhost. Client SSL: false.
Mode: follower
```

:::{note}
The last line will be `Mode: leader` if run the command on a leader node. Only one of the nodes should be 'leader' and the others should be 'follower'.
:::

Stop the service on one node:

```console
$ zkServer.sh stop
ZooKeeper JMX enabled by default
Using config: /opt/zookeeper/bin/../conf/zoo.cfg
Stopping zookeeper ... STOPPED
```

There must be at least 3 nodes to make `zookeeper` functions properly.

## Usage

Start the client:

```console
$ zkCli.sh -server las0
```

Check server status:

```console
$ echo srvr | nc las2 2181
Zookeeper version: 3.9.3-c26634f34490bb0ea7a09cc51e05ede3b4e320ee, built on 2024-10-17 23:21 UTC
Latency min/avg/max: 0/0.0/0
Received: 2
Sent: 1
Connections: 1
Outstanding: 0
Zxid: 0x200000002
Mode: leader
Node count: 5
Proposal sizes last/min/max: 48/48/48
```

The admin service is started on port 8080 on each node by default. Open `http://las0:8080/commands` to see the list of available commands.
