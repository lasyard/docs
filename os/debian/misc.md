# Miscellaneous

## Change runlevel

On Debian 12, using `systemctl`.

Show default:

```console
$ systemctl get-default
graphical.target
```

Show loaded targets:

```console
$ systemctl list-units --type=target
  UNIT                  LOAD   ACTIVE SUB    DESCRIPTION
  basic.target          loaded active active Basic System
  bluetooth.target      loaded active active Bluetooth Support
  cryptsetup.target     loaded active active Local Encrypted Volumes
  getty.target          loaded active active Login Prompts
  graphical.target      loaded active active Graphical Interface
  integritysetup.target loaded active active Local Integrity Protected Volumes
  local-fs-pre.target   loaded active active Preparation for Local File Systems
  local-fs.target       loaded active active Local File Systems
  multi-user.target     loaded active active Multi-User System
  network-online.target loaded active active Network is Online
  network.target        loaded active active Network
  paths.target          loaded active active Path Units
  remote-fs.target      loaded active active Remote File Systems
  slices.target         loaded active active Slice Units
  sockets.target        loaded active active Socket Units
  sound.target          loaded active active Sound Card
  swap.target           loaded active active Swaps
  sysinit.target        loaded active active System Initialization
  time-set.target       loaded active active System Time Set
  timers.target         loaded active active Timer Units
  veritysetup.target    loaded active active Local Verity Protected Volumes

LOAD   = Reflects whether the unit definition was properly loaded.
ACTIVE = The high-level unit activation state, i.e. generalization of SUB.
SUB    = The low-level unit activation state, values depend on unit type.
21 loaded units listed. Pass --all to see loaded but inactive units, too.
To show all installed unit files use 'systemctl list-unit-files'.
```

Set target:

```console
$ sudo systemctl set-default multi-user.target
Created symlink /etc/systemd/system/default.target → /lib/systemd/system/multi-user.target.
```

Now reboot:

```console
$ sudo reboot

Broadcast message from root@xxxx-deb12 on pts/2 (Tue 2025-12-23 03:11:44 CST):

The system will reboot now!
```
