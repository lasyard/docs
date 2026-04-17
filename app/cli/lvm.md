# LVM

On Linux, there are a suite of CLI commands to manage LVM.

## PV

Create a physical volume:

```console
$ sudo pvcreate /dev/loop0
  Physical volume "/dev/loop0" successfully created.
```

List physical volumes:

```console
$ sudo pvs
  PV         VG     Fmt  Attr PSize   PFree  
  /dev/loop0 ceph-0 lvm2 a--  <20.00g <20.00g
```

Show the details of physical volumes:

```console
$ sudo pvdisplay
  "/dev/loop0" is a new physical volume of "20.00 GiB"
  --- NEW Physical volume ---
  PV Name               /dev/loop0
  VG Name               
  PV Size               20.00 GiB
  Allocatable           NO
  PE Size               0   
  Total PE              0
  Free PE               0
  Allocated PE          0
  PV UUID               0uNbwM-yuk7-P3kg-SSM2-xUq2-44q7-d7g83h
```

Delete a physical volume:

```console
$ sudo pvremove /dev/loop0
  Labels on physical volume "/dev/loop0" successfully wiped.
```

## VG

We can group physical volumes into a volume group:

```console
$ sudo vgcreate ceph-0 /dev/loop0
  Volume group "ceph-0" successfully created
```

List volume groups:

```console
$ sudo vgs
  VG     #PV #LV #SN Attr   VSize   VFree  
  ceph-0   1   0   0 wz--n- <20.00g <20.00g
```

Show the details of volume groups:

```console
$ sudo vgdisplay
  --- Volume group ---
  VG Name               ceph-0
  System ID             
  Format                lvm2
  Metadata Areas        1
  Metadata Sequence No  1
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                0
  Open LV               0
  Max PV                0
  Cur PV                1
  Act PV                1
  VG Size               <20.00 GiB
  PE Size               4.00 MiB
  Total PE              5119
  Alloc PE / Size       0 / 0   
  Free  PE / Size       5119 / <20.00 GiB
  VG UUID               TJTmBr-SSl7-txVF-g171-1OqI-qVpc-RyyK71
```

Delete a volume group:

```console
$ sudo vgremove ceph-0
  Volume group "ceph-0" successfully removed
```

## LV

Use all free space on a volume group to create a logical volumes:

```console
$ sudo lvcreate -n ceph-osd-0 -l 100%FREE ceph-0
  Logical volume "ceph-osd-0" created.
```

List logical volumes:

```console
$ sudo lvs
  LV         VG     Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  ceph-osd-0 ceph-0 -wi-a----- <20.00g
```

Show details of logical volumes:

```console
$ sudo lvdisplay
  --- Logical volume ---
  LV Path                /dev/ceph-0/ceph-osd-0
  LV Name                ceph-osd-0
  VG Name                ceph-0
  LV UUID                I26WbA-r37n-dfen-kBfy-5MyV-4MwP-naDWQX
  LV Write Access        read/write
  LV Creation host, time las3, 2026-04-16 17:44:51 +0800
  LV Status              available
  # open                 0
  LV Size                <20.00 GiB
  Current LE             5119
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:0
```

The device of the logical volume is created:

```console
$ ls -l /dev/ceph-0/ceph-osd-0 
lrwxrwxrwx 1 root root 7 Apr 16 17:54 /dev/ceph-0/ceph-osd-0 -> ../dm-0
```

Remove all logical volumes on a volume group:

```console
$ sudo lvremove ceph-0
Do you really want to remove and DISCARD active logical volume ceph-0/ceph-osd-0? [y/n]: y
  Logical volume "ceph-osd-0" successfully removed
```
