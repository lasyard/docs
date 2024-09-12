# Miscellaneous Commands

## dmidecode

::::{plat} centos
:vers: CentOS 8.5

`dmidecode` is a tool for dumping a computer's DMI (some say SMBIOS) table contents in a human-readable format.

```sh
sudo dmidecode -s system-manufacturer
sudo dmidecode -s system-product-name
sudo dmidecode -s system-version
```

:::{note}
`sudo` previleges may be required to run these command. Acctually, on most Linux systems, you can also read these information from `sysfs` even without `sudo`:

```sh
cat /sys/devices/virtual/dmi/id/sys_vendor
cat /sys/devices/virtual/dmi/id/product_name
cat /sys/devices/virtual/dmi/id/product_version
```

:::

::::

:::{tip}
You can tell if the host is a virtual machine or physical machine.
:::
