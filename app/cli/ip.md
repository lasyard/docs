# ip

## Usage

Show version:

```console
$ ip -V
ip utility, iproute2-5.15.0, libbpf 0.5.0
```

Show links (MAC addr):

```console
$ ip link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: ens3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether fa:16:3e:6e:71:6d brd ff:ff:ff:ff:ff:ff
    altname enp0s3
```

Show ip addresses:

```console
$ ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: ens3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether fa:16:3e:6e:71:6d brd ff:ff:ff:ff:ff:ff
    altname enp0s3
    inet 10.225.4.51/24 metric 100 brd 10.225.4.255 scope global dynamic ens3
       valid_lft 79956sec preferred_lft 79956sec
    inet6 fe80::f816:3eff:fe6e:716d/64 scope link 
       valid_lft forever preferred_lft forever
```
