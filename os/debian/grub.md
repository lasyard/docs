# grub

本页说明如何在 Debian 12 中减小 GRUB 的启动等待时间（timeout），以加快系统启动。修改前建议保留备份并确保你能在需要时进入恢复/高级菜单。

## 快速步骤

- 编辑主配置文件 `/etc/default/grub`:

```console
$ sudo vi /etc/default/grub
```

修改内容如下：

:::{literalinclude} /_files/debian/etc/default/grub
:diff: /_files/debian/etc/default/grub.orig
:::

解释：

- `GRUB_TIMEOUT`：以秒为单位的等待时间，设置为 `1` 表示等待 1 秒后自动启动。设置为 `0` 表示立即启动（可能导致难以进入菜单），建议设置 `1` 或 `2` 做折中
- `GRUB_TIMEOUT_STYLE`：可选值 `menu`（显示菜单）、`hidden`（默认隐藏菜单但仍等待超时）等。将其设为 `menu` 可以短暂显示菜单，`hidden` 则更隐蔽

修改完成后，必须更新 grub 配置并使其生效：

```console
$ sudo update-grub
Generating grub configuration file ...
Found background image: /usr/share/images/desktop-base/desktop-grub.png
Found linux image: /boot/vmlinuz-6.1.0-41-amd64
Found initrd image: /boot/initrd.img-6.1.0-41-amd64
Found linux image: /boot/vmlinuz-6.1.0-39-amd64
Found initrd image: /boot/initrd.img-6.1.0-39-amd64
Warning: os-prober will not be executed to detect other bootable partitions.
Systems on them will not be added to the GRUB boot configuration.
Check GRUB_DISABLE_OS_PROBER documentation entry.
done
```

然后重启检查效果：

```console
$ sudo reboot
```

## 额外提示与注意事项

若要临时从下次启动进入特定内核或菜单项，可使用 `grub-reboot` 或 `grub-set-default`：

```console
$ sudo grub-reboot '1>2'   # 示例：根据你的 grub 配置选择项
```
