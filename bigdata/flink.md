# flink

<https://flink.apache.org/>

## Prerequisites

Install JDK on each node, see "<project:/devel/java/install.md>".

Get shell script [`install_java_bin`](https://github.com/lasyard/coding/blob/main/shell/install_java_bin.sh).

Download the java binary packages:

```console
$ curl -LO https://mirrors.tuna.tsinghua.edu.cn/apache/flink/flink-1.20.0/flink-1.20.0-bin-scala_2.12.tgz
```

Check sum:

```console
$ sha512sum flink-1.20.0-bin-scala_2.12.tgz
2af8c4d0329df8b139d8ad50ef9179bfed98907a9df7d4411b6e60ff60ca8105f81d07d8d2b7b904e214e68f10c9dfa3616274ca692a2b18de66f3541597a71d  flink-1.20.0-bin-scala_2.12.tgz
```

## Deploy

Install the java binary package on each node:

```console
$ install_java_bin flink flink-1.20.0-bin-scala_2.12.tgz /opt
$ sudo chown ubuntu:ubuntu /opt/flink/log
```

### Configure

Edit file `/opt/flink/conf/config.yaml`:

:::{literalinclude} /_files/ubuntu/opt/flink/conf/config.yaml
:diff: /_files/ubuntu/opt/flink/conf/config.yaml.orig
:::

Edit file `/opt/flink/conf/masters`:

:::{literalinclude} /_files/ubuntu/opt/flink/conf/masters
:diff: /_files/ubuntu/opt/flink/conf/masters.orig
:::

Edit file `/opt/flink/conf/workers`:

:::{literalinclude} /_files/ubuntu/opt/flink/conf/workers
:diff: /_files/ubuntu/opt/flink/conf/workers.orig
:::

These files need to be copied to all nodes to the same path.

:::{important}
Edit file `/opt/flink/conf/config.yaml` to set the config `taskmanager.host` to the hostname of each node respectively.
:::

Create the directory of `${io.tmp.dirs}` on each node:

```console
$ sudo mkdir -p /opt/tmp/flink
$ sudo chown ubuntu:ubuntu /opt/tmp/flink
```

### Start a standalone cluster

Check the version:

```console
$ flink --version
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/opt/flink-1.20.0/lib/log4j-slf4j-impl-2.17.1.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/opt/hadoop-3.4.1/share/hadoop/common/lib/slf4j-reload4j-1.7.36.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.apache.logging.slf4j.Log4jLoggerFactory]
Version: 1.20.0, Commit ID: b1fe7b4
```

Run the following command on the node of JobManager to start the cluster:

```console
$ start-cluster.sh 
Starting cluster.
Starting standalonesession daemon on host k8ctl.
Starting taskexecutor daemon on host k8ctl.
Starting taskexecutor daemon on host k8cpu0.
Starting taskexecutor daemon on host k8cpu1.
```

Show java processes:

```console
$ jps -lm
3365748 org.apache.flink.runtime.taskexecutor.TaskManagerRunner --configDir /opt/flink-1.20.0/conf -D taskmanager.memory.network.min=134217730b -D taskmanager.cpu.cores=8.0 -D taskmanager.memory.task.off-heap.size=0b -D taskmanager.memory.jvm-metaspace.size=268435456b -D external-resources=none -D taskmanager.memory.jvm-overhead.min=201326592b -D taskmanager.memory.framework.off-heap.size=134217728b -D taskmanager.memory.network.max=134217730b -D taskmanager.memory.framework.heap.size=134217728b -D taskmanager.memory.managed.size=536870920b -D taskmanager.memory.task.heap.size=402653174b -D taskmanager.numberOfTaskSlots=8 -D taskmanager.memory.jvm-overhead.max=201326592b
3366233 sun.tools.jps.Jps -lm
3364936 org.apache.flink.runtime.entrypoint.StandaloneSessionClusterEntrypoint -D jobmanager.memory.off-heap.size=134217728b -D jobmanager.memory.jvm-overhead.min=201326592b -D jobmanager.memory.jvm-metaspace.size=268435456b -D jobmanager.memory.heap.size=1073741824b -D jobmanager.memory.jvm-overhead.max=201326592b --configDir /opt/flink-1.20.0/conf --executionMode cluster
```

Open `http://las0:8081/` in a web browser to see the Flink dashboard.

Stop the cluster:

```console
$ stop-cluster.sh 
Stopping taskexecutor daemon (pid: 3365748) on host k8ctl.
Stopping taskexecutor daemon (pid: 2304551) on host k8cpu0.
Stopping taskexecutor daemon (pid: 2204138) on host k8cpu1.
Stopping standalonesession daemon (pid: 3364936) on host k8ctl.
```

## Usage

### Batch expample

Create a text file `words.txt`:

:::{literalinclude} /_files/ubuntu/workspace/words.txt
:language: text
:::

Put the file into hdfs:

```console
$ hdfs dfs -put -f words.txt
```

Submit a batch `WordCount` job:

```console
$ flink run /opt/flink/examples/batch/WordCount.jar --input hdfs://las0:9000/user/ubuntu/words.txt
...
Printing result to stdout. Use --output to specify output path.
Job has been submitted with JobID 0850ca7989a26058d20f4dc987d546ae
Program execution finished
Job with JobID 0850ca7989a26058d20f4dc987d546ae has finished.
Job Runtime: 3010 ms
Accumulator Results: 
- c79afe69fc305f3b31d5a614cd556b18 (java.util.ArrayList) [5 elements]


(alice,3)
(betty,2)
(cindy,1)
(doris,2)
(emily,2)
```

### Streaming example

Use the same `words.txt` file, submit a streaming `WordCount` job:

```console
$ flink run /opt/flink/examples/streaming/WordCount.jar --input hdfs://las0:9000/user/ubuntu/words.txt
...
Printing result to stdout. Use --output to specify output path.
Job has been submitted with JobID e7d0225697a0af2cb47db7b5866a43c4
Program execution finished
Job with JobID e7d0225697a0af2cb47db7b5866a43c4 has finished.
Job Runtime: 518 ms
```

The output will append to a `.out` file where the task is running. You can find the host on the Flink dashboard web UI. To monitor it:

```console
$ tail -f flink-ubuntu-taskexecutor-0-k8ctl.out
(alice,1)
(betty,1)
(alice,2)
(cindy,1)
(doris,1)
(betty,2)
(emily,1)
(alice,3)
(emily,2)
(doris,2)
```

## Run on yarn

Environment `HADOOP_CLASSPATH` needs to be set properly in order to run Flink on yarn.

To start a Flink yarn session:

```console
$ yarn-session.sh --detached
...
JobManager Web Interface: http://las2:36373
...
```

The last lines of the output expose the Flink dashboard URL and the commands to stop the cluster.

:::{note}
TaskManager will be allocated dynamically based on the running jobs.
:::

Now jobs can be submitted to the cluster.
