# hadoop

<https://hadoop.apache.org/>

The Apache Hadoop software library is a framework that allows for the distributed processing of large data sets across clusters of computers using simple programming models.

{{ for_centos }}

{{ cluster_las }}

Roles of nodes:

:NameNodes: las1
:DataNodes: las1, las2, las3
:ResourceManagers: las1
:NodeManagers: las1, las2, las3

## Prerequisites

Get shell scripts:

- [install_java_bin](https://github.com/lasyard/coding/blob/main/shell/install_java_bin.sh)

Download the java packages:

```sh
wget https://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
```

Check sum:

```sh
sha512sum hadoop-3.3.6.tar.gz
```

{.cli-output}

```text
de3eaca2e0517e4b569a88b63c89fae19cb8ac6c01ff990f1ff8f0cc0f3128c8e8a23db01577ca562a0e0bb1b4a3889f8c74384e609cd55e537aada3dcaa9f8a  hadoop-3.3.6.tar.gz
```

## Deploy

Install the java packages on each node:

```sh
install_java_bin hadoop hadoop-3.3.6.tar.gz /opt
```

### Configure

```sh
vi /opt/hadoop/etc/hadoop/hadoop-env.sh
```

:::{literalinclude} /_files/common/etc/hadoop/hadoop-env.sh
:diff: /_files/common/etc/hadoop/hadoop-env.sh.orig
:class: file-content
:::

```sh
vi /opt/hadoop/etc/hadoop/core-site.xml
```

:::{literalinclude} /_files/common/etc/hadoop/core-site.xml
:diff: /_files/common/etc/hadoop/core-site.xml.orig
:class: file-content
:::

Make directory for `${hadoop.tmp.dir}`:

```sh
mkdir -p /opt/tmp/hadoop
```

Set environment variables:

```sh
echo "export HADOOP_HOME=\"/opt/hadoop\"" | tee -a /etc/profile.d/hadoop.sh
echo "export HADOOP_CLASSPATH=\"\$(\${HADOOP_HOME}/bin/hadoop classpath)\"" | tee -a /etc/profile.d/hadoop.sh
```

```sh
vi /opt/hadoop/etc/hadoop/workers
```

:::{literalinclude} /_files/common/etc/hadoop/workers
:diff: /_files/common/etc/hadoop/workers.orig
:class: file-content
:::

#### Configure hdfs

```sh
vi /opt/hadoop/etc/hadoop/hdfs-site.xml
```

:::{literalinclude} /_files/common/etc/hadoop/hdfs-site.xml
:diff: /_files/common/etc/hadoop/hdfs-site.xml.orig
:class: file-content
:::

#### Configure yarn

```sh
vi /opt/hadoop/etc/hadoop/yarn-site.xml
```

:::{literalinclude} /_files/common/etc/hadoop/yarn-site.xml
:diff: /_files/common/etc/hadoop/yarn-site.xml.orig
:class: file-content
:::

```sh
vi /opt/hadoop/etc/hadoop/mapred-site.xml
```

:::{literalinclude} /_files/common/etc/hadoop/mapred-site.xml
:diff: /_files/common/etc/hadoop/mapred-site.xml.orig
:class: file-content
:::

#### Distribute configuration files

Copy these files to all nodes:

- `hadoop-env.sh`
- `core-site.xml`
- `hdfs-site.xml`
- `mapred-site.xml`
- `yarn-site.xml`

### Run

Check version:

```sh
hadoop version
```

:::{literalinclude} /_files/common/output/hadoop/version.txt
:language: text
:class: cli-output
:::

Init hdfs:

```sh
hdfs namenode -format
```

Start hdfs:

```sh
start-dfs.sh
```

Start yarn:

```sh
start-yarn.sh
```

Show java processes:

```sh
jps -lm
```

:::{literalinclude} /_files/common/output/jps/lm_hdfs_yarn.txt
:language: text
:class: cli-output
:::

Stop them:

```sh
stop-yarn.sh
stop-dfs.sh
```

These commands are all executed on the NameNode/ResourceManager node.

## Usage

### hdfs

```sh
hdfs dfs -ls /
hdfs dfs -mkdir -p /user/root
hdfs dfs -put file.dat
hdfs dfs -cat /user/root/file.dat
hdfs dfs -rm file.dat
```

The hadoop web UI is available at `http://las1:9870`.

### Clear hdfs data

If you want to clear the hdfs data, stop hdfs and run the following commands on each node:

```sh
rm -rf /opt/tmp/hadoop/dfs/*
```

### yarn

The yarn web UI is available at `http://las1:8088` or `http://las1:8088/ui2/`.
