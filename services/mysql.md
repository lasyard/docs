# MySQL

<https://www.mysql.com/>

The world's most popular open source database.

## Usage

### Create user

Start mysql client:

```sh
mysql -u root -p
```

In mysql client:

```sql
CREATE USER xxx IDENTIFIED BY 'xxxxxxxx';
GRANT ALL ON xxdb.* to 'xxx'@'%';
quit;
```

Relogin as the new user:

```sql
mysql -u xxx -p
```

In mysql client:

```sql
CREATE DATABASE xxdb;
```
