# spark

<https://spark.apache.org/>

Apache Spark™ is a multi-language engine for executing data engineering, data science, and machine learning on single-node machines or clusters.

:::{plat} centos
{{ cluster_las }}

Roles of the nodes:

:Master: las1
:Worker: las1, las2, las3
:::

## Prerequisites

Get shell scripts:

- [install_java_bin](https://github.com/lasyard/coding/blob/main/shell/install_java_bin.sh)

Download the java binary packages:

```sh
wget https://mirrors.tuna.tsinghua.edu.cn/apache/spark/spark-3.5.2/spark-3.5.2-bin-hadoop3-scala2.13.tgz
```

Check sum:

```sh
sha512sum spark-3.5.2-bin-hadoop3-scala2.13.tgz
```

{.cli-output}

```text
90aa31c52a240155c9047a3d72748d569ca2109cf42abe359709e3212337456f327046e0c1849a29e0f731c0aee1f2a14e0a37739851a79a18e8aa7be125c0af  spark-3.5.2-bin-hadoop3-scala2.13.tgz
```

## Deploy

Install packages on each node:

```sh
install_java_bin spark spark-3.5.2-bin-hadoop3-scala2.13.tgz /opt
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

:::{literalinclude} /_files/centos/output/spark/start_all.txt
:language: text
:class: cli-output
:::

:::{caution}
The `hadoop` distribution contains scripts with the same name `start-all.sh`. Do not run the wrong one.
:::

See the java processes:

```sh
sudo jps -lm
```

:::{literalinclude} /_files/centos/output/jps/lm_spark.txt
:language: text
:class: cli-output
:::

Spark web UI is available at URL `http://las1:8080`.

:::{note}
Spark workers' web UI is binding to prot `8081`, which is conflicting with [Flink](project:flink.md).
:::

To stop the Spark cluster:

```sh
sudo /opt/spark/sbin/stop-all.sh
```

:::{literalinclude} /_files/centos/output/spark/stop_all.txt
:language: text
:class: cli-output
:::

## Usage

```sh
spark-submit --master spark://las1:7077 --class org.apache.spark.examples.JavaSparkPi /opt/spark/examples/jars/spark-examples_2.13-3.5.2.jar
```

```sh
spark-submit --master spark://las1:7077 /opt/spark/examples/src/main/python/pi.py 10
```
