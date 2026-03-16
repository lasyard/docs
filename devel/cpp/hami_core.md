# HAMi-core

下载源代码：

```console
$ git clone git@github.com:Project-HAMi/HAMi-core.git
```

## 构建

### 在主机上

`HAMi-core` 使用 C 语言开发，主机需要安装开发环境，如 `gcc` 工具链，`make` 和 `CMake` 工具。

`HAMi-core` 不支持最新的 CUDA 13.0, 建议降级到 CUDA 12.8.

在 `Hami-core` 源代码目录内：

```console
$ ./build.sh
...
[ 95%] Linking C executable ../../shrreg-tool
[ 95%] Built target test_runtime_host_register
[ 95%] Built target shrreg-tool
[ 97%] Linking C shared library ../libvgpu.so
[ 97%] Built target vgpu
nvcc warning : Support for offline compilation for architectures prior to '<compute/sm/lto>_75' will be removed in a future release (Use -Wno-deprecated-gpu-targets to suppress warning).
[100%] Linking CXX executable test_runtime_launch
[100%] Built target test_runtime_launch
```

输出文件 `libvgpu.so` 在目录 `build/` 下。

## 使用

设置环境变量：

```console
$ export LD_PRELOAD="$(pwd)/build/libvgpu.so"
$ export CUDA_DEVICE_MEMORY_LIMIT=1g
$ export CUDA_DEVICE_SM_LIMIT=50
```

:::{caution}
设置 `LD_PRELOAD` 将使所有新启动的进程都依赖 `libcuda.so.1`, 不管有没有用 GPU.
:::

如果之前用过 `HAMi-core`, 可能需要删除缓存的配置：

```console
$ rm /tmp/cudevshr.cache
```

查看：

```console
$ nvidia-smi 
[HAMI-core Msg(3263897:139913786537792:libvgpu.c:836)]: Initializing.....
Thu Aug 28 15:34:24 2025       
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 570.124.06             Driver Version: 570.124.06     CUDA Version: 12.8     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  Tesla P4                       Off |   00000000:00:05.0 Off |                    0 |
| N/A   39C    P0             22W /   75W |       0MiB /   1024MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
                                                                                         
+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+
[HAMI-core Msg(3263897:139913786537792:multiprocess_memory_limit.c:459)]: Calling exit handler 3263897
```

从输出可见报告的内存被限制在了 1GiB.
