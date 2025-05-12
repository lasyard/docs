# hadoop

<https://hadoop.apache.org/>

## Prerequisites

Install JDK on each node, see "<project:/devel/java/install.md>".

Get shell script [`install_java_bin`](https://github.com/lasyard/coding/blob/main/shell/install_java_bin.sh).

Download the java binary packages:

```console
$ curl -LO https://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common/hadoop-3.4.1/hadoop-3.4.1.tar.gz
```

Check sum:

```console
$ sha512sum hadoop-3.4.1.tar.gz
09cda6943625bc8e4307deca7a4df76d676a51aca1b9a0171938b793521dfe1ab5970fdb9a490bab34c12a2230ffdaed2992bad16458169ac51b281be1ab6741  hadoop-3.4.1.tar.gz
```

Set password-free login to all workers (even it is the same node where the commands are emitted) for the user used (in this case, it is `ubuntu`).

## Deploy

Install the java packages on each node:

```console
$ install_java_bin hadoop hadoop-3.4.1.tar.gz /opt
$ sudo chown ubuntu:ubuntu /opt/hadoop
```

Set environment variables on each node:

```console
$ echo "export HADOOP_HOME=\"/opt/hadoop\"" | sudo tee -a /etc/profile.d/hadoop.sh
$ echo "export HADOOP_CLASSPATH=\"\$(\${HADOOP_HOME}/bin/hadoop classpath)\"" | sudo tee -a /etc/profile.d/hadoop.sh
```

### Configure

Edit file `/opt/hadoop/etc/hadoop/hadoop-env.sh`:

:::{literalinclude} /_files/ubuntu/opt/hadoop/etc/hadoop/hadoop-env.sh
:diff: /_files/ubuntu/opt/hadoop/etc/hadoop/hadoop-env.sh.orig
:::

Edit file `/opt/hadoop/etc/hadoop/core-site.xml`:

:::{literalinclude} /_files/ubuntu/opt/hadoop/etc/hadoop/core-site.xml
:diff: /_files/ubuntu/opt/hadoop/etc/hadoop/core-site.xml.orig
:::

These files need to be copied to all nodes to the same path.

Create the directory for `${hadoop.tmp.dir}` on each node:

```console
$ sudo mkdir -p /opt/tmp/hadoop
$ sudo chown ubuntu:ubuntu /opt/tmp/hadoop
```

Edit file `/opt/hadoop/etc/hadoop/workers`:

:::{literalinclude} /_files/ubuntu/opt/hadoop/etc/hadoop/workers
:diff: /_files/ubuntu/opt/hadoop/etc/hadoop/workers.orig
:::

#### Configure hdfs

Edit file `/opt/hadoop/etc/hadoop/hdfs-site.xml`:

:::{literalinclude} /_files/ubuntu/opt/hadoop/etc/hadoop/hdfs-site.xml
:diff: /_files/ubuntu/opt/hadoop/etc/hadoop/hdfs-site.xml.orig
:::

This file need to be copied to all nodes to the same path.

#### Configure yarn

Edit file `/opt/hadoop/etc/hadoop/yarn-site.xml`:

:::{literalinclude} /_files/ubuntu/opt/hadoop/etc/hadoop/yarn-site.xml
:diff: /_files/ubuntu/opt/hadoop/etc/hadoop/yarn-site.xml.orig
:::

Edit file `/opt/hadoop/etc/hadoop/mapred-site.xml`:

:::{literalinclude} /_files/ubuntu/opt/hadoop/etc/hadoop/mapred-site.xml
:diff: /_files/ubuntu/opt/hadoop/etc/hadoop/mapred-site.xml.orig
:::

These files need to be copied to all nodes to the same path.

### Run

Check the version:

```console
$ hadoop version
Hadoop 3.4.1
Source code repository https://github.com/apache/hadoop.git -r 4d7825309348956336b8f06a08322b78422849b1
Compiled by mthakur on 2024-10-09T14:57Z
Compiled on platform linux-x86_64
Compiled with protoc 3.23.4
From source with checksum 7292fe9dba5e2e44e3a9f763fce3e680
This command was run using /opt/hadoop-3.4.1/share/hadoop/common/hadoop-common-3.4.1.jar
```

Init hdfs:

```console
$ hdfs namenode -format
...
/************************************************************
SHUTDOWN_MSG: Shutting down NameNode at las0/10.225.4.51
************************************************************/
```

Start hdfs:

```console
$ start-dfs.sh
Starting namenodes on [las0]
Starting datanodes
Starting secondary namenodes [las0]
```

Start yarn:

```console
$ start-yarn.sh
Starting resourcemanager
Starting nodemanagers
```

Show java processes:

```console
$ jps -lm
2509842 org.apache.hadoop.hdfs.server.namenode.SecondaryNameNode
2510720 org.apache.hadoop.yarn.server.resourcemanager.ResourceManager
2509278 org.apache.hadoop.hdfs.server.namenode.NameNode
2511597 sun.tools.jps.Jps -lm
2509499 org.apache.hadoop.hdfs.server.datanode.DataNode
2510937 org.apache.hadoop.yarn.server.nodemanager.NodeManager
```

Stop them:

```console
$ stop-yarn.sh
Stopping nodemanagers
Stopping resourcemanager
$ stop-dfs.sh
Stopping namenodes on [las0]
Stopping datanodes
Stopping secondary namenodes [las0]
```

## Usage

### hdfs

```console
$ hdfs dfs -ls /
$ hdfs dfs -mkdir -p /user/ubuntu
$ echo 'Hello world!' > file.dat
$ hdfs dfs -put file.dat
$ hdfs dfs -cat file.dat
Hello world!
$ hdfs dfs -rm file.dat
Deleted file.dat
```

The hadoop web UI is available at `http://las0:9870`.

#### Safe mode

Show current safe mode status:

```console
$ hdfs dfsadmin -safemode get
Safe mode is OFF
```

Enter safe mode:

```console
$ hdfs dfsadmin -safemode enter
Safe mode is ON
```

Leave safe mode:

```console
$ hdfs dfsadmin -safemode leave
Safe mode is OFF
```

:::{note}
A freshly started/restarted NameNode is in safe mode temporarily. It will leave safe mode automatically.
:::

#### Clear all data

If you want to clear the hdfs data, stop hdfs and run the following commands on each node:

```console
$ rm -rf /opt/tmp/hadoop/dfs/*
```

### yarn

The yarn web UI is available at `http://las0:8088` or `http://las0:8088/ui2/`.
