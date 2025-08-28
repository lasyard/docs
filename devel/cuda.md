# CUDA

<https://developer.nvidia.com/cuda-toolkit>

Download the installer:

```console
$ curl -LO https://developer.download.nvidia.com/compute/cuda/13.0.0/local_installers/cuda_13.0.0_580.65.06_linux.run
$ chmod +x cuda_13.0.0_580.65.06_linux.run
```

Before installation, close any program using GPU devices or it ought to fail. Then install:

```console
$ sudo ./cuda_13.0.0_580.65.06_linux.run 
===========
= Summary =
===========

Driver:   Installed
Toolkit:  Installed in /usr/local/cuda-13.0/

Please make sure that
 -   PATH includes /usr/local/cuda-13.0/bin
 -   LD_LIBRARY_PATH includes /usr/local/cuda-13.0/lib64, or, add /usr/local/cuda-13.0/lib64 to /etc/ld.so.conf and run ldconfig as root

To uninstall the CUDA Toolkit, run cuda-uninstaller in /usr/local/cuda-13.0/bin
To uninstall the NVIDIA Driver, run nvidia-uninstall
Logfile is /var/log/cuda-installer.log
```

:::{note}
Be patient! It is slow and need interactive inputs.
:::

:::{caution}
`cuda-uninstaller` is not installed if you do not install Demo/Documentation, though mentioned in the output.
:::

Check:

```console
$ nvidia-smi
Thu Aug 28 11:23:00 2025       
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 580.65.06              Driver Version: 580.65.06      CUDA Version: 13.0     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  Tesla P4                       Off |   00000000:00:05.0 Off |                    0 |
| N/A   39C    P0             21W /   75W |       0MiB /   7680MiB |      2%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+
```

Check the compiler version:

```console
$ /usr/local/cuda/bin/nvcc --version
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2025 NVIDIA Corporation
Built on Wed_Jul_16_07:30:01_PM_PDT_2025
Cuda compilation tools, release 13.0, V13.0.48
Build cuda_13.0.r13.0/compiler.36260728_0
```
