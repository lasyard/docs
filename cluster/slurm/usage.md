# Slurm Usage

## sinfo

Watch the status of cluster at an interval of 5 seconds:

```console
$ sinfo -i 5
Mon May 12 18:09:08 2025
PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST
normal*      up   infinite      4   idle las[0-3]
high         up   infinite      4   idle las[0-3]
...
```

Node-centric format:

```console
$ sinfo -N
NODELIST   NODES PARTITION STATE 
las0           1   normal* idle  
las0           1      high idle  
las1           1   normal* idle  
las1           1      high idle  
las2           1   normal* idle  
las2           1      high idle  
las3           1   normal* idle  
las3           1      high idle
```

Customized format:

```console
$ sinfo -o "%20N %10c %10m %25f %G"
NODELIST             CPUS       MEMORY     AVAIL_FEATURES            GRES
las3                 8          7935       (null)                    gpu:nvidia:1(S:0-7)
las[0-2]             16         32090      (null)                    (null)
```

List the reasons nodes are down or drained (a while after stopping `slurmd` service on `las2`):

```console
$ sinfo -R
REASON               USER      TIMESTAMP           NODELIST
Not responding       slurm     2025-05-13T14:22:26 las2
$ sinfo
PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST
normal*      up   infinite      1  down* las2
normal*      up   infinite      3   idle las[0-1,3]
high         up   infinite      1  down* las2
high         up   infinite      3   idle las[0-1,3]
```

:::{tip}
The `*` after the node state means it is not responding.
:::

## srun

Specify the number of nodes:

```console
$ srun -N4 hostname
las3
las1
las2
las0
```

Run on specified node with specified number of tasks:

```console
$ srun -w las2 -n 2 hostname
las2
las2
```

Specify the begin time of job:

```console
$ srun -b now+10 hostname
srun: job 24 queued and waiting for resources
srun: job 24 has been allocated resources
las3
```

In another console, you can see the queued job (before it is finished) with:

```console
$ squeue
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
                24    normal hostname   ubuntu PD       0:00      1 (BeginTime)
```

## REST API

Export the token:

```console
$ export $(scontrol token)
```

Access the site with the token:

```console
$ curl -v -H X-SLURM-USER-NAME:${USER} -H X-SLURM-USER-TOKEN:${SLURM_JWT} 'http://localhost:6820/openapi'
*   Trying 127.0.0.1:6820...
* Connected to localhost (127.0.0.1) port 6820 (#0)
> GET /openapi HTTP/1.1
> Host: localhost:6820
> User-Agent: curl/7.81.0
> Accept: */*
> X-SLURM-USER-NAME:ubuntu
> X-SLURM-USER-TOKEN:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDcxMTkxODcsImlhdCI6MTc0NzExNzM4Nywic3VuIjoidWJ1bnR1In0.zbjEwmJtkDwWL-yUF_-7Kvbzi5JCfExYxvbAE9LAIx0
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Content-Length: 1620152
< Content-Type: application/json
...
```

Unset the token environment variable for it will make `srun` try to use JWT to authenticate (which is not supported by `slurmd`):

```console
$ unset SLURM_JWT
```

## Accounting

List the clusters:

```console
$ sacctmgr list cluster
   Cluster     ControlHost  ControlPort   RPC     Share GrpJobs       GrpTRES GrpSubmit MaxJobs       MaxTRES MaxSubmit     MaxWall                  QOS   Def QOS 
---------- --------------- ------------ ----- --------- ------- ------------- --------- ------- ------------- --------- ----------- -------------------- --------- 
       las       127.0.0.1         6817 10752         1                                                                                           normal
```

Show history of jobs:

```console
$ sacct
JobID           JobName  Partition    Account  AllocCPUS      State ExitCode 
------------ ---------- ---------- ---------- ---------- ---------- -------- 
1              hostname     normal                     1  COMPLETED      0:0 
1.0            hostname                                1  COMPLETED      0:0 
...
```

Check the database:

```console
$ mysql -u slurmdbd -p slurm_acct_db
```

## scontrol

After you altered the configuration files of slurm, you can apply it by:

```console
$ sudo scontrol reconfigure
```

If the state of nodes are not valid, they may stay at the state even if the fail reasons were fixed. You can bring it back mannually by:

```console
$ sudo scontrol update NodeName=las3 State=idle
```
