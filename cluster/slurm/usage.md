# Slurm Usage

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
