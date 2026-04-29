# ACL

POSIX ACL(Access Control List) 是对 Unix/Linux 文件系统权限的扩展。

安装 ACL 工具：

::::{tab-set}
:::{tab-item} Ubuntu
:sync: ubuntu

```console
$ sudo apt install acl
```

:::
::::

查看权限：

```console
$ getfacl /home
getfacl: Removing leading '/' from absolute path names
# file: home
# owner: root
# group: root
user::rwx
group::r-x
other::r-x
```
