# tsh

<https://goteleport.com/>

## Install

Download the packages:

:::::{tab-set}

::::{tab-item} macOS

```console
$ curl -LO https://cdn.teleport.dev/tsh-16.1.0.pkg
```

:::{tip}
You can install the desktop GUI version first:

```console
$ curl -LO https://cdn.teleport.dev/Teleport%20Connect-16.1.8.dmg
```

Then select "Install tsh in PATH" on the top-right ellipsis button.
:::

::::
::::{tab-item} Linux

```console
$ curl -LO https://cdn.teleport.dev/teleport-v16.1.0-linux-amd64-bin.tar.gz
```

::::
:::::

Show the version:

```console
$ tsh version
Teleport v16.1.0 git:v16.1.0-0-gfd6032e go1.22.5
```

## Usage

Login:

```console
$ tsh login --proxy=xxxx.teleport --user=xxxx
Enter password for Teleport user xxxx:
Enter an OTP code from a device:
> Profile URL:        https://xxxx.teleport
  Logged in as:       xxxx
  Cluster:            xxxx.teleport
  Roles:              k8s_admin_role
...
```

These info can also be gotten by:

```console
$ tsh status
> Profile URL:        https://xxxx.teleport
  Logged in as:       xxxx
  Cluster:            xxxx.teleport
  Roles:              k8s_admin_role
...
```

Show versions in logined status:

```console
$ tsh version
Teleport v16.1.0 git:v16.1.0-0-gfd6032e go1.22.5
Proxy version: 16.5.12
Proxy: xxxx.teleport
```

List all clusters:

```console
$ tsh clusters                                                  
Cluster Name                    Status Cluster Type Labels       Selected 
------------------------------- ------ ------------ ------------ -------- 
xxxx.teleport                   online root                      *        
xxxx.teleport.las1              online leaf         cluster=las1
```

Switch to another cluster:

```console
$ tsh login xxxx.teleport.las1
```

List hosts:

```console
$ tsh ls
Node Name         Address    Labels                              
----------------- ---------- ----------------------------------- 
...
```

SSH to a host:

```console
$ tsh ssh root@host-xxxx
```

Copy files to a host:

```console
$ tsh scp volcano-1.12.2.tgz root@host-xxxx:
volcano-1.12.2.tgz 100% |████████████████████████████████████████████████████████████████████████████████████████████| (81/81 kB, 9.5 MB/s)
```

List available kubernetes clusters:

```console
$ tsh kube ls
Kube Cluster Name Labels   Selected
----------------- -------- --------
las               role=k8s *       
```

Login into a kubernetes cluster:

```console
$ tsh kube login las
```

The login info is added to `~/.kube/config`. Now you can use `kubectl` to access the cluster.

Logout:

```console
$ tsh logout
Logged out all users from all proxies.
```
