# zookeeper

<https://zookeeper.apache.org/>

:::{plat} centos
{{ cluster_las }}
:::

## Prerequisites

Install JDK on each node, see <project:/devel/java/install.md>.

Get shell scripts [`install_java_bin`](https://github.com/lasyard/coding/blob/main/shell/install_java_bin.sh).

Download the java binary packages:

```sh
wget https://mirrors.tuna.tsinghua.edu.cn/apache/zookeeper/zookeeper-3.9.3/apache-zookeeper-3.9.3-bin.tar.gz
```

Check sum:

```console
$ sha512sum apache-zookeeper-3.9.3-bin.tar.gz 
d44d870c1691662efbf1a8baf1859c901b820dc5ff163b36e81beb27b6fbf3cd31b5f1f075697edaaf6d3e7a4cb0cc92f924dcff64b294ef13d535589bdaf143  apache-zookeeper-3.9.3-bin.tar.gz
```

## Deploy

Install the java packages on each node:

```sh
install_java_bin zookeeper apache-zookeeper-3.9.3-bin.tar.gz /opt
```

### Configure

```sh
sudo cp /opt/zookeeper/conf/zoo_sample.cfg /opt/zookeeper/conf/zoo.cfg
sudo vi /opt/zookeeper/conf/zoo.cfg
```

:::{literalinclude} /_files/centos/opt/zookeeper/conf/zoo.cfg
:diff: /_files/centos/opt/zookeeper/conf/zoo.cfg.orig
:class: file-content
:::

Create the directory of `${dataDir}` on each node:

```sh
sudo mkdir -p /opt/tmp/zookeeper
```

### Distribute configuration files

Copy `zoo.cfg` in directory `/opt/zookeeper/conf/` to the same path on all nodes.

Create a `myid` file whose content is an unique id number in directory `/opt/tmp/zookeeper` for each node.

For example, on `las1`:

```sh
echo 1 | sudo tee /opt/tmp/zookeeper/myid
```

### Run

Check version:

:::{literalinclude} /_files/centos/console/zkserver/version.txt
:language: console
:::

Start service on each node:

```sh
sudo /opt/zookeeper/bin/zkServer.sh start
```

Show java processes:

:::{literalinclude} /_files/centos/console/jps/lm_zookeeper.txt
:language: console
:::

Check service status:

```sh
zkServer.sh status
```

:::{literalinclude} /_files/centos/console/zkserver/status.txt
:language: console
:::

:::{note}
Only one of the nodes should be 'leader' and the others should be 'follower'.
:::

Stop service on one node:

```sh
sudo /opt/zookeeper/bin/zkServer.sh stop
```

There must be at least 3 nodes to make `zookeeper` functions properly.

## Usage

```sh
zkCli.sh -server las0
```

The admin service is started on port 8080 on each node by default. Open `http://las0:8080/commands` to see the list of available commands.
