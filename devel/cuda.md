# CUDA

<https://developer.nvidia.com/cuda-toolkit>

Download the installer:

```console
$ curl -LO https://developer.download.nvidia.com/compute/cuda/12.6.3/local_installers/cuda_12.6.3_560.35.05_linux.run
$ chmod +x cuda_12.6.3_560.35.05_linux.run
$ curl -LO https://developer.download.nvidia.com/compute/cuda/12.9.0/local_installers/cuda_12.9.0_575.51.03_linux.run
$ chmod +x cuda_12.9.0_575.51.03_linux.run
```

Install:

```console
$ sudo ./cuda_12.9.0_575.51.03_linux.run
...
===========
= Summary =
===========

Driver:   Installed
Toolkit:  Installed in /usr/local/cuda-12.9/

Please make sure that
 -   PATH includes /usr/local/cuda-12.9/bin
 -   LD_LIBRARY_PATH includes /usr/local/cuda-12.9/lib64, or, add /usr/local/cuda-12.9/lib64 to /etc/ld.so.conf and run ldconfig as root

To uninstall the CUDA Toolkit, run cuda-uninstaller in /usr/local/cuda-12.9/bin
To uninstall the NVIDIA Driver, run nvidia-uninstall
Logfile is /var/log/cuda-installer.log
```

:::{note}
Be patient! It is slow and need interactive inputs.
:::

Check:

```console
$ nvidia-smi
Fri May 16 18:18:32 2025       
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 575.51.03              Driver Version: 575.51.03      CUDA Version: 12.9     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  Tesla P4                       Off |   00000000:00:05.0 Off |                    0 |
| N/A   40C    P0             21W /   75W |       0MiB /   7680MiB |      0%      Default |
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
$ /usr/local/cuda-12.9/bin/nvcc --version
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2025 NVIDIA Corporation
Built on Wed_Apr__9_19:24:57_PDT_2025
Cuda compilation tools, release 12.9, V12.9.41
Build cuda_12.9.r12.9/compiler.35813241_0
```
