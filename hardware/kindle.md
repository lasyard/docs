# Kindle Fire HD 获取 Root 权限

本文适用于 Kindle Fire HD (2nd generation). 如何识别设备是 Kindle Fire HD (2nd generation)? 在设置中查看菜单`设备·关于·序列号`的前四位是 `D025`.

以下提到的主机是 Windows 10 系统。

:::{caution}
获取 Root 权限过程可能导致设备变砖，请谨慎操作！
:::

获取 Root 权限需要用到一个软件包：[root_with_restore_by_bin4ry](https://xdaforums.com/attachments/root_with_restore_by_bin4ry_v33-zip.2476937/). 年代久远，链接不保证有效。

此压缩包里包含了一个老版本的 `adb` 和 `fastboot`. `fastboot` 老到连 `--version` 参数都不支持。可以另外下载较新的版本使用，以下是本文使用的版本：

```console
$ adb version
Android Debug Bridge version 1.0.39
Version 0.0.1-4500957
Installed as C:\Users\xxxx\Downloads\software\Windows\android_tools\adb.exe
$ fastboot --version
fastboot version 0.0.1-4500957
Installed as C:\Users\xxxx\Downloads\software\Windows\android_tools\fastboot.exe
```

操作之前，在设备设置中开启选项`安全·启用 ADB`, 主机上安装驱动 [Kindle Fire USB Driver](https://amzndevresources.com/firetablets/kindle_fire_usb_driver.zip).

连接设备与主机，在设备管理器中应能看到 `Fire Devices/Android Composite ADB Interface`. 此时用 `adb` 也可以找到设备：

```console
$ adb devices
List of devices attached
D025XXXXXXXXXXXX        device
```

解压 `root_with_restore_by_bin4ry.zip` 软件包后直接在命令行窗口运行里面的 `RunMe.bat`:

```console
$ RunMe
======================================================================
= This script will root your Android phone with adb restore function =
= Script by Bin4ry (thanks to Goroh_kun and tkymgr for the idea)     =
=             Idea for Tablet S from Fi01_IS01                       =
=                      (14.12.2013) v33                              =
======================================================================

Device type:
0) Xperia Root by cubeundcube
1) New Standard-Root (thx Ariel Berkman)
2) New Xperia Root by Goroh_kun (Xperia Z, Xperia V [JellyBean] ...)
3) Old
4) Old-Special (for example: Sony Tablet S, Medion Lifetab)
G) Google Glass Mode (thx Saurik for the ab file)

x) Unroot

Make a choice:
```

到此处选择 `1`, 按回车继续：

```console
Please connect Device with enabled USB-Debugging to your Computer
adb server is out of date.  killing...
* daemon started successfully *
Doing a Backup first, please confirm this on your device!
Now unlock your device and confirm the backup operation.
Done!
请按任意键继续. . .
Please select the RESTORE MY DATA option now on your device!
Now unlock your device and confirm the restore operation.
Please press any Key when restore is done.
请按任意键继续. . .
Going to reboot now ...
3268 KB/s (104576 bytes in 0.031s)
4744 KB/s (2139595 bytes in 0.440s)
6105 KB/s (1165484 bytes in 0.186s)
remote object '/system/bin/ric' does not exist
.
Going to copy files to it's place
Rebooting again, please wait!
找不到 C:\Users\xxxx\Downloads\ric
Restoring previous Backup! Please select the RESTORE MY DATA option now on your device!
Now unlock your device and confirm the restore operation.
Please press any Key when restore is done.
请按任意键继续. . .
Going to reboot last time now ...
You can close all open command-prompts now!
After reboot all is done! Have fun!
Bin4ry
请按任意键继续. . .
```

过程中按提示在主机和设备上操作即可，“找不到”的错误可忽略。至此 Root 完成。完成后增加了一个 SuperSU 应用和 `su` 命令。`su` 命令可以在 `adb shell` 中使用。

在设备上打开 SuperSU. 其设置界面如下：

![supersu_settings.png](/_images/hardware/supersu_settings.png)

主机上进入 `adb shell`:

```console
$ adb shell
shell@android:/ $ su
root@android:/ #
```

键入 `su` 命令后，SuperSU 弹出一个授权对话框：

![supersu_request.png](/_images/hardware/supersu_request.png)

授权后 `adb shell` 的提示符中用户变为 `root`, 可以“为所欲为”了。
