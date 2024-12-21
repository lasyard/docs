# hadoop

<https://hadoop.apache.org/>

:::{plat} centos
{{ cluster_las }}

Roles of nodes:

:NameNodes: las0
:DataNodes: las0, las1, las2
:ResourceManagers: las0
:NodeManagers: las0, las1, las2
:::

## Prerequisites

Install JDK on each node, see <project:/devel/java/install.md>.

Get shell scripts [`install_java_bin`](https://github.com/lasyard/coding/blob/main/shell/install_java_bin.sh).

Download the java binary packages:

```sh
wget https://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common/hadoop-3.4.1/hadoop-3.4.1.tar.gz
```

Check sum:

```console
$ sha512sum hadoop-3.4.1.tar.gz
09cda6943625bc8e4307deca7a4df76d676a51aca1b9a0171938b793521dfe1ab5970fdb9a490bab34c12a2230ffdaed2992bad16458169ac51b281be1ab6741  hadoop-3.4.1.tar.gz
```

:::{note}
Hadoop services are run as `root`, so pass free login to all nodes (include the node where the commands are emitted) should be set for `root`.
:::

## Deploy

Install the java packages on each node:

```sh
install_java_bin hadoop hadoop-3.4.1.tar.gz /opt
```

Set environment variables on each node:

```sh
echo "export HADOOP_HOME=\"/opt/hadoop\"" | sudo tee -a /etc/profile.d/hadoop.sh
echo "export HADOOP_CLASSPATH=\"\$(\${HADOOP_HOME}/bin/hadoop classpath)\"" | sudo tee -a /etc/profile.d/hadoop.sh
```

### Configure

```sh
sudo vi /opt/hadoop/etc/hadoop/hadoop-env.sh
```

:::{literalinclude} /_files/centos/opt/hadoop/etc/hadoop/hadoop-env.sh
:diff: /_files/centos/opt/hadoop/etc/hadoop/hadoop-env.sh.orig
:class: file-content
:::

```sh
sudo vi /opt/hadoop/etc/hadoop/core-site.xml
```

:::{literalinclude} /_files/centos/opt/hadoop/etc/hadoop/core-site.xml
:diff: /_files/centos/opt/hadoop/etc/hadoop/core-site.xml.orig
:class: file-content
:::

Create the directory of `${hadoop.tmp.dir}` on each node:

```sh
sudo mkdir -p /opt/tmp/hadoop
```

```sh
sudo vi /opt/hadoop/etc/hadoop/workers
```

:::{literalinclude} /_files/centos/opt/hadoop/etc/hadoop/workers
:diff: /_files/centos/opt/hadoop/etc/hadoop/workers.orig
:class: file-content
:::

#### Configure hdfs

```sh
sudo vi /opt/hadoop/etc/hadoop/hdfs-site.xml
```

:::{literalinclude} /_files/centos/opt/hadoop/etc/hadoop/hdfs-site.xml
:diff: /_files/centos/opt/hadoop/etc/hadoop/hdfs-site.xml.orig
:class: file-content
:::

#### Configure yarn

```sh
sudo vi /opt/hadoop/etc/hadoop/yarn-site.xml
```

:::{literalinclude} /_files/centos/opt/hadoop/etc/hadoop/yarn-site.xml
:diff: /_files/centos/opt/hadoop/etc/hadoop/yarn-site.xml.orig
:class: file-content
:::

```sh
sudo vi /opt/hadoop/etc/hadoop/mapred-site.xml
```

:::{literalinclude} /_files/centos/opt/hadoop/etc/hadoop/mapred-site.xml
:diff: /_files/centos/opt/hadoop/etc/hadoop/mapred-site.xml.orig
:class: file-content
:::

#### Distribute configuration files

Copy these files in directory `/opt/hadoop/etc/hadoop/` to the same path on all nodes:

- `hadoop-env.sh`
- `core-site.xml`
- `hdfs-site.xml`
- `mapred-site.xml`
- `yarn-site.xml`

### Run

Check the version:

:::{literalinclude} /_files/centos/console/hadoop/version.txt
:language: console
:::

Init hdfs:

```sh
sudo /opt/hadoop/bin/hdfs namenode -format
```

Start hdfs:

```sh
sudo /opt/hadoop/sbin/start-dfs.sh
```

Start yarn:

```sh
sudo /opt/hadoop/sbin/start-yarn.sh
```

Show java processes:

:::{literalinclude} /_files/centos/console/jps/lm_hdfs_yarn.txt
:language: console
:::

Stop them:

```sh
sudo /opt/hadoop/sbin/stop-yarn.sh
sudo /opt/hadoop/sbin/stop-dfs.sh
```

These commands are all executed on the NameNode/ResourceManager node.

## Usage

### hdfs

Suppose that the current user is `xxxx`.

```sh
hdfs dfs -ls /
sudo /opt/hadoop/bin/hdfs dfs -mkdir -p /user/xxxx
sudo /opt/hadoop/bin/hdfs dfs -chown xxxx /user/xxxx
hdfs dfs -put file.dat
hdfs dfs -cat file.dat
hdfs dfs -rm file.dat
```

The hadoop web UI is available at `http://las0:9870`.

#### Safe mode

Show current safe mode status:

```sh
hdfs dfsadmin -safemode get
```

Enter safe mode:

```sh
sudo /opt/hadoop/bin/hdfs dfsadmin -safemode enter
```

Leave safe mode:

```sh
sudo /opt/hadoop/bin/hdfs dfsadmin -safemode leave
```

:::{note}
A freshly started/restarted NameNode is in safe mode temporarily. It will leave safe mode automatically.
:::

#### Clear all data

If you want to clear the hdfs data, stop hdfs and run the following commands on each node:

```sh
sudo rm -rf /opt/tmp/hadoop/dfs/*
```

### yarn

The yarn web UI is available at `http://las0:8088` or `http://las0:8088/ui2/`.
