# hbase

<https://hbase.apache.org/>

## Prerequisites

Get shell script [`install_java_bin`](https://github.com/lasyard/coding/blob/main/shell/install_java_bin.sh).

Download the java binary packages:

```console
$ curl -LO https://mirrors.tuna.tsinghua.edu.cn/apache/hbase/2.6.1/hbase-2.6.1-hadoop3-bin.tar.gz
```

Check sum:

```console
$ sha512sum hbase-2.6.1-hadoop3-bin.tar.gz
160d7a79cb21c92101d8e74647477200b541b93d5e75f09648e3a601921119d13f8387beb9f63a9228e67630959227b9ef665d9ac7cbe03e570b7fc4fe1fbfdc  hbase-2.6.1-hadoop3-bin.tar.gz
```

Install and start [hadoop](project:hadoop.md) and [zookeeper](project:zookeeper.md) first.

## Deploy

Install the java packages on each node:

```console
$ install_java_bin hbase hbase-2.6.1-hadoop3-bin.tar.gz /opt
$ sudo chown ubuntu:ubuntu /opt/hbase
```

### Configure

Edit file `/opt/hbase/conf/hbase-env.sh`:

:::{literalinclude} /_files/ubuntu/opt/hbase/conf/hbase-env.sh
:diff: /_files/ubuntu/opt/hbase/conf/hbase-env.sh.orig
:::

Edit file `/opt/hbase/conf/hbase-site.xml`:

:::{literalinclude} /_files/ubuntu/opt/hbase/conf/hbase-site.xml
:diff: /_files/ubuntu/opt/hbase/conf/hbase-site.xml.orig
:::

These files need to be copied to all nodes to the same path.

Edit file `/opt/hbase/conf/regionservers`:

:::{literalinclude} /_files/ubuntu/opt/hbase/conf/regionservers
:diff: /_files/ubuntu/opt/hbase/conf/regionservers.orig
:::

Create the directory of `${hbase.tmp.dir}` on each node:

```console
$ sudo mkdir -p /opt/tmp/hbase
$ sudo chown ubuntu:ubuntu /opt/tmp/hbase
```

### Run

Check the version:

```console
$ hbase version
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/opt/hadoop-3.4.1/share/hadoop/common/lib/slf4j-reload4j-1.7.36.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/opt/hbase-2.6.1-hadoop3/lib/client-facing-thirdparty/log4j-slf4j-impl-2.17.2.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.slf4j.impl.Reload4jLoggerFactory]
HBase 2.6.1-hadoop3
Source code repository git://5d132f6e0305/home/ndimiduk/hbase-rm/output/hbase revision=7ed50b4dd742269a78875fb32112215f831284ff
Compiled by ndimiduk on Wed Oct  9 10:53:48 UTC 2024
From source with checksum 63fc9a9f53780d4b96c58332d1d251bf2bd04ee73c45f2e19ab5e6ecf85efb343c3c23607362913ec3ef5a66602026b363e38e43821664f38e96830ed818c41d
```

Start hbase:

```console
$ start-hbase.sh
...
running master, logging to /opt/hbase/bin/../logs/hbase-ubuntu-master-k8ctl.out
las2: running regionserver, logging to /opt/hbase/bin/../logs/hbase-ubuntu-regionserver-k8cpu1.out
las0: running regionserver, logging to /opt/hbase/bin/../logs/hbase-ubuntu-regionserver-k8ctl.out
las1: running regionserver, logging to /opt/hbase/bin/../logs/hbase-ubuntu-regionserver-k8cpu0.out
```

Show java processes:

```console
$ jps -lm
3178161 org.apache.hadoop.hdfs.server.datanode.DataNode
3183385 sun.tools.jps.Jps -lm
3182457 org.apache.hadoop.hbase.regionserver.HRegionServer start
3181994 org.apache.hadoop.hbase.master.HMaster start
3177962 org.apache.hadoop.hdfs.server.namenode.NameNode
3178940 org.apache.zookeeper.server.quorum.QuorumPeerMain /opt/zookeeper/bin/../conf/zoo.cfg
3178511 org.apache.hadoop.hdfs.server.namenode.SecondaryNameNode
```

Stop hbase:

```console
$ stop-hbase.sh
stopping hbase..............
...
```

:::{tip}
If the command above does not work, try these commands:

```console
$ hbase-daemon.sh stop regionserver
running regionserver, logging to /opt/hbase/bin/../logs/hbase-ubuntu-regionserver-k8ctl.out
stopping regionserver.
$ hbase-daemon.sh stop master
running master, logging to /opt/hbase/bin/../logs/hbase-ubuntu-master-k8ctl.out
stopping master..
```

:::

## Usage

```console
$ hbase shell
```

In hbase shell:

```sql
help
quit
```

Open the web UI at `http://las0:16010/`.
