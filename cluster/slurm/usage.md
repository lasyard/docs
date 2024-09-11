# Slurm Usage

## sinfo

Watch the status of cluster at an interval of 5 seconds:

```sh
sinfo -i 5
```

Node-centric format:

```sh
sinfo -N
```

:::{literalinclude} /_files/centos/output/sinfo/n.txt
:language: text
:class: cli-output
:::

```sh
sinfo -o "%20N %10c %10m %25f %G"
```

:::{literalinclude} /_files/centos/output/sinfo/o.txt
:language: text
:class: cli-output
:::

List the reasons nodes are down or drained:

```sh
sinfo -R
```

:::{literalinclude} /_files/centos/output/sinfo/r.txt
:language: text
:class: cli-output
:::

The outputs above were gotten quite a while after the `slurmd` service is shutdown on node `las3`.

## srun

```sh
# Specify number of CPUs
srun -c 8 sleep
# Run on specified node
srun -w host2 sleep 5
# Specify the number of Nodes
srun -N 3 hostname
# Specify the begin time of job
srun -b now+100 sleep 100
```

## REST API

```sh
export $(scontrol token)
```

```sh
curl -v -H X-SLURM-USER-NAME:${USER} -H X-SLURM-USER-TOKEN:${SLURM_JWT} 'http://localhost:6820/openapi'
```

## Accounting

```sh
sacctmgr add cluster las
```

```sh
sacctmgr list cluster
```

:::{literalinclude} /_files/centos/output/sacctmgr/list_cluster.txt
:language: text
:class: cli-output
:::

Check the database:

```sh
mysql -u slurmdbd -p slurm_acct_db
```

In MySQL client:

```sql
select * from cluster_table;
select id_job, job_name from las_job_table;
```
