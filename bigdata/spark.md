# spark

<https://spark.apache.org/>

:::{plat} centos
{{ cluster_las }}

Roles of the nodes:

:Master: las0
:Worker: las0, las1, las2
:::

## Prerequisites

Get shell script [`install_java_bin`](https://github.com/lasyard/coding/blob/main/shell/install_java_bin.sh).

Download the java binary packages:

```sh
wget https://mirrors.tuna.tsinghua.edu.cn/apache/spark/spark-3.5.4/spark-3.5.4-bin-hadoop3-scala2.13.tgz
```

Check sum:

```console
$ sha512sum spark-3.5.4-bin-hadoop3-scala2.13.tgz
9691435f42525a34d67564d397fed1a2380d27dcd5bfd309cd77eb8c26e6cc7a3fdfc4c8b8c501bb8740ee36dd8562b3c15e6bba7c75ea12899fbf5136442a91  spark-3.5.4-bin-hadoop3-scala2.13.tgz
```

## Deploy

Install packages on each node:

```sh
install_java_bin spark spark-3.5.4-bin-hadoop3-scala2.13.tgz /opt
```

### Configure

```sh
sudo cp /opt/spark/conf/workers.template /opt/spark/conf/workers
sudo vi /opt/spark/conf/workers
```

:::{literalinclude} /_files/centos/opt/spark/conf/workers
:diff: /_files/centos/opt/spark/conf/workers.orig
:class: file-content
:::

### Run

Start the Spark cluster on the Master node:

```sh
sudo /opt/spark/sbin/start-all.sh
```

:::{caution}
The `hadoop` distribution contains scripts with the same name `start-all.sh`. Do not run the wrong one.
:::

Show java processes:

:::{literalinclude} /_files/centos/console/jps/lm_spark.txt
:language: console
:::

Spark web UI is available at URL `http://las0:8080`.

:::{note}
Spark workers' web UI is binding to prot `8081`, which is conflicting with [Flink](project:flink.md).
:::

To stop the Spark cluster:

```sh
sudo /opt/spark/sbin/stop-all.sh
```

## Usage

```sh
spark-submit --master spark://las0:7077 --class org.apache.spark.examples.JavaSparkPi /opt/spark/examples/jars/spark-examples_2.13-3.5.4.jar
```

The output:

```console
Pi is roughly 3.1346
```

```sh
spark-submit --master spark://las0:7077 /opt/spark/examples/src/main/python/pi.py 10
```

The output:

```console
Pi is roughly 3.143440
```
