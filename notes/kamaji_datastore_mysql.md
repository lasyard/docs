---
myst:
  substitutions:
    tcp: TenantControlPlane
---
# Kamaji 中使用 MySQL 作为 DataStore

首先，你得有一个 MySQL/MariaDB 服务。假设服务已经独立部署好了，那么需要为 Kamaji 创建一个账户：

```mysql
CREATE USER 'kamaji'@'%' IDENTIFIED BY 'xxxxxxxx';
GRANT ALL PRIVILEGES ON *.* TO 'kamaji'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```

Kamaji 将为每一个 {{tcp}} 创建以 UUID 为名的数据库，并且试图授权给自己对数据库进行访问，所以 `WITH GRANT OPTION` 很重要。

MySQL 的用户密码需要放在一个 Secret 中，假定已经存在命名空间 `mysql-system`:

```console
$ kubectl create secret generic mysql-secret --from-literal=password='xxxxxxxx' -n mysql-system
secret/mysql-secret created
```

然后创建一个使用 MySQL 的 DataStore:

:::{literalinclude} /_files/macos/workspace/k8s/kamaji/mysql_datastore.yaml
:::

这里的 `spec.basicAuth` 提供了用户名和密码。其中的 `username.content` 必须是 BASE64 编码，`password` 需要引用正确的 Secret 和 key.

查看创建的 DataStore:

```console
$ kubectl get datastore mysql
NAME    DRIVER   READY   AGE
mysql   MySQL    true    20m
```

这里 `READY` 为 `true` 不代表数据库可用，只有创建 {{tcp}} 的时候 Kamaji 才真正去访问数据库。

设置 TenantControlPlane 的 `spec.dataStore` 指向刚才创建的 DataStore `mysql`, 然后创建它，我们来看看 Kamaji 在数据库里干了什么。

```mysql
show databases like '________-____-____-____-____________';
```

输出：

```text
+-------------------------------------------------+
| Database (________-____-____-____-____________) |
+-------------------------------------------------+
| d38ef1a3-ad97-4620-b4c2-aba5e82bb69c            |
+-------------------------------------------------+
1 row in set (0.000 sec)
```

```mysql
use d38ef1a3-ad97-4620-b4c2-aba5e82bb69c;
```

```mysql
show tables;
```

输出：

```text
+------------------------------------------------+
| Tables_in_d38ef1a3-ad97-4620-b4c2-aba5e82bb69c |
+------------------------------------------------+
| kine                                           |
+------------------------------------------------+
1 row in set (0.000 sec)
```

```mysql
desc kine;
```

输出：

```text
+-----------------+---------------------+------+-----+---------+----------------+
| Field           | Type                | Null | Key | Default | Extra          |
+-----------------+---------------------+------+-----+---------+----------------+
| id              | bigint(20) unsigned | NO   | PRI | NULL    | auto_increment |
| name            | varchar(630)        | YES  | MUL | NULL    |                |
| created         | int(11)             | YES  |     | NULL    |                |
| deleted         | int(11)             | YES  |     | NULL    |                |
| create_revision | bigint(20) unsigned | YES  |     | NULL    |                |
| prev_revision   | bigint(20) unsigned | YES  | MUL | NULL    |                |
| lease           | int(11)             | YES  |     | NULL    |                |
| value           | mediumblob          | YES  |     | NULL    |                |
| old_value       | mediumblob          | YES  |     | NULL    |                |
+-----------------+---------------------+------+-----+---------+----------------+
9 rows in set (0.001 sec)
```

## 提升安全性

### 服务器认证

当 MySQL 服务打开 `require_secure_transport=ON` 配置后，通过 TCP Socket 连接数据库需要认证。如果 MySQL 的服务器证书是由不被信任（自签名）的 CA 认证的，那么需要客户端信任此 CA 才能通过认证。

将 CA 的证书添加到集群：

```console
$ kubectl create secret tls mysql-ca --cert ca.crt --key ca.key -n mysql-system
secret/mysql-ca created
$ kubectl describe secret mysql-ca -n mysql-system
Name:         mysql-ca
Namespace:    mysql-system
Labels:       <none>
Annotations:  <none>

Type:  kubernetes.io/tls

Data
====
tls.crt:  1789 bytes
tls.key:  3268 bytes
```

注意 TLS 类型的 Secret 里必须有 `tls.crt` 和 `tls.key`, 认证时只要 `tls.crt`. 另外认证需要的 Secret 类型不必是 TLS, 路径也不必是 `tls.crt`.

修改 DataStore 的定义，增加证书：

:::{literalinclude} /_files/macos/workspace/k8s/kamaji/mysql_ssl_datastore.yaml
:diff: /_files/macos/workspace/k8s/kamaji/mysql_datastore.yaml
:::

### 客户端认证

同样，MySQL 服务器也可以要求客户端持有用户的合法证书。修改用户，要求 X.509 认证：

```mysql
ALTER USER 'kamaji'@'%' REQUIRE X509;
FLUSH PRIVILEGES;
```

添加客户端证书到集群：

```console
$ kubectl create secret tls kamaji-mysql-ca --cert=client.crt --key=client.key -n mysql-system
secret/kamaji-mysql-ca created
```

客户端证书最好也是 MySQL CA 签发的，这样可以直接被信任。

修改 DataStore 的定义，增加客户端证书：

:::{literalinclude} /_files/macos/workspace/k8s/kamaji/mysql_tls_datastore.yaml
:diff: /_files/macos/workspace/k8s/kamaji/mysql_datastore.yaml
:::

> [!TIP]
> 访问数据库如出现问题，可以从 Kamaji 日志中查询：
>
> ```console
> kubectl logs deploy/kamaji -n kamaji-system
> ```
