# vcctl

Download from GitHub:

```console
$ git clone -b v1.11.1 git@github.com:volcano-sh/volcano.git
```

Build (need C++ and Go development environments, see "<project:/devel/cpp/install.md>" and "<project:/devel/go/install.md>"):

```console
$ cd volcano/
$ make vcctl
$ cp _output/bin/vcctl ${HOME}/bin
```

Show queue list:

```console
$ vcctl queue list
Name                     Weight  State   Inqueue Pending Running Unknown Completed
default                  1       Open    0       0       1       0       0
root                     1       Open    0       0       0       0       0
test                     1       Open    0       0       0       0       0
```

Show job list:

```console
$ vcctl job list
Name    Creation       Phase       JobType     Replicas    Min   Pending   Running   Succeeded   Failed    Unknown     RetryCount
sleep   2025-05-07     Running     Batch       3           3     0         3         0           0         0           0
```
