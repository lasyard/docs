# 控制系统 CPU 使用

## 设置内核参数 `isolcpus`

这个参数可以禁止内核向指定的 CPU 调度进程（包括内核本身），除非进程显式绑定在某些 CPU 上。例如 `isolcpus=0-3` 可以使 CPU 0,1,2,3 完全空闲出来给那些指定了 CPU 的进程使用。用以下命令查看生效的设置：

```console
$ cat /sys/devices/system/cpu/isolated
```

## 用 `taskset` 命令设置 CPU 亲和性

例如：

```console
$ taskset -c 1,3 sleep infinity
```

此命令还可以用来查看进程的 CPU 亲和性设置，例如：

```console
$ taskset -p 423201
pid 423201's current affinity mask: a
```

输出亲和性掩码为 `a` 对应的二进制第 1 位和第 3 位为 1, 表示使用了 CPU 1, 3.

也可以直接查看 `proc` 文件系统：

```console
$ cat /proc/423201/status | grep Cpus_allowed
Cpus_allowed:       0000000,0000000a
Cpus_allowed_list:  1,3
```

## 设置服务的 CPU 亲和性

```console
$ sudo systemctl edit --full kubelet
```

添加以下内容：

```ini
[Service]
CPUAffinity=0-3
```

将使服务只在 CPU 0-3 上运行。

## 设置 IRQ 的 CPU 亲和性

通过写 `proc` 文件系统，例如：

```console
$ echo 00000040,00000000 > /proc/irq/123/smp_affinity
```

设置了 123 号中断的 CPU 亲和性掩码。注意需要 `root` 权限并且不是任意一个中断都可以修改。

查询：

```console
$ cat /proc/irq/123/effective_affinity
00000040,00000000
```
