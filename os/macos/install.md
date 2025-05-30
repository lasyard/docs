# macOS Install

See <https://support.apple.com/en-us/102662> to download the installer.

See <https://support.apple.com/en-us/101578> to create a bootable USB drive.

## Create a bootable installer

::::{tab-set}
:::{tab-item} Monterey

Insert a removable disk, then create the bootable installer:

```console
$ sudo /Applications/Install\ macOS\ Monterey.app/Contents/Resources/createinstallmedia --downloadassets --volume /Volumes/XxxxVolume
```

`XxxxVolume` is the name of the volume.

:::
::::

## Install

::::{tab-set}
:::{tab-item} Monterey

Turn on the computer and hold the {kbd}`Option`/{kbd}`Alt` key to see the boot menu.

:::
::::
