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

Enable the server:

```console
$ sudo systemctl enable mariadb --now
```

:::
:::{tab} Ubuntu 22.04

```console
$ sudo apt install mariadb-server
```

Check the version:

```console
$ mysql --version
mysql  Ver 15.1 Distrib 10.6.21-MariaDB, for debian-linux-gnu (x86_64) using  EditLine wrapper
```

:::
::::

Initialize:

```console
$ sudo mysql_secure_installation
```

## Usage

### Show users

In mysql client:

```sql
SELECT user FROM mysql.user;
```

## Troubleshoot

### Bind address

On Ubuntu 22.04, the default binding address is `127.0.0.1`. Change it by edit file `/etc/mysql/mariadb.conf.d/50-server.cnf`:

:::{literalinclude} /_files/ubuntu/etc/mysql/mariadb.conf.d/50-server.cnf
:diff: /_files/ubuntu/etc/mysql/mariadb.conf.d/50-server.cnf.orig
:::

Then restart the service:

```console
$ sudo systemctl restart mariadb
```

### Reinstall database

In case you want to completely wipe out the data, clear the data dir (default to `/var/lib/mysql`):

```console
$ sudo rm -rf /var/lib/mysql/*
```

Then do this:

```console
$ sudo mysql_install_db --user=mysql
Installing MariaDB/MySQL system tables in '/var/lib/mysql' ...
2025-05-12 16:09:53 0 [Warning] You need to use --log-bin to make --expire-logs-days or --binlog-expire-logs-seconds work.
OK

To start mariadbd at boot time you have to copy
support-files/mariadb.service to the right place for your system


Two all-privilege accounts were created.
One is root@localhost, it has no password, but you need to
be system 'root' user to connect. Use, for example, sudo mysql
The second is mysql@localhost, it has no password either, but
you need to be the system 'mysql' user to connect.
After connecting you can set the password, if you would need to be
able to connect as any of these users with a password and without sudo

See the MariaDB Knowledgebase at https://mariadb.com/kb

You can start the MariaDB daemon with:
cd '/usr' ; /usr/bin/mariadbd-safe --datadir='/var/lib/mysql'

You can test the MariaDB daemon with mysql-test-run.pl
cd '/usr/share/mysql/mysql-test' ; perl mariadb-test-run.pl

Please report any problems at https://mariadb.org/jira

The latest information about MariaDB is available at https://mariadb.org/.

Consider joining MariaDB's strong and vibrant community:
https://mariadb.org/get-involved/
```
