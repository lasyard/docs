# volcano

<https://volcano.sh/en/>

Install with helm:

```console
$ helm repo add volcano-sh https://volcano-sh.github.io/helm-charts
"volcano-sh" has been added to your repositories
$ helm repo update
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "volcano-sh" chart repository
Update Complete. ⎈Happy Helming!⎈
$ helm pull volcano-sh/volcano
$ helm install volcano volcano-1.11.2.tgz -n volcano-system --create-namespace
NAME: volcano
LAST DEPLOYED: Tue Apr 22 03:47:04 2025
NAMESPACE: volcano-system
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
Thank you for installing volcano.

Your release is named volcano.

For more information on volcano, visit:
https://volcano.sh/
```

Show the installed release:

```console
$ helm list -n volcano-system
NAME    NAMESPACE       REVISION    UPDATED                                 STATUS      CHART           APP VERSION
volcano volcano-system  1           2025-04-22 03:47:04.391250411 +0000 UTC deployed    volcano-1.11.1  1.11.1
```

Show the created `queue`s:

```console
$ kubectl get q
NAME      AGE
default   2s
root      2s
```

If you don't want to pull images while installing:

```console
$ helm install volcano volcano-1.11.2.tgz -n volcano-system --create-namespace --set basic.image_pull_policy=IfNotPresent
```

## vcctl

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
