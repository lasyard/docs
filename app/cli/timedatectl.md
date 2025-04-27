# timedatectl

Show information:

```console
$ timedatectl
               Local time: Sun 2025-04-27 05:30:15 UTC
           Universal time: Sun 2025-04-27 05:30:15 UTC
                 RTC time: Sun 2025-04-27 05:30:15
                Time zone: Etc/UTC (UTC, +0000)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
```

List available time zones:

```console
$ timedatectl list-timezones
Africa/Abidjan
Africa/Accra
Africa/Addis_Ababa
Africa/Algiers
Africa/Asmara
Africa/Asmera
Africa/Bamako
Africa/Bangui
Africa/Banjul
Africa/Bissau
Africa/Blantyre
Africa/Brazzaville
Africa/Bujumbura
Africa/Cairo
Africa/Casablanca
...
```

Set time zone:

```console
$ sudo timedatectl set-timezone Asia/Shanghai
$ timedatectl 
               Local time: Sun 2025-04-27 13:34:53 CST
           Universal time: Sun 2025-04-27 05:34:53 UTC
                 RTC time: Sun 2025-04-27 05:34:53
                Time zone: Asia/Shanghai (CST, +0800)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
```
