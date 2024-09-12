# flink

<https://flink.apache.org/>

Apache Flink is a framework and distributed processing engine for stateful computations over unbounded and bounded data streams. Flink has been designed to run in all common cluster environments, perform computations at in-memory speed and at any scale.

:::{plat} centos
{{ cluster_las }}

Roles of nodes:

:JobManager: las1
:TaskManager: las1, las2, las3
:::

## Prerequisites

Get shell scripts:

- [install_java_bin](https://github.com/lasyard/coding/blob/main/shell/install_java_bin.sh)

Download the java binary packages:

```sh
wget https://mirrors.tuna.tsinghua.edu.cn/apache/flink/flink-1.19.1/flink-1.19.1-bin-scala_2.12.tgz
```

Check sum:

```sh
sha512sum flink-1.19.1-bin-scala_2.12.tgz
```

{.cli-output}

```text
2be32fd038d078c9701f3557d0409b432a5d358749528a8f9113cec119972941b99b8dd375dd4e22e4895a8319b5409533209b3afd5fe73aeaa03566d76f0cc0  flink-1.19.1-bin-scala_2.12.tgz
```

## Deploy

Install the java binary package on each node:

```sh
install_java_bin flink flink-1.19.1-bin-scala_2.12.tgz /opt
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

```sh
flink --version
```

:::{literalinclude} /_files/centos/output/flink/version.txt
:language: text
:class: cli-output
:::

Run the following command on the node of JobManager to start the cluster:

```sh
sudo /opt/flink/bin/start-cluster.sh
```

:::{literalinclude} /_files/centos/output/flink/start_cluster.txt
:language: text
:class: cli-output
:::

See the java processes:

```sh
sudo jps -lm
```

:::{literalinclude} /_files/centos/output/jps/lm_flink.txt
:language: text
:class: cli-output
:::

Open `http://las1:8081/` in a web browser to see the Flink dashboard.

Stop the cluster:

```sh
sudo /opt/flink/bin/stop-cluster.sh
```

:::{literalinclude} /_files/centos/output/flink/stop_cluster.txt
:language: text
:class: cli-output
:::

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
flink run /opt/flink/examples/batch/WordCount.jar --input hdfs://las1:9000/user/xxxx/words.txt
```

The output (omit the warning messages):

:::{literalinclude} /_files/centos/output/flink/run_batch_word_count.txt
:language: text
:class: cli-output
:::

### Streaming example

Use the same `words.txt` file, submit a streaming `WordCount` job:

```sh
flink run /opt/flink/examples/streaming/WordCount.jar --input hdfs://las1:9000/user/xxxx/words.txt
```

The output will append to a `.out` file where the task is running. You can find the host on the Flink dashboard web UI. To monitor it:

```sh
tail -f /opt/flink/log/flink-root-taskexecutor-0-las1.out
```

:::{literalinclude} /_files/centos/output/flink/run_streaming_word_count.txt
:language: text
:class: cli-output
:::

## Run on yarn

Environment `HADOOP_CLASSPATH` needs to be set properly in order to run Flink on yarn.

To start a Flink yarn session:

```sh
yarn-session.sh --detached
```

The last lines of the output expose the Flink dashboard URL and the commands to stop the cluster:

:::{literalinclude} /_files/centos/output/flink/yarn_session.txt
:language: text
:class: cli-output
:::

:::{note}
TaskManager will be allocated dynamically based on the running jobs. The number of task slots is 0 for now.
:::

Now jobs can be submitted to the cluster.
