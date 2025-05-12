# spark

<https://spark.apache.org/>

## Prerequisites

Install JDK on each node, see "<project:/devel/java/install.md>".

Get shell script [`install_java_bin`](https://github.com/lasyard/coding/blob/main/shell/install_java_bin.sh).

Download the java binary packages:

```console
curl -LO https://mirrors.tuna.tsinghua.edu.cn/apache/spark/spark-3.5.4/spark-3.5.4-bin-hadoop3-scala2.13.tgz
```

Check sum:

```console
$ sha512sum spark-3.5.4-bin-hadoop3-scala2.13.tgz
9691435f42525a34d67564d397fed1a2380d27dcd5bfd309cd77eb8c26e6cc7a3fdfc4c8b8c501bb8740ee36dd8562b3c15e6bba7c75ea12899fbf5136442a91  spark-3.5.4-bin-hadoop3-scala2.13.tgz
```

## Deploy

Install packages on each node:

```console
$ install_java_bin spark spark-3.5.4-bin-hadoop3-scala2.13.tgz /opt
$ sudo chown ubuntu:ubuntu /opt/spark
```

### Configure

Copy file `/opt/spark/conf/workers.template` to `/opt/spark/conf/workers` and edit it:

:::{literalinclude} /_files/ubuntu/opt/spark/conf/workers
:diff: /_files/ubuntu/opt/spark/conf/workers.orig
:::

### Run

Start the Spark cluster on the Master node:

```console
$ /opt/spark/sbin/start-all.sh
starting org.apache.spark.deploy.master.Master, logging to /opt/spark/logs/spark-ubuntu-org.apache.spark.deploy.master.Master-1-las0.out
las2: starting org.apache.spark.deploy.worker.Worker, logging to /opt/spark/logs/spark-ubuntu-org.apache.spark.deploy.worker.Worker-1-las2.out
las1: starting org.apache.spark.deploy.worker.Worker, logging to /opt/spark/logs/spark-ubuntu-org.apache.spark.deploy.worker.Worker-1-las1.out
las0: starting org.apache.spark.deploy.worker.Worker, logging to /opt/spark/logs/spark-ubuntu-org.apache.spark.deploy.worker.Worker-1-las0.out
```

:::{caution}
The `hadoop` distribution contains scripts with the same name `start-all.sh`. Do not run the wrong one.
:::

Show java processes:

```console
$ jps -lm
3404602 org.apache.spark.deploy.master.Master --host las0 --port 7077 --webui-port 8080
3406925 sun.tools.jps.Jps -lm
3404796 org.apache.spark.deploy.worker.Worker --webui-port 8081 spark://las0:7077
```

Spark web UI is available at URL `http://las0:8080`.

:::{note}
Spark workers' web UI is binding to prot `8081`, which is conflicting with [Flink](project:flink.md).
:::

To stop the Spark cluster:

```console
$ /opt/spark/sbin/stop-all.sh
las0: stopping org.apache.spark.deploy.worker.Worker
las2: stopping org.apache.spark.deploy.worker.Worker
las1: stopping org.apache.spark.deploy.worker.Worker
stopping org.apache.spark.deploy.master.Master
```

## Usage

Submit java programs:

```console
$ spark-submit --master spark://las0:7077 --class org.apache.spark.examples.JavaSparkPi /opt/spark/examples/jars/spark-examples_2.13-3.5.4.jar
...
Pi is roughly 3.1409
...
```

Submit python programs:

```console
$ spark-submit --master spark://las0:7077 /opt/spark/examples/src/main/python/pi.py 10
...
Pi is roughly 3.133040
...
```
