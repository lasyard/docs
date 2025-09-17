# nvidia-smi

## Usage

List GPUs:

```console
$ nvidia-smi -L
GPU 0: NVIDIA H100 80GB HBM3 (UUID: GPU-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
```

### MIG

Enable MIG Mode:

```console
$ sudo nvidia-smi -i 0 -mig 1
Enabled MIG Mode for GPU 00000000:16:00.0
All done.
```

The UUID can also be used for parameter `-i`.

List available MIG profile for a GPU:

```console
$ sudo nvidia-smi mig -i 0 -lgip
+-----------------------------------------------------------------------------+
| GPU instance profiles:                                                      |
| GPU   Name             ID    Instances   Memory     P2P    SM    DEC   ENC  |
|                              Free/Total   GiB              CE    JPEG  OFA  |
|=============================================================================|
|   0  MIG 1g.10gb       19     7/7        9.75       No     16     1     0   |
|                                                             1     1     0   |
+-----------------------------------------------------------------------------+
|   0  MIG 1g.10gb+me    20     1/1        9.75       No     16     1     0   |
|                                                             1     1     1   |
+-----------------------------------------------------------------------------+
|   0  MIG 1g.20gb       15     4/4        19.62      No     26     1     0   |
|                                                             1     1     0   |
+-----------------------------------------------------------------------------+
|   0  MIG 2g.20gb       14     3/3        19.62      No     32     2     0   |
|                                                             2     2     0   |
+-----------------------------------------------------------------------------+
|   0  MIG 3g.40gb        9     2/2        39.50      No     60     3     0   |
|                                                             3     3     0   |
+-----------------------------------------------------------------------------+
|   0  MIG 4g.40gb        5     1/1        39.50      No     64     4     0   |
|                                                             4     4     0   |
+-----------------------------------------------------------------------------+
|   0  MIG 7g.80gb        0     1/1        79.25      No     132    7     0   |
|                                                             8     7     1   |
+-----------------------------------------------------------------------------+
```

Form the output we can see 7 instances with profile ID `19` can be created.

List the possible placements available:

```console
$ nvidia-smi mig -i 0 -lgipp
GPU  0 Profile ID 19 Placements: {0,1,2,3,4,5,6}:1
GPU  0 Profile ID 20 Placements: {0,1,2,3,4,5,6}:1
GPU  0 Profile ID 15 Placements: {0,2,4,6}:2
GPU  0 Profile ID 14 Placements: {0,2,4}:2
GPU  0 Profile ID  9 Placements: {0,4}:4
GPU  0 Profile ID  5 Placement : {0}:4
GPU  0 Profile ID  0 Placement : {0}:8
```

Create MIG Instances:

```console
$ sudo nvidia-smi mig -i 0 -cgi 19,19,19,19,19,19,19 -C
Successfully created GPU instance ID 13 on GPU  0 using profile MIG 1g.10gb (ID 19)
Successfully created compute instance ID  0 on GPU  0 GPU instance ID 13 using profile MIG 1g.10gb (ID  0)
Successfully created GPU instance ID 11 on GPU  0 using profile MIG 1g.10gb (ID 19)
Successfully created compute instance ID  0 on GPU  0 GPU instance ID 11 using profile MIG 1g.10gb (ID  0)
Successfully created GPU instance ID 12 on GPU  0 using profile MIG 1g.10gb (ID 19)
Successfully created compute instance ID  0 on GPU  0 GPU instance ID 12 using profile MIG 1g.10gb (ID  0)
Successfully created GPU instance ID  7 on GPU  0 using profile MIG 1g.10gb (ID 19)
Successfully created compute instance ID  0 on GPU  0 GPU instance ID  7 using profile MIG 1g.10gb (ID  0)
Successfully created GPU instance ID  8 on GPU  0 using profile MIG 1g.10gb (ID 19)
Successfully created compute instance ID  0 on GPU  0 GPU instance ID  8 using profile MIG 1g.10gb (ID  0)
Successfully created GPU instance ID  9 on GPU  0 using profile MIG 1g.10gb (ID 19)
Successfully created compute instance ID  0 on GPU  0 GPU instance ID  9 using profile MIG 1g.10gb (ID  0)
Successfully created GPU instance ID 10 on GPU  0 using profile MIG 1g.10gb (ID 19)
Successfully created compute instance ID  0 on GPU  0 GPU instance ID 10 using profile MIG 1g.10gb (ID  0)
```

`-C` means create compute instances for the GPU instances.

List created GPU instances and compute instances:

```console
$ sudo nvidia-smi mig -i 0 -lgi
+-------------------------------------------------------+
| GPU instances:                                        |
| GPU   Name             Profile  Instance   Placement  |
|                          ID       ID       Start:Size |
|=======================================================|
|   0  MIG 1g.10gb         19        7          0:1     |
+-------------------------------------------------------+
|   0  MIG 1g.10gb         19        8          1:1     |
+-------------------------------------------------------+
|   0  MIG 1g.10gb         19        9          2:1     |
+-------------------------------------------------------+
|   0  MIG 1g.10gb         19       10          3:1     |
+-------------------------------------------------------+
|   0  MIG 1g.10gb         19       11          4:1     |
+-------------------------------------------------------+
|   0  MIG 1g.10gb         19       12          5:1     |
+-------------------------------------------------------+
|   0  MIG 1g.10gb         19       13          6:1     |
+-------------------------------------------------------+
$ sudo nvidia-smi mig -i 0 -lci
+--------------------------------------------------------------------+
| Compute instances:                                                 |
| GPU     GPU       Name             Profile   Instance   Placement  |
|       Instance                       ID        ID       Start:Size |
|         ID                                                         |
|====================================================================|
|   0      7       MIG 1g.10gb          0         0          0:1     |
+--------------------------------------------------------------------+
|   0      8       MIG 1g.10gb          0         0          0:1     |
+--------------------------------------------------------------------+
|   0      9       MIG 1g.10gb          0         0          0:1     |
+--------------------------------------------------------------------+
|   0     10       MIG 1g.10gb          0         0          0:1     |
+--------------------------------------------------------------------+
|   0     11       MIG 1g.10gb          0         0          0:1     |
+--------------------------------------------------------------------+
|   0     12       MIG 1g.10gb          0         0          0:1     |
+--------------------------------------------------------------------+
|   0     13       MIG 1g.10gb          0         0          0:1     |
+--------------------------------------------------------------------+
```

Delete all compute instances of all GPU instances of a GPU:

```console
$ sudo nvidia-smi mig -i 0 -dci
Successfully destroyed compute instance ID  0 from GPU  0 GPU instance ID  7
Successfully destroyed compute instance ID  0 from GPU  0 GPU instance ID  8
Successfully destroyed compute instance ID  0 from GPU  0 GPU instance ID  9
Successfully destroyed compute instance ID  0 from GPU  0 GPU instance ID 10
Successfully destroyed compute instance ID  0 from GPU  0 GPU instance ID 11
Successfully destroyed compute instance ID  0 from GPU  0 GPU instance ID 12
Successfully destroyed compute instance ID  0 from GPU  0 GPU instance ID 13
```

Delete all GPU instances of a GPU:

```console
$ sudo nvidia-smi mig -i 0 -dgi
Successfully destroyed GPU instance ID  7 from GPU  0
Successfully destroyed GPU instance ID  8 from GPU  0
Successfully destroyed GPU instance ID  9 from GPU  0
Successfully destroyed GPU instance ID 10 from GPU  0
Successfully destroyed GPU instance ID 11 from GPU  0
Successfully destroyed GPU instance ID 12 from GPU  0
Successfully destroyed GPU instance ID 13 from GPU  0
```

Disable MIG:

```console
$ sudo nvidia-smi -i 0 -mig 0
Disabled MIG Mode for GPU 00000000:16:00.0
All done.
```
