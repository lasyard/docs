# Kindle Fire HD 安装第三方操作系统

这个古老设备在 Amazon 不支持之后基本已成砖，不过可以重装非官方系统挽救之。

:::{note}
本文适用于 Kindle Fire HD (2nd generation). 如何识别设备是 Kindle Fire HD (2nd generation)? 在设置中查看菜单`设备·关于·序列号`的前四位是 `D025`.

以下提到的主机是 Windows 10 系统。
:::

重装之路的第一步是获取 Root 权限.

## 1. 获取 Root 权限

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

不过我们可以先做一些有意义的事情——备份。在 `adb shell` 中并切换为 `root` 用户后：

```console
$ dd if=/dev/block/mmcblk0boot0 of=/sdcard/boot0block.img
4096+0 records in
4096+0 records out
2097152 bytes transferred in 0.513 secs (4088015 bytes/sec)
$ dd if=/dev/block/platform/omap/omap_hsmmc.1/by-name/boot of=/sdcard/stock-boot.img
16384+0 records in
16384+0 records out
8388608 bytes transferred in 2.081 secs (4031046 bytes/sec)
$ dd if=/dev/block/platform/omap/omap_hsmmc.1/by-name/recovery of=/sdcard/stock-recovery.img
16384+0 records in
16384+0 records out
8388608 bytes transferred in 2.025 secs (4142522 bytes/sec)
$ dd if=/dev/block/platform/omap/omap_hsmmc.1/by-name/system of=/sdcard/stock-system.img
1814528+0 records in
1814528+0 records out
929038336 bytes transferred in 261.382 secs (3554331 bytes/sec)
```

以上命令将关键数据备份到 `/sdcard` 目录下。然后回到主机命令行，把文件复制回主机：

```console
$ adb pull /sdcard/boot0block.img
/sdcard/boot0block.img: 1 file pulled. 3.3 MB/s (2097152 bytes in 0.601s)
$ adb pull /sdcard/stock-boot.img
/sdcard/stock-boot.img: 1 file pulled. 3.2 MB/s (8388608 bytes in 2.474s)
$ adb pull /sdcard/stock-recovery.img
/sdcard/stock-recovery.img: 1 file pulled. 3.1 MB/s (8388608 bytes in 2.554s)
$ adb pull /sdcard/stock-system.img # This will take a few minutes
/sdcard/stock-system.img: 1 file pulled. 3.2 MB/s (929038336 bytes in 280.605s)
```

:::{tip}
备份的文件据说可以通过 `fastboot` 烧入设备，完全恢复原来状态：

```console
$ fastboot -i 0x1949 flash boot stock-boot.img
$ fastboot -i 0x1949 flash recovery stock-recovery.img
$ fastboot -i 0x1949 flash system stock-system.img
$ fastboot -i 0x1949 reboot
```

没试过不作保证。
:::

## 2. 进入 Fastboot 模式

网上所有针对 Android 设备，通过开机时按住某些键进入 Fastboot 模式的方法对本版本的 Kindle File HD 均不生效。唯一有效的办法是使用一根工程线 (Factory Cable). 工程线的电路如下图：

![moto_amazon_fastboot_cable.png](/_images/hardware/moto_amazon_fastboot_cable.png)

通常的 USB 数据线主机一头是 Type-A, 只有 4 个引脚，设备侧是 Micro USB, ID 脚是悬空的（如果是 OTG 线则是接地的）。很难把一根普通数据线改造成工程线，因为这些线的 Micro USB 一头的 ID 脚没有引出线。只能购买有 5 个引出脚的裸 Micro USB 头进行焊接。

将一根普通数据线的设备端剪掉，露出里面的 4 根引线（一般还有一根裸露的屏蔽线连接到插头的金属外壳）。4 根引线的颜色为红、白、绿、蓝，分别对应 `VBUS`, `D-`, `D+`, `GND`, 焊接到 Micro USB 头的对应引脚。Micro USB 的 `ID` 则需要连接到 `VBUS`，保险起见可以用一个 220Ω 左右的电阻限流。

在设备关机状态下，用工程线连接到主机。设备自动开机并进入 Fastboot 模式，屏幕显示：

![kindle_fastboot.jpg](/_images/hardware/kindle_fastboot.jpg)

打开 Windows 的设备管理器，可以看到一个名为 `Tate-PVT-08` 的设备，需要安装驱动。因为之前装过了 Kindle Fire USB Driver, 现在可以直接从列表中选择 `Fire Devices/Android BootLoader Interface` 安装。

这时在主机命令行界面用 `fastboot` 工具应该可以看到设备：

```console
$ fastboot devices
4E96000200000001        fastboot
```

## 3. 烧录 TWRP

TWRP 代表 [TeamWin Recovery Project](https://twrp.me/), 是一个开源的 Android 恢复软件。

下载以下文件：

- `stack.img`
- `kfhd7-u-boot-prod-7.2.3.img`
- `kfhd7-freedom-boot-7.4.6.img`
- `kfhd7-twrp-2.8.7.0-recovery.img`

先做一些准备工作。正常模式启动设备，使用 `adb` 传输文件 `stack.img` 到设备：

```console
$ adb push stack.img /sdcard
stack.img: 1 file pushed. 0.2 MB/s (4096 bytes in 0.016s)
```

然后打开 `adb shell` 连接并切换到 `root` 用户，使用 `dd` 命令将刚才的文件写入 `system` 分区：

```console
$ dd if=/sdcard/stack.img of=/dev/block/platform/omap/omap_hsmmc.1/by-name/system bs=6519488 seek=1
0+1 records in
0+1 records out
4096 bytes transferred in 0.003 secs (1365333 bytes/sec)
```

据说此神秘的 4k 大小的数据写入可以阻止原操作系统恢复原 `boot` 分区。没有更详细的信息，照做就是！

然后是阻止系统更新 `recovery` 分区。同样是在 `root` 用户的 shell 中：

```console
$ mount -o remount,rw ext4 /system
$ mv /system/etc/install-recovery.sh /system/etc/install-recovery.sh.bak
$ mount -o remount,ro ext4 /system
```

准备完毕，关闭设备并用工程线连接，进入 Fastboot 模式，然后依次烧录 `bootloader`, `boot`, `recovery` 分区并重启设备：

```console
$ fastboot -i 0x1949 flash bootloader kfhd7-u-boot-prod-7.2.3.bin.img
target reported max download size of 1006632960 bytes
sending 'bootloader' (221 KB)...
OKAY [  0.084s]
writing 'bootloader'...
OKAY [  0.047s]
finished. total time: 0.131s
$ fastboot -i 0x1949 flash boot kfhd7-freedom-boot-7.4.6.img
target reported max download size of 1006632960 bytes
sending 'boot' (8145 KB)...
OKAY [  2.875s]
writing 'boot'...
OKAY [  0.670s]
finished. total time: 3.576s
$ fastboot -i 0x1949 flash recovery kfhd7-twrp-2.8.7.0-recovery.img
target reported max download size of 1006632960 bytes
sending 'recovery' (8145 KB)...
OKAY [  2.873s]
writing 'recovery'...
OKAY [  0.688s]
finished. total time: 3.577s
$ fastboot -i 0x1949 reboot
rebooting...

finished. total time: -0.000s
```

重启之后，设备先显示正常的 Kindle 图标，然后显示一个“蓝化”的 Kindle 图标，标志 TWRP 烧录成功了：

![kindle_fire_blue.jpg](/_images/hardware/kindle_fire_blue.jpg)

当以上图标出现时立刻按下音量增加键不放，会出现短暂的花屏，然后进入 TWRP 界面。后续的安装操作系统的任务都可以在这个界面操作完成。

## 4. 安装操作系统

在 TWRP 中，每次安装新的操作系统时可以用 `Wipe` 将旧数据彻底清除，确保新系统中没有旧系统的残留，否则有可能出现新系统启动不了或文件系统权限不对的问题。`Wipe` 时可以选择高级功能并把所有选项都选上，不影响已有的 `bootloader`, `boot` 和 `recovery`.

然后将下载的操作系统 `zip` 包传输到设备的 `/sdcard` 目录下。TWRP 支持 MTP 设备连接，所以这一步无须操作系统也可以进行。最后在 TWRP 中 `Install` 即可。

下面列出一些可用的操作系统。

### LineageOS 14.1

:安装文件: `lineage-14.1-20180326-UNOFFICIAL-tate.zip`
:Android 版本: 7.1.2
:中文支持: 有

界面截图：

```{figure} https://imghost.online/ib/BvRRHLA6votKIae_1755710470.png
:alt: LineageOS 14.1 Desktop
:target: https://imghost.online/en/ntaDF9M2rW5jbFe

LineageOS 14.1 Desktop
```

```{figure} https://imghost.online/ib/Sx5IHmAgsChRycH_1755710470.png
:alt: LineageOS 14.1 Main Menu
:target: https://imghost.online/en/6ggFRoj7dZP7VYz

LineageOS 14.1 Main Menu
```

```{figure} https://imghost.online/ib/gmuVUwWsy65t9NJ_1755710408.png
:alt: LineageOS 14.1 About
:target: https://imghost.online/en/MHoN6pXJhHOfJfw

LineageOS 14.1 About
```

### CyanogenMod 12.1

:安装文件: `cm-12.1-20150602-UNOFFICIAL-tate.zip`
:Android 版本: 5.1.1
:中文支持: 有

界面截图：

```{figure} https://imghost.online/ib/AJu9yCpNK61GTsR_1755710408.png
:alt: CyanogenMod 12.1 Desktop
:target: https://imghost.online/en/F98gBTkbS7tpQHr

CyanogenMod 12.1 Desktop
```

```{figure} https://imghost.online/ib/28hifZbd6cyOPaT_1755710408.png
:alt: CyanogenMod 12.1 Main Menu
:target: https://imghost.online/en/nNjqGpkmV9cQE1h

CyanogenMod 12.1 Main Menu
```

```{figure} https://imghost.online/ib/AGt8WgxC29nOS6M_1755710408.png
:alt: CyanogenMod 12.1 About
:target: https://imghost.online/en/PYVrj0QtxtDIEyh

CyanogenMod 12.1 About
```

### crDroid 7.1.2

:安装文件: `crDroidAndroid-7.1.2-20181021-tate-v3.8.9.zip`
:Android 版本: 5.1.1
:中文支持: 无

界面截图：

```{figure} https://imghost.online/ib/7knmttVmwBKBdaD_1755710408.png
:alt: crDroid 7.1.2 Desktop
:target: https://imghost.online/en/hjOAp6PTqsJKPuW

crDroid 7.1.2 Desktop
```

```{figure} https://imghost.online/ib/Hv1FHZLbRg2SrUl_1755710408.png
:alt: crDroid 7.1.2 Main Menu
:target: https://imghost.online/en/bgplgkMLczGSH6z

crDroid 7.1.2 Main Menu
```

```{figure} https://imghost.online/ib/8dDBVmi5Zrjljqm_1755710408.png
:alt: crDroid 7.1.2 About
:target: https://imghost.online/en/PqfPWbIydoNW0bt

crDroid 7.1.2 About
```

### Carbon

:安装文件: `carbon_tate-ota-9c7a2d1d33-patched.zip`
:Android 版本: 4.4.2
:中文支持: 无

界面截图：

```{figure} https://imghost.online/ib/wjYoraLtlJaxu9a_1755710408.png
:alt: Carbon Desktop
:target: https://imghost.online/en/sSYxTopFDHIbrfc

Carbon Desktop
```

```{figure} https://imghost.online/ib/ptBNvyYjZhQMHhU_1755710408.png
:alt: Carbon Main Menu
:target: https://imghost.online/en/GxKyS8jqHfzDpvk

Carbon Main Menu
```

```{figure} https://imghost.online/ib/HKcyBfhwmovSGC1_1755710408.png
:alt: Carbon About
:target: https://imghost.online/en/4t361C29lojpJXt

Carbon About
```

:::{tip}
Android 版本高可以安装较新的应用，缺点是较新的应用在老硬件上卡顿。

老旧 APK 可以从 <https://www.apkmirror.com/> 这个网站下载。
:::

## 附

本文中的文件可以从 <https://www.mediafire.com/folder/f3hle221i2yaf/kfhd7> 下载。

文件均为搬运而来。下列文件：

- `stack.img`
- `kfhd7-u-boot-prod-7.2.3.bin.img`
- `kfhd7-freedom-boot-7.4.6.img`
- `kfhd7-twrp-2.8.7.0-recovery.img`

从 <https://androidfilehost.com/?w=files&flid=34232> 获得。其中 `kfhd7-u-boot-prod-7.2.3.bin.img` 重命名为 `kfhd7-u-boot-prod-7.2.3.img`, 因为 <https://www.mediafire.com/> 不允许 `.bin.img` 双扩展名。

下列文件：

- `crDroidAndroid-7.1.2-20181021-tate-v3.8.9.zip`
- `lineage-14.1-20180326-UNOFFICIAL-tate.zip`

从 <https://www.mediafire.com/folder/u7sb7p10ik7v0/tate> 获得。
