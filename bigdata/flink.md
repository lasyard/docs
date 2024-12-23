# flink

<https://flink.apache.org/>

:::{plat} centos
{{ cluster_las }}

Roles of nodes:

:JobManager: las0
:TaskManager: las0, las1, las2
:::

## Prerequisites

Get shell scripts [`install_java_bin`](https://github.com/lasyard/coding/blob/main/shell/install_java_bin.sh).

Download the java binary packages:

```sh
wget https://mirrors.tuna.tsinghua.edu.cn/apache/flink/flink-1.20.0/flink-1.20.0-bin-scala_2.12.tgz
```

Check sum:

```console
$ sha512sum flink-1.20.0-bin-scala_2.12.tgz
2af8c4d0329df8b139d8ad50ef9179bfed98907a9df7d4411b6e60ff60ca8105f81d07d8d2b7b904e214e68f10c9dfa3616274ca692a2b18de66f3541597a71d  flink-1.20.0-bin-scala_2.12.tgz
```

## Deploy

Install the java binary package on each node:

```sh
install_java_bin flink flink-1.20.0-bin-scala_2.12.tgz /opt
```

### Configure

```sh
sudo vi /opt/flink/conf/config.yaml
```

:::{literalinclude} /_files/centos/opt/flink/conf/config.yaml
:diff: /_files/centos/opt/flink/conf/config.yaml.orig
:class: file-content
:::

```sh
sudo vi /opt/flink/conf/masters
```

:::{literalinclude} /_files/centos/opt/flink/conf/masters
:diff: /_files/centos/opt/flink/conf/masters.orig
:class: file-content
:::

```sh
sudo vi /opt/flink/conf/workers
```

:::{literalinclude} /_files/centos/opt/flink/conf/workers
:diff: /_files/centos/opt/flink/conf/workers.orig
:class: file-content
:::

Create the directory of `${io.tmp.dirs}` on each node:

```sh
sudo mkdir -p /opt/tmp/flink
```

### Distribute configuration files

Copy these files in directory `/opt/flink/conf/` to all nodes:

- `config.yaml`
- `masters`
- `workers`

:::{important}
Edit `config.yaml` to set the config `taskmanager.host` to the hostname of each node respectively.
:::

### Start a standalone cluster

Check the version:

:::{literalinclude} /_files/centos/console/flink/version.txt
:language: console
:::

Run the following command on the node of JobManager to start the cluster:

```sh
sudo /opt/flink/bin/start-cluster.sh
```

See the java processes:

:::{literalinclude} /_files/centos/console/jps/lm_hdfs_flink.txt
:language: console
:::

Open `http://las0:8081/` in a web browser to see the Flink dashboard.

Stop the cluster:

```sh
sudo /opt/flink/bin/stop-cluster.sh
```

## Usage

### Batch expample

Create a text file:

```sh
vi words.txt
```

:::{literalinclude} /_files/centos/work/flink/words.txt
:language: text
:class: file-content
:::

Put the file into hdfs:

```sh
hdfs dfs -put -f words.txt
```

Submit a batch `WordCount` job:

```sh
flink run /opt/flink/examples/batch/WordCount.jar --input hdfs://las0:9000/user/xxxx/words.txt
```

The output (omit the warning messages):

:::{literalinclude} /_files/centos/console/flink/run_batch_word_count.txt
:language: text
:class: cli-output
:::

### Streaming example

Use the same `words.txt` file, submit a streaming `WordCount` job:

```sh
flink run /opt/flink/examples/streaming/WordCount.jar --input hdfs://las0:9000/user/xxxx/words.txt
```

The output will append to a `.out` file where the task is running. You can find the host on the Flink dashboard web UI. To monitor it:

```sh
tail -f /opt/flink/log/flink-root-taskexecutor-0-las0.out
```

:::{literalinclude} /_files/centos/console/flink/run_streaming_word_count.txt
:language: text
:class: cli-output
:::

## Run on yarn

Environment `HADOOP_CLASSPATH` needs to be set properly in order to run Flink on yarn.

To start a Flink yarn session:

```sh
yarn-session.sh --detached
```

Last lines of the output:

:::{literalinclude} /_files/centos/console/flink/yarn_session.txt
:language: text
:class: cli-output
:::

The last lines of the output expose the Flink dashboard URL and the commands to stop the cluster:

:::{note}
TaskManager will be allocated dynamically based on the running jobs.
:::

Now jobs can be submitted to the cluster.
