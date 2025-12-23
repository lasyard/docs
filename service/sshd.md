# sshd

本页说明在 Debian 12 上安装、启用与配置 OpenSSH 服务器（sshd）的常用步骤、基本排错和安全建议。

## 1 准备

以具有 `sudo` 权限的用户登录系统。推荐先更新软件包索引：

```console
$ sudo apt update
$ sudo apt upgrade -y
```

## 2 安装 OpenSSH Server

```console
$ sudo apt install -y openssh-server
```

安装后，Debian 的服务名为 `ssh`（而不是 `sshd`），使用 systemd 管理。

## 3 启用并启动服务

服务默认已启用。

```console
$ sudo systemctl status ssh --no-pager
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/lib/systemd/system/ssh.service; enabled; preset: enabled)
     Active: active (running) since Tue 2025-12-23 02:07:20 CST; 1min 15s ago
       Docs: man:sshd(8)
             man:sshd_config(5)
   Main PID: 3226 (sshd)
      Tasks: 1 (limit: 2236)
     Memory: 1.4M
        CPU: 36ms
     CGroup: /system.slice/ssh.service
             └─3226 "sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups"
```

确认服务正在运行且没有错误。

## 4 验证监听端口

查看 ssh 是否在端口 22 上监听：

```console
$ sudo ss -tlnp | grep :22
LISTEN 0      128          0.0.0.0:22        0.0.0.0:*    users:(("sshd",pid=3226,fd=3))
LISTEN 0      128             [::]:22           [::]:*    users:(("sshd",pid=3226,fd=4))
```

或：

```console
$ sudo lsof -iTCP -sTCP:LISTEN -P | grep ssh
sshd    3226 root    3u  IPv4  34555      0t0  TCP *:22 (LISTEN)
sshd    3226 root    4u  IPv6  34566      0t0  TCP *:22 (LISTEN)
```

## 5 基本配置文件

主配置文件为 `/etc/ssh/sshd_config`。常见调整：

:::{literalinclude} /_files/debian/etc/ssh/sshd_config
:diff: /_files/debian/etc/ssh/sshd_config.orig
:::

修改后，重载配置：

```console
$ sudo systemctl reload ssh
```

如果遇到问题，可先用 `sshd` 检查配置语法：

```console
$ sudo sshd -t
```
