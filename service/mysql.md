# MySQL

<https://www.mysql.com/>

The world's most popular open source database.

## Install

:::{plat} centos

```sh
sudo dnf install mysql-server
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
