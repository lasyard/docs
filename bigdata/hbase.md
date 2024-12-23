# hbase

<https://hbase.apache.org/>

:::{plat} centos
{{ cluster_las }}

Roles of the nodes:

:Master: las0
:RegionServer: las0, las1, las2
:::

## Prerequisites

Get shell scripts [`install_java_bin`](https://github.com/lasyard/coding/blob/main/shell/install_java_bin.sh).

Download the java binary packages:

```sh
wget https://mirrors.tuna.tsinghua.edu.cn/apache/hbase/2.6.1/hbase-2.6.1-hadoop3-bin.tar.gz
```

Check sum:

```console
$ sha512sum hbase-2.6.1-hadoop3-bin.tar.gz
160d7a79cb21c92101d8e74647477200b541b93d5e75f09648e3a601921119d13f8387beb9f63a9228e67630959227b9ef665d9ac7cbe03e570b7fc4fe1fbfdc  hbase-2.6.1-hadoop3-bin.tar.gz
```

Install [hadoop](project:hadoop.md) and [zookeeper](project:zookeeper.md) first.

## Deploy

Install the java packages on each node:

```sh
install_java_bin hbase hbase-2.6.1-hadoop3-bin.tar.gz /opt
```

### Configure

```sh
sudo vi /opt/hbase/conf/hbase-env.sh
```

:::{literalinclude} /_files/centos/opt/hbase/conf/hbase-env.sh
:diff: /_files/centos/opt/hbase/conf/hbase-env.sh.orig
:class: file-content
:::

```sh
sudo vi /opt/hbase/conf/hbase-site.xml
```

:::{literalinclude} /_files/centos/opt/hbase/conf/hbase-site.xml
:diff: /_files/centos/opt/hbase/conf/hbase-site.xml.orig
:class: file-content
:::

```sh
sudo vi /opt/hbase/conf/regionservers
```

:::{literalinclude} /_files/centos/opt/hbase/conf/regionservers
:diff: /_files/centos/opt/hbase/conf/regionservers.orig
:class: file-content
:::

Create the directory of `${hbase.tmp.dir}` on each node:

```sh
sudo mkdir -p /opt/tmp/hbase
```

### Distribute configuration files

Copy these files in direcotry `/opt/hbase/conf/` to all nodes:

- `hbase-env.sh`
- `hbase-site.xml`

### Run

```sh
hbase version
```

:::{literalinclude} /_files/centos/console/hbase/version.txt
:language: console
:::

Start hdfs & zookeeper first.

Start hbase:

```sh
sudo /opt/hbase/bin/start-hbase.sh
```

Show java processes:

:::{literalinclude} /_files/centos/console/jps/lm_hdfs_zookeeper_hbase.txt
:language: console
:::

Stop hbase:

```sh
sudo /opt/hbase/bin/stop-hbase.sh
```

:::{tip}
If the command above does not work, try these commands:

```sh
sudo /opt/hbase/bin/hbase-daemon.sh stop master
sudo /opt/hbase/bin/hbase-daemon.sh stop regionserver
```

to stop the master and each region server one by one.
:::

## Usage

```sh
hbase shell
```

In hbase shell:

```sql
help
quit
```

Open the web UI at `http://las0:16010/`.
