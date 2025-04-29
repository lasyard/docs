# MariaDb

<https://mariadb.org/>

## Install

::::{tabs}
:::{tab} CentOS 8.5

```console
$ sudo dnf install mariadb-server
```

Check the version:

```console
$ mysql --version
mysql  Ver 15.1 Distrib 10.3.28-MariaDB, for Linux (x86_64) using readline 5.1
```

Clear `/var/lib/mysql` if there are remains of previous `mysql/mariadb` installation:

```console
$ sudo rm -rf /var/lib/mysql/*
```

Enable the server:

```console
$ sudo systemctl enable mariadb --now
```

:::
::::

Initialize:

```console
$ mysql_secure_installation
```

## Usage

### Show users

In mysql client:

```sql
SELECT user FROM mysql.user;
```
