# systemctl

`systemctl` is a CLI command to control the systemd system and service manager.

## Show status

```console
$ systemctl status
● las3
    State: running
     Jobs: 0 queued
   Failed: 0 units
    Since: Tue 2025-12-30 17:06:24 CST; 3 months 14 days ago
   CGroup: /
```

Show failed services:

```console
$ systemctl --failed
  UNIT LOAD ACTIVE SUB DESCRIPTION
0 loaded units listed.
```

## Reset failed

After remove(disable) the failed services, need to reset the failed status:

```console
$ sudo systemctl reset-failed
```

## Mask

By symbolic linking a unit file to `/dev/null`, prevent it from restarting:

```console
$ sudo systemctl mask x11-common
Created symlink /etc/systemd/system/x11-common.service → /dev/null.
```

List masked services:

```console
$ systemctl list-unit-files --state=masked
UNIT FILE                                                            STATE  VENDOR PRESET
cryptdisks-early.service                                             masked enabled      
cryptdisks.service                                                   masked enabled      
hwclock.service                                                      masked enabled      
lvm2.service                                                         masked enabled      
multipath-tools-boot.service                                         masked enabled      
rc.service                                                           masked enabled      
rcS.service                                                          masked enabled      
screen-cleanup.service                                               masked enabled      
sudo.service                                                         masked enabled      
x11-common.service                                                   masked enabled      

10 unit files listed.
```

If you try to enable a masked service:

```console
$ sudo systemctl enable sudo
Failed to enable unit: Unit file /etc/systemd/system/sudo.service is masked.
```

Unmask an unit file just deleting the symbolic link:

```console
$ sudo systemctl unmask x11-common
Removed /etc/systemd/system/x11-common.service.
```
