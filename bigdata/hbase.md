# hbase

<https://hbase.apache.org/>

Use Apache HBase® when you need random, realtime read/write access to your Big Data. This project's goal is the hosting of very large tables -- billions of rows X millions of columns -- atop clusters of commodity hardware.

:::{plat} centos
{{ cluster_las }}

Roles of the nodes:

:Master: las1
:RegionServer: las1, las2, las3
:::

## Prerequisites

Get shell scripts:

- [install_java_bin](https://github.com/lasyard/coding/blob/main/shell/install_java_bin.sh)

Download the java binary packages:

```sh
wget https://mirrors.tuna.tsinghua.edu.cn/apache/hbase/2.5.8/hbase-2.5.8-hadoop3-bin.tar.gz
```

Check sum:

```sh
sha512sum hbase-2.5.8-hadoop3-bin.tar.gz
```

{.cli-output}

```text
6b61b264310e9854d1cf47cb91a149a82643ad2400a96351e4a73c329e140b18bb728282d7b9855c3f25215c6357924265909f85f39a634070c0d092b678516b  hbase-2.5.8-hadoop3-bin.tar.gz
```

Install [hadoop](project:hadoop.md) and [zookeeper](project:zookeeper.md) first.

## Deploy

Install the java packages on each node:

```sh
install_java_bin hbase hbase-2.5.8-hadoop3-bin.tar.gz /opt
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

:::{literalinclude} /_files/centos/output/hbase/version.txt
:language: text
:class: cli-output
:::

Start hdfs & zookeeper first.

Start hbase:

```sh
sudo /opt/hbase/bin/start-hbase.sh
```

```sh
sudo jps -lm
```

:::{literalinclude} /_files/centos/output/jps/lm_hdfs_zookeeper_hbase.txt
:language: text
:class: cli-output
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

Open the web UI at `http://las1:16010/`.
