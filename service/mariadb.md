# MariaDb

<https://mariadb.org/>

## Install

:::::{tab-set}
::::{tab-item} macOS
:sync: macos

```console
$ brew install mariadb
...
==> Caveats
==> mariadb
A "/etc/my.cnf" from another install may interfere with a Homebrew-built
server starting up correctly.

MySQL is configured to only allow connections from localhost by default

To start mariadb now and restart at login:
  brew services start mariadb
Or, if you don't want/need a background service you can just run:
  /opt/homebrew/opt/mariadb/bin/mariadbd-safe --datadir\=/opt/homebrew/var/mysql
```

Show the version:

```console
$ mysql --version
mysql from 12.2.2-MariaDB, client 15.2 for osx10.21 (arm64) using  EditLine wrapper
```

Initialize for production use:

```console
$ sudo mariadb-secure-installation
```

Start the service:

```console
$ brew services start mariadb
==> Successfully started `mariadb` (label: homebrew.mxcl.mariadb)
```

::::
::::{tab-item} CentOS 8
:sync: centos8

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

::::
::::{tab-item} Ubuntu
:sync: ubuntu

```console
$ sudo apt install mariadb-server
```

Check the version:

```console
$ mysql --version
mysql  Ver 15.1 Distrib 10.6.21-MariaDB, for debian-linux-gnu (x86_64) using  EditLine wrapper
```

::::
:::::

Initialize:

```console
$ sudo mysql_secure_installation
```

## Usage

### Show version

In mysql client:

```sql
SELECT version();
```

### Show users

In mysql client:

```sql
SELECT user FROM mysql.user;
```

### Set TLS connection

According to <project:/app/cli/openssl.md>, if you already have a CA key and cert, use it to sign a cert for mysql server:

```console
$ openssl genrsa -out server.key 4096
$ openssl req -new -key server.key -subj "/CN=mysql-server" -out server.csr
$ openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365 -sha256 -extfile <(printf "subjectAltName=DNS:las0,IP:10.220.70.56")
Certificate request self-signature ok
subject=CN = mysql-server
```

> [!IMPORTANT]
> If you want to login to the server remotely, the `/CN` field can be set to the hostname you will use, or bake the "DNS name"/"IP address" into `subjectAltName` by extfile. This is not required if you login at local by UNIX domain socket.

Copy the key and the certs into a dedicated place and allow `mysqld` to read the private key:

```console
$ sudo mkdir /etc/mysql/certs
$ sudo cp ca.crt server.crt server.key /etc/mysql/certs/
$ sudo chown mysql:mysql server.key
```

Create a config file `/etc/mysql/conf.d/tls.cnf`:

:::{literalinclude} /_files/ubuntu/etc/mysql/conf.d/tls.cnf
:language: ini
:::

Make sure this file is included in the main `cnf` file, generally `/etc/mysql/my.cnf`.

Restart `mysql`/`mariadb`. Connect to the db as `root`, check ssl related settings:

```sql
show variables like '%ssl%';
```

The output may be:

```text
+---------------------+-----------------------------+
| Variable_name       | Value                       |
+---------------------+-----------------------------+
| have_openssl        | YES                         |
| have_ssl            | YES                         |
| ssl_ca              | /etc/mysql/certs/ca.crt     |
| ssl_capath          |                             |
| ssl_cert            | /etc/mysql/certs/server.crt |
| ssl_cipher          |                             |
| ssl_crl             |                             |
| ssl_crlpath         |                             |
| ssl_key             | /etc/mysql/certs/server.key |
| version_ssl_library | OpenSSL 3.0.2 15 Mar 2022   |
+---------------------+-----------------------------+
10 rows in set (0.001 sec)
```

Create a user for testing:

```sql
CREATE USER 'tls'@'%' IDENTIFIED BY 'xxxxxxxx' REQUIRE X509;
```

Now generate a key and cert for the new user:

```console
$ openssl genrsa -out client.key 4096
$ openssl req -new -key client.key -subj "/CN=mysql-client" -out client.csr
$ openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 365 -sha256
Certificate request self-signature ok
subject=CN = mysql-client
```

Use the new key and certs to login into mysql server:

```console
$ mysql -u tls -p --ssl-ca=/etc/mysql/certs/ca.crt --ssl-cert=client.crt --ssl-key=client.key
```

The mysql server will check if the certs are valid. After login, check if SSL is enabled:

```sql
SHOW STATUS LIKE 'Ssl_cipher';
```

The output may be:

```text
+---------------+------------------------+
| Variable_name | Value                  |
+---------------+------------------------+
| Ssl_cipher    | TLS_AES_256_GCM_SHA384 |
+---------------+------------------------+
1 row in set (0.001 sec)
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
