# Slurm Usage

## sinfo

Watch the status of cluster at an interval of 5 seconds:

```sh
sinfo -i 5
```

Node-centric format:

:::{literalinclude} /_files/centos/console/sinfo/n.txt
:language: console
:::

Customized format:

:::{literalinclude} /_files/centos/console/sinfo/o.txt
:language: console
:::

List the reasons nodes are down or drained (a while after stopping `slurmd` service on `las2`):

:::{literalinclude} /_files/centos/console/sinfo/r.txt
:language: console
:::

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

:::{literalinclude} /_files/centos/console/sacctmgr/list_cluster.txt
:language: console
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

Show job history:

:::{literalinclude} /_files/centos/console/sacct/no_args.txt
:language: console
:::
