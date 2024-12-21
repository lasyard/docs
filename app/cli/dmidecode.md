# dmidecode

::::{plat} centos
:vers: CentOS 8.5

`dmidecode` is a tool for dumping a computer's DMI (some say SMBIOS) table contents in a human-readable format.

:::{literalinclude} /_files/centos/console/dmidecode/s.txt
:language: console
:::

`sudo` previleges may be required to run these command. Acctually, on most Linux systems, you can also read these information from `sysfs` even without `sudo`:

:::{literalinclude} /_files/centos/console/cat/sys_devices_virtual_dmi_id.txt
:language: console
:::

::::

:::{tip}
You can tell if the host is a virtual machine or physical machine.
:::
