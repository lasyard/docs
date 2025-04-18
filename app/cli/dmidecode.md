# dmidecode

`dmidecode` is a tool for dumping a computer's DMI (some say SMBIOS) table contents in a human-readable format.

For example:

```console
$ sudo dmidecode -s system-manufacturer
OpenStack Foundation
$ sudo dmidecode -s system-product-name
OpenStack Nova
$ sudo dmidecode -s system-version
28.3.1
$ sudo dmidecode -s system-family
Virtual Machine
$ sudo dmidecode -s system-uuid
4b16a34c-d5a8-4edb-934a-0cef51bf0fe1
```

`sudo` previleges may be required to run these command. Acctually, on most Linux systems, you can also read the information from `sysfs` even without `sudo`:

```console
$ cat /sys/devices/virtual/dmi/id/sys_vendor
OpenStack Foundation
$ cat /sys/devices/virtual/dmi/id/product_name 
OpenStack Nova
$ cat /sys/devices/virtual/dmi/id/product_version 
28.3.1
$ cat /sys/devices/virtual/dmi/id/product_family 
Virtual Machine
$ sudo cat /sys/devices/virtual/dmi/id/product_uuid 
4b16a34c-d5a8-4edb-934a-0cef51bf0fe1
```

:::{tip}

- You can tell if the host is a virtual machine or physical machine
- UUID is often used to identify the host

:::
