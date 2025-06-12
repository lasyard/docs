# Beam Cloud

<https://www.beam.cloud/>

## Quick Start

Create a env for test:

```console
$ python3 -m venv beam-quickstart/.venv
$ . beam-quickstart/.venv/bin/activate
```

Install Beam Client:

```console
$ pip install beam-client
$ beam --version
beam, version 0.2.161
```

Configure:

```console
$ beam configure default --token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Added new context to /Users/xxxx/.beam/config.ini
$ cat /Users/xxxx/.beam/config.ini 
[default]
token = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
gateway_host = gateway.beam.cloud
gateway_port = 443
```

Show available machine types:

```console
$ beam machine list
                        
  GPU Type   Available  
 ────────────────────── 
  A100-40       ✅      
  A100-80       ❌      
  A10G          ✅      
  A6000         ❌      
  H100          ✅      
  L4            ❌      
  L40S          ❌      
  RTX4090       ✅      
  T4            ✅      
                        
  9 items               
```

Create a Python app:

:::{literalinclude} /_files/macos/workspace/beam.cloud/app/app.py
:::

Save it as `app/app.py`, then sumbit it to beam.cloud:

```console
$ cd app
$ python app.py
=> Building image 
=> Using cached image 
=> Syncing files 
...
=> Uploading 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 336/336 bytes 0:00:00
=> Files synced 
=> Running function: <app:square> 
Loading image <d055bc4ee4ad0e61>...
Loaded image <d055bc4ee4ad0e61>, took: 14.627716ms
This code is running on a remote worker!
=> Function complete <73aee64e-a7a0-4dc0-8c3e-176031b79566> 
The square is 1764
```

:::{tip}
Beam Client will submit all `.py` files in the current working directory, so better make a new directory for a new app.
:::

Create another Python app to check GPU:

:::{literalinclude} /_files/macos/workspace/beam.cloud/gpu/gpu.py
:::

Save it as `gpu/gpu.py`, then submit it:

```console
$ cd gpu
$ python gpu.py 
=> Building image 
=> Using cached image 
=> Syncing files 
...
=> Uploading 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 370/370 bytes 0:00:00
=> Files synced 
=> Running function: <gpu:is_gpu_available> 
Loading image <d055bc4ee4ad0e61>...
Loaded image <d055bc4ee4ad0e61>, took: 13.300503ms
Tue Jun  3 03:39:54 2025       
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 570.86.15              Driver Version: 570.86.15      CUDA Version: 12.8     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  Tesla T4                       On  |   00000000:00:1D.0 Off |                    0 |
| N/A   25C    P8             13W /   70W |       1MiB /  15360MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
                                                                                         
+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+
This code is running on a remote GPU!
=> Function complete <428c8442-dd62-46ca-9adf-23b364c08f4a>
```

## Deploy Beta9

### Deploy local-path StorageClass

```console
$ curl -LO https://raw.githubusercontent.com/rancher/local-path-provisioner/v0.0.31/deploy/local-path-storage.yaml
$ kubectl apply -f local-path-storage.yaml 
namespace/local-path-storage created
serviceaccount/local-path-provisioner-service-account created
role.rbac.authorization.k8s.io/local-path-provisioner-role created
clusterrole.rbac.authorization.k8s.io/local-path-provisioner-role created
rolebinding.rbac.authorization.k8s.io/local-path-provisioner-bind created
clusterrolebinding.rbac.authorization.k8s.io/local-path-provisioner-bind created
deployment.apps/local-path-provisioner created
storageclass.storage.k8s.io/local-path created
configmap/local-path-config created
```

Check existence:

```console
$ kubectl get sc local-path
NAME         PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
local-path   rancher.io/local-path   Delete          WaitForFirstConsumer   false                  2m5s
```

### Create namespace beta9

```console
$ kubectl create namespace beta9
namespace/beta9 created
```

:::{note}
Why this is needed? For the workers need to create in namespace `beta9`, which seems to be hard coded. Then the `redis` must be in the same namespace, and the `localstack`.
:::

### Deploy localstack

Add repo and pull the chart:

```console
$ helm repo add localstack-repo https://helm.localstack.cloud
$ helm pull localstack-repo/localstack
```

Create a file `localstack_values.yaml` to customize it:

:::{literalinclude} /_files/macos/workspace/beam.cloud/localstack_values.yaml
:::

Install:

```console
$ helm install localstack localstack-0.6.24.tgz -f localstack_values.yaml -n beta9
NAME: localstack
LAST DEPLOYED: Thu Jun 12 15:57:36 2025
NAMESPACE: beta9
STATUS: deployed
REVISION: 1
NOTES:
1. Get the application URL by running these commands:
  export NODE_PORT=$(kubectl get --namespace "beta9" -o jsonpath="{.spec.ports[0].nodePort}" services localstack)
  export NODE_IP=$(kubectl get nodes --namespace "beta9" -o jsonpath="{.items[0].status.addresses[0].address}")
  echo http://$NODE_IP:$NODE_PORT
```

### Deploy beta9

```console
$ helm pull oci://public.ecr.aws/n4e0e1y0/beta9-chart
Pulled: public.ecr.aws/n4e0e1y0/beta9-chart:0.1.492
Digest: sha256:9c576c52acdfa6d80073252a157eb7cbc909df17ab0505e4926ceecdc66aeeb2
$ helm install beta9 beta9-chart-0.1.492.tgz -n beta9
NAME: beta9
LAST DEPLOYED: Thu Jun 12 15:47:43 2025
NAMESPACE: beta9
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

Expose the service:

```console
$ kubectl port-forward -n beta9 --address=0.0.0.0 svc/beta9-gateway 1993 1994
Forwarding from 0.0.0.0:1993 -> 1993
Forwarding from 0.0.0.0:1994 -> 1994
...
```

### Install beta9 client

```console
$ pip install beta9
$ beta9 --version
beta9, version 0.1.194
```

At the first time you run `beta9`, a `default` config is created:

```console
$ beta9
=> Welcome to Beta9! Let's get started 📡 

           ,#@@&&&&&&&&&@&/
        @&&&&&&&&&&&&&&&&&&&&@#
         *@&&&&&&&&&&&&&&&&&&&&&@/
   ##      /&&&&&&&&&&&&&@&&&&&&&&@,
  @&&&&&.    (&&&&&&@/    &&&&&&&&&&/
 &&&&&&&&&@*   %&@.      @& ,@&&&&&&&,
.@&&&&&&&&&&&&#        &&*  ,@&&&&&&&&
*&&&&&&&&&&&@,   %&@/@&*    @&&&&&&&&@
.@&&&&&&&&&*      *&@     .@&&&&&&&&&&
 %&&&&&&&&     /@@*     .@&&&&&&&&&&@,
  &&&&&&&/.#@&&.     .&&&    %&&&&&@,
   /&&&&&&&@%*,,*#@&&(         ,@&&
     /&&&&&&&&&&&&&&,
        #@&&&&&&&&&&,
            ,(&@@&&&,

Gateway Host [0.0.0.0]: 10.220.70.56
Gateway Port [1993]: 
Token: 
=> Authorizing with gateway 
=> Authorized 🎉 
Usage: beta9 [OPTIONS] COMMAND [ARGS]...

Options:
  -c, --context TEXT  The config context to use.  [default: default]
  --version           Show the version and exit.
  -h, --help          Show this message and exit.

Common Commands:
  deploy  Deploy a new function.
  serve   Serve a function.
  ls      List contents in a volume.
  cp      Upload or download contents to or from a volume.
  rm      Remove content from a volume.
  mv      Move a file or directory to a new location within the same volume.
  shell   Connect to a container with the same config as your handler.
  run     Run a container.
  dev     Spins up a remote environment to develop in.

Management Commands:
  config      Manage configuration contexts.
  container   Manage containers.
  deployment  Manage deployments.
  machine     Manage remote machines.
  pool        Manage worker pools.
  secret      Manage secrets
  task        Manage tasks.
  token       Manage tokens.
  volume      Manage volumes.
  worker      Manage workers.
```

:::{note}
The gateway address and port are vital, but the token can be left empty.
:::

Show the configs:

```console
$ cat ~/.beta9/config.ini 
[default]
token = nyIkEBkBTj0kWh4Ln1Aj5m4EeXUySxHcbjNoo98MgSTFEju7zaGKKVOrvvz2PHdCL7bi0rrLtin-df_O5Le8Uw==
gateway_host = 10.220.70.56
gateway_port = 1993
```

### Run a program

Modify the `app/app.py` to use `beta9`:

:::{literalinclude} /_files/macos/workspace/beam.cloud/beta9/app.py
:diff: /_files/macos/workspace/beam.cloud/app/app.py
:::

Run it:

```console
$ python app.py 
=> Building image 
...
Loaded image <39b588f7692f2114>, took: 320ns
Python 3.10.12

Saving image, this may take a few minutes...
=> Build complete 🎉 
=> Syncing files 
...
=> Uploading 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 336/336 bytes 0:00:00
=> Files synced 
=> Running function: <app:square> 
Loading image <88d1fd193ae6c25f>...
Loaded image <88d1fd193ae6c25f>, took: 269ns
Unable to connect to gateway.
Function failed <ae5cc75b-59fb-49b0-9883-74fbb8cba613> ❌
The square is None
```

:::{error}
Error occured. Don't know why.
:::

:::{tip}
Copy the beta9 config to beam:

```console
$ cp ~/.beta9/config.ini ~/.beam/config.ini
```

Then you can run the program using `beam`. The output is just the same.
:::
