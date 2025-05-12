# systemd-timesyncd

To set time sync server address on client, you need to edit `/etc/systemd/timesyncd.conf`:

:::{literalinclude} /_files/ubuntu/etc/systemd/timesyncd.conf
:diff: /_files/ubuntu/etc/systemd/timesyncd.conf.orig
:::

```console
$ sudo systemctl restart systemd-timesyncd
```

Show time sync options:

```console
$ timedatectl show-timesync
SystemNTPServers=las0
FallbackNTPServers=ntp.ubuntu.com
ServerName=las0
ServerAddress=10.225.4.51
RootDistanceMaxUSec=5s
PollIntervalMinUSec=32s
PollIntervalMaxUSec=34min 8s
PollIntervalUSec=34min 8s
Frequency=0
```

Show timesync status:

```console
$ timedatectl timesync-status
       Server: 10.225.4.51 (las0)
Poll interval: 34min 8s (min: 32s; max 34min 8s)
 Packet count: 0
```
