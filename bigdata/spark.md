# spark

<https://spark.apache.org/>

Apache Spark™ is a multi-language engine for executing data engineering, data science, and machine learning on single-node machines or clusters.

{{ for_centos }}

{{ cluster_las }}

Roles of the nodes:

:Master: las1
:Worker: las1, las2, las3

## Prerequisites

Get shell scripts:

- [install_java_bin](https://github.com/lasyard/coding/blob/main/shell/install_java_bin.sh)

Download the java binary packages:

```sh
wget https://mirrors.tuna.tsinghua.edu.cn/apache/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3-scala2.13.tgz
```

Check sum:

```sh
sha512sum spark-3.5.1-bin-hadoop3-scala2.13.tgz
```

{.cli-output}

```text
225d2675a1fbde3f923bad4221e0d56dadeb43c8b13504c15efb16e433b681ad4a3b55d69d1d9ef9a7366862dfe6fe928b6114409cb0e662ccdf37c3676ae71e  spark-3.5.1-bin-hadoop3-scala2.13.tgz
```

## Deploy

Install packages on each node:

```sh
install_java_bin spark spark-3.5.1-bin-hadoop3-scala2.13.tgz /opt
```

### Configure

```sh
cp /opt/spark/conf/workers.template /opt/spark/conf/workers
vi /opt/spark/conf/workers
```

:::{literalinclude} /_files/common/etc/spark/workers
:diff: /_files/common/etc/spark/workers.orig
:class: file-content
:::

### Run

Start the Spark cluster on the Master node:

```sh
/opt/spark/sbin/start-all.sh
```

:::{caution}
The `hadoop` distribution contains scripts with the same name `start-all.sh`. Do not run the wrong one.
:::

See the java processes:

```sh
jps -lm
```

:::{literalinclude} /_files/common/output/jps/lm_spark.txt
:language: text
:class: cli-output
:::

Spark web UI is available at URL `http://las1:8080`.

:::{note}
Spark workers' web UI is binding to prot `8081`, which is conflicting with [Flink](project:flink.md).
:::

To stop the Spark cluster:

```sh
/opt/spark/sbin/stop-all.sh
```

## Usage

```sh
spark-submit --master spark://las1:7077 --class org.apache.spark.examples.JavaSparkPi /opt/spark/examples/jars/spark-examples_2.13-3.5.1.jar
```

```sh
spark-submit --master spark://las1:7077 /opt/spark/examples/src/main/python/pi.py 10
```
