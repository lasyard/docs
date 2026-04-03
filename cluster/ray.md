# Ray

## Install

Install ray on each node:

```console
$ sudo pip install -U "ray[default]"
```

## Run

### Mannually

Start a head node:

```console
$ ray start --head --port=6379 --dashboard-host=0.0.0.0
Enable usage stats collection? This prompt will auto-proceed in 10 seconds to avoid blocking cluster startup. Confirm [Y/n]: 
Usage stats collection is enabled. To disable this, add `--disable-usage-stats` to the command that starts the cluster, or run the following command: `ray disable-usage-stats` before starting the cluster. See https://docs.ray.io/en/master/cluster/usage-stats.html for more details.

Local node IP: 10.225.4.51

--------------------
Ray runtime started.
--------------------

Next steps
  To add another node to this Ray cluster, run
    ray start --address='10.225.4.51:6379'
  
  To connect to this Ray cluster:
    import ray
    ray.init()
  
  To submit a Ray job using the Ray Jobs CLI:
    RAY_API_SERVER_ADDRESS='http://10.225.4.51:8265' ray job submit --working-dir . -- python my_script.py
  
  See https://docs.ray.io/en/latest/cluster/running-applications/job-submission/index.html 
  for more information on submitting Ray jobs to the Ray cluster.
  
  To terminate the Ray runtime, run
    ray stop
  
  To view the status of the cluster, use
    ray status
  
  To monitor and debug Ray, view the dashboard at 
    10.225.4.51:8265
  
  If connection to the dashboard fails, check your firewall settings and network configuration.
```

Start Worker nodes:

```console
$ ray start --address='10.225.4.51:6379'
Local node IP: 10.225.4.53

--------------------
Ray runtime started.
--------------------

To terminate the Ray runtime, run
  ray stop
```

Check ray cluster status:

```console
======== Autoscaler status: 2026-04-03 15:16:01.279233 ========
Node status
---------------------------------------------------------------
Active:
 1 node_bae165fb38933adb4299b4c856363101c36aa14a2953eeeba83737e7
 1 node_40a4218cfae734c57821c51ee9927a9d8f3a922840fe4e8b76157a15
 1 node_196edc38eeb48c518cb064395c84b7af2a5e56ce723b51be4342d368
 1 node_d394e88293678c958f1eea4d97dceb93f7dbb6ab6118be74d243df6a
Pending:
 (no pending nodes)
Recent failures:
 (no failures)

Resources
---------------------------------------------------------------
Total Usage:
 0.0/64.0 CPU
 0B/79.43GiB memory
 0B/34.04GiB object_store_memory

From request_resources:
 (none)
Pending Demands:
 (no resource demands)
```

Show all nodes:

```console
$ ray list nodes

======== List: 2026-04-03 15:19:40.524765 ========
Stats:
------------------------------
Total: 4

Table:
------------------------------
...
```

Stop ray on the head node:

```console
$ ray stop
Stopped all 6 Ray processes.
```

Stop a worker:

```console
$ ray stop
Stopped all 2 Ray processes.
```

:::{note}
Must stop workers first before stopping the head.
:::

### Using config file

A more practical way is using a cluster config file, like this:

:::{literalinclude} /_files/ubuntu/workspace/ray/ray-cluster.yaml
:::

Then bootstrap a ray cluster up:

```console
$ ray up ray-cluster.yaml
Cluster: las

Checking Local environment settings
2026-04-03 17:10:58,735 INFO node_provider.py:53 -- ClusterState: Loaded cluster state: ['10.225.4.52', '10.225.4.53', '10.225.4.54', '10.225.4.51']
No head node found. Launching a new cluster. Confirm [y/N]: y
...
Useful commands:
  To terminate the cluster:
    ray down /home/ubuntu/workspace/ray-cluster.yaml
  
  To retrieve the IP address of the cluster head:
    ray get-head-ip /home/ubuntu/workspace/ray-cluster.yaml
  
  To port-forward the cluster's Ray Dashboard to the local machine:
    ray dashboard /home/ubuntu/workspace/ray-cluster.yaml
  
  To submit a job to the cluster, port-forward the Ray Dashboard in another terminal and run:
    ray job submit --address http://localhost:<dashboard-port> --working-dir . -- python my_script.py
  
  To connect to a terminal on the cluster head for debugging:
    ray attach /home/ubuntu/workspace/ray-cluster.yaml
  
  To monitor autoscaling:
    ray exec /home/ubuntu/workspace/ray-cluster.yaml 'tail -n 100 -f /tmp/ray/session_latest/logs/monitor*'

```

Check status:

```console
$ ray status
======== Autoscaler status: 2026-04-03 17:12:01.809482 ========
Node status
---------------------------------------------------------------
Active:
 (no active nodes)
Idle:
 3 local.cluster.node
Pending:
 (no pending nodes)
Recent failures:
 (no failures)

Resources
---------------------------------------------------------------
Total Usage:
 0.0/48.0 CPU
 0B/59.14GiB memory
 0B/25.34GiB object_store_memory

From request_resources:
 (none)
Pending Demands:
 (no resource demands)
```

:::{important}
There is a `max_workers` config, which is default to the number of `worker_ips` (and cannot be set to a larger number), and a worker is run on the head node, so there is always a host left without any worker running on. Don't know why it is designed.
:::

Teardown the cluster:

```console
$ ray down ray-cluster.yaml 
Loaded cached provider configuration
If you experience issues with the cloud provider, try re-running the command with --no-config-cache.
Destroying cluster. Confirm [y/N]: y
...
Requested 3 nodes to shut down. [interval=1s]
0 nodes remaining after 5 second(s).
No nodes remaining.
```

## Usage

### Run a command

If you are on a node of ray cluster (head or worker), you can run ray app directly by:

```console
$ python count_hosts.py
This cluster consists of
    3 nodes in total
    48.0 CPU resources in total

Tasks executed
    20 tasks on las0
    14 tasks on las1
    14 tasks on las2
```

The source code of `count_hosts.py` is public on [GitHub](https://github.com/lasyard/coding/blob/main/python/ray/count_hosts.py).

### Submit a job

Or you can run it by sumbit a job:

```console
$ ray job submit --working-dir . -- python count_hosts.py
Job submission server address: http://10.225.4.51:8265
2026-04-03 18:42:22,308 INFO dashboard_sdk.py:359 -- Uploading package gcs://_ray_pkg_1cd54066d1e984c7.zip.
2026-04-03 18:42:22,309 INFO packaging.py:691 -- Creating a file package for local module '.'.

-------------------------------------------------------
Job 'raysubmit_62j7dPtmX6UfzDnx' submitted successfully
-------------------------------------------------------

Next steps
  Query the logs of the job:
    ray job logs raysubmit_62j7dPtmX6UfzDnx
  Query the status of the job:
    ray job status raysubmit_62j7dPtmX6UfzDnx
  Request the job to be stopped:
    ray job stop raysubmit_62j7dPtmX6UfzDnx

Tailing logs until the job exits (disable with --no-wait):
2026-04-03 18:42:22,328 INFO job_manager.py:587 -- Runtime env is setting up.
Running entrypoint for job raysubmit_62j7dPtmX6UfzDnx: python count_hosts.py
2026-04-03 18:42:24,001 INFO worker.py:1669 -- Using address 10.225.4.51:6379 set in the environment variable RAY_ADDRESS
2026-04-03 18:42:24,009 INFO worker.py:1810 -- Connecting to existing Ray cluster at address: 10.225.4.51:6379...
2026-04-03 18:42:24,084 INFO worker.py:2004 -- Connected to Ray cluster. View the dashboard at 10.225.4.51:8265 
This cluster consists of
    3 nodes in total
    48.0 CPU resources in total

Tasks executed
    19 tasks on las1
    19 tasks on las0
    10 tasks on las2

------------------------------------------
Job 'raysubmit_62j7dPtmX6UfzDnx' succeeded
------------------------------------------

```

:::{note}
In this way, the files under the working directory is packaged and uploaded. So don't put irrelevant files in it.
:::

Submit a job asynchronously:

```console
$ ray job submit --no-wait --working-dir . -- python count_hosts.py
Job submission server address: http://10.225.4.51:8265
2026-04-03 18:43:05,441 INFO dashboard_sdk.py:411 -- Package gcs://_ray_pkg_1cd54066d1e984c7.zip already exists, skipping upload.
...
```

The package is now cached, so it will not being uploaded again.

### Job management

List all jobs:

```console
$ ray list jobs

======== List: 2026-04-03 18:56:24.144025 ========
Stats:
------------------------------
Total: 2

Table:
------------------------------
      JOB_ID  SUBMISSION_ID               ENTRYPOINT              TYPE        STATUS     MESSAGE                     ERROR_TYPE    DRIVER_INFO
 0  01000000                              python count_hosts.py   DRIVER      SUCCEEDED                                            id: '01000000'
                                                                                                                                   node_ip_address: 10.225.4.51
                                                                                                                                   pid: '1139146'
 1  03000000  raysubmit_2npNAssCnHczsCpv  python count_hosts.py   SUBMISSION  SUCCEEDED  Job finished successfully.                id: '03000000'
                                                                                                                                   node_ip_address: 10.225.4.51
                                                                                                                                   pid: '1140228'

```

Delete a job:

```console
$ ray job delete 03000000
Job submission server address: http://10.225.4.51:8265
Job '03000000' deleted successfully
```

If the job is in `RUNNING` status, you need to stop it first:

```console
$ ray job stop 04000000
Job submission server address: http://10.225.4.51:8265
Attempting to stop job '04000000'
Waiting for job '04000000' to exit (disable with --no-wait):
Job has not exited yet. Status: RUNNING
Job has not exited yet. Status: RUNNING
Job has not exited yet. Status: RUNNING
Job '04000000' was stopped
```
