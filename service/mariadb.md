# MariaDb

<https://mariadb.org/>

## Install

:::{plat} centos
:vers: CentOS 8.5

```sh
sudo dnf install mariadb-server
```

Check the version:

```console
$ mysql --version
mysql  Ver 15.1 Distrib 10.3.28-MariaDB, for Linux (x86_64) using readline 5.1
```

Clear `/var/lib/mysql` if there are remains of previous `mysql/mariadb` installation:

```sh
sudo rm -rf /var/lib/mysql/*
```

Enable the server:

```sh
sudo systemctl enable mariadb --now
```

Initialize:

```sh
mysql_secure_installation
```

:::

## Usage

### Show users

In mysql client:

```sql
SELECT user FROM mysql.user;
```
