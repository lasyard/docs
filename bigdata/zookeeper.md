# zookeeper

<https://zookeeper.apache.org/>

ZooKeeper is a centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services.

{{ for_centos }}

{{ cluster_las }}

## Prerequisites

Get shell scripts:

- [install_java_bin](https://github.com/lasyard/coding/blob/main/shell/install_java_bin.sh)

Download the java binary packages:

```sh
wget https://mirrors.tuna.tsinghua.edu.cn/apache/zookeeper/zookeeper-3.8.4/apache-zookeeper-3.8.4-bin.tar.gz
```

Check sum:

```sh
sha512sum apache-zookeeper-3.8.4-bin.tar.gz
```

{.cli-output}

```text
4d85d6f7644d5f36d9c4d65e78bd662ab35ebe1380d762c24c12b98af029027eee453437c9245dbdf2b9beb77cd6b690b69e26f91cf9d11b0a183a979c73fa43  apache-zookeeper-3.8.4-bin.tar.gz
```

## Deploy

Install the java packages on each node:

```sh
install_java_bin zookeeper apache-zookeeper-3.8.4-bin.tar.gz /opt
```

### Configure

```sh
cp /opt/zookeeper/conf/zoo_sample.cfg /opt/zookeeper/conf/zoo.cfg
vi /opt/zookeeper/conf/zoo.cfg
```

:::{literalinclude} /_files/common/etc/zookeeper/zoo.cfg
:diff: /_files/common/etc/zookeeper/zoo.cfg.orig
:class: file-content
:::

Create the directory of `${dataDir}` on each node:

```sh
mkdir -p /opt/tmp/zookeeper
```

### Distribute configuration files

Copy `zoo.cfg` to all nodes:

```sh
scp /opt/zookeeper/conf/zoo.cfg las2:/opt/zookeeper/conf
scp /opt/zookeeper/conf/zoo.cfg las3:/opt/zookeeper/conf
```

Create `myid` file for each node:

```sh
for i in {1..3}; do
    ssh las${i} "echo ${i} | tee /opt/tmp/zookeeper/myid"
done
```

### Run

Check version:

```sh
zkServer.sh version
```

:::{literalinclude} /_files/common/output/zkServer/version.txt
:language: text
:class: cli-output
:::

Start service on each node:

```sh
for host in las1 las2 las3; do
    ssh ${host} "/opt/zookeeper/bin/zkServer.sh start"
done
```

```sh
jps -lm
```

:::{literalinclude} /_files/common/output/jps/lm_zookeeper.txt
:language: text
:class: cli-output
:::

Check service status:

```sh
zkServer.sh status
```

:::{literalinclude} /_files/common/output/zkServer/status.txt
:language: text
:class: cli-output
:::

:::{note}
Only one of the nodes should be 'leader' and the others should be 'follower'.
:::

Stop service on each node:

```sh
for host in las1 las2 las3; do
    ssh "${host}" "/opt/zookeeper/bin/zkServer.sh stop"
done
```

## Usage

```sh
zkCli.sh -server las1
```

The admin service is started on port 8080 on each node by default. Open `http://las1:8080/commands` to see the list of available commands.
