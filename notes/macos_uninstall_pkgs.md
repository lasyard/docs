# 在 macOS 上卸载 pkg 方式安装的程序

在 macOS 系统上，用 `pkg` 文件安装的程序一般没有显式的卸载方法，需要手动清除。

以 `Python-3.12` 为例，首先列出所安装的软件包：

```console
$ pkgutil --pkgs | grep python
org.python.Python.PythonFramework-3.12
org.python.Python.PythonDocumentation-3.12
org.python.Python.PythonApplications-3.12
org.python.Python.PythonUnixTools-3.12
```

可见有四个软件包被安装了，需要逐一手动清除，查看软件包信息：

```console
$ pkgutil --pkg-info org.python.Python.PythonFramework-3.12
package-id: org.python.Python.PythonFramework-3.12
version: 0
volume: /
location: Library/Frameworks/Python.framework
install-time: 1717572134
$ pkgutil --pkg-info org.python.Python.PythonDocumentation-3.12
package-id: org.python.Python.PythonDocumentation-3.12
version: 0
volume: /
location: Library/Frameworks/Python.framework/Versions/3.12/Resources/English.lproj/Documentation
install-time: 1717572134
$ pkgutil --pkg-info org.python.Python.PythonApplications-3.12 
package-id: org.python.Python.PythonApplications-3.12
version: 0
volume: /
location: Applications
install-time: 1717572134
$ pkgutil --pkg-info org.python.Python.PythonUnixTools-3.12
package-id: org.python.Python.PythonUnixTools-3.12
version: 0
volume: /
location: usr/local/bin
install-time: 1717572134
```

包之间的依赖关系不好确定，但可见的是 PythonDocumentation 这个包安装在 PythonFramework 的目录内，另外 PythonUnixTools 安装的文件实际上是指向 PythonFramework 的一堆链接，所以应该先移除 PythonUnixTools 和 PythonUnixTools.

由于 `pkgutil` 列出的文件路径是相对于安装目录的，所以执行命令前先进入包的安装目录：

```console
$ cd /Library/Frameworks/Python.framework/Versions/3.12/Resources/English.lproj/Documentation
$ pkgutil --only-files --files org.python.Python.PythonDocumentation-3.12 | tr '\n' '\0' | xargs -n 1 -0 sudo rm -f
$ pkgutil --only-dirs --files org.python.Python.PythonDocumentation-3.12 | tail -r | tr '\n' '\0' | xargs -n 1 -0 sudo rmdir
$ cd /usr/local/bin
$ pkgutil --only-files --files org.python.Python.PythonUnixTools-3.12 | tr '\n' '\0' | xargs -n 1 -0 sudo rm -f
$ pkgutil --only-dirs --files org.python.Python.PythonUnixTools-3.12 | tail -r | tr '\n' '\0' | xargs -n 1 -0 sudo rmdir
```

先删文件再删目录。`tail -r` 将输入的每一行倒序排列，确保先删子目录再删父目录。如果能确信目录下的文件都属于这个软件包，也可以直接删除整个目录。

其他软件包的操作类似：

```console
$ cd /Applications
$ pkgutil --only-files --files org.python.Python.PythonApplications-3.12 | tr '\n' '\0' | xargs -n 1 -0 sudo rm -f
$ pkgutil --only-dirs --files org.python.Python.PythonApplications-3.12 | tail -r | tr '\n' '\0' | xargs -n 1 -0 sudo rmdir
$ cd /Library/Frameworks/Python.framework
$ pkgutil --only-files --files org.python.Python.PythonFramework-3.12 | tr '\n' '\0' | xargs -n 1 -0 sudo rm -f
$ pkgutil --only-dirs --files org.python.Python.PythonFramework-3.12 | tail -r | tr '\n' '\0' | xargs -n 1 -0 sudo rmdir
```

有些目录因为非空无法删除，可经甄别后手动删除。

最后别忘了从数据库中清除安装包的记录：

```console
$ sudo pkgutil --forget org.python.Python.PythonUnixTools-3.12   
Forgot package 'org.python.Python.PythonUnixTools-3.12' on '/'.
$ sudo pkgutil --forget org.python.Python.PythonDocumentation-3.12
Forgot package 'org.python.Python.PythonDocumentation-3.12' on '/'.
$ sudo pkgutil --forget org.python.Python.PythonApplications-3.12
Forgot package 'org.python.Python.PythonApplications-3.12' on '/'.
$ sudo pkgutil --forget org.python.Python.PythonFramework-3.12
Forgot package 'org.python.Python.PythonFramework-3.12' on '/'.
```
