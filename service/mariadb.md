# MariaDb

<https://mariadb.org/>

MariaDB Server: the innovative open source database.

## Install

:::{plat} centos

```sh
sudo dnf install mariadb-server
```

Show the version:

```sh
mysql --version
```

{.cli-output}

```text
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
