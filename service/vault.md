# HashiCorp Vault

## Install

:::::{tab-set}
::::{tab-item} Ubuntu
:sync: ubuntu

Add the HashiCorp repository:

```console
$ wget -O - https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
$ echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(grep -oP '(?<=UBUNTU_CODENAME=).*' /etc/os-release || lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
$ sudo apt update
```

Install:

```console
$ sudo apt install vault
```

::::
:::::

Show the version:

```console
$ vault --version
Vault v2.0.2 (a71d5add7ef4111ec4015e9a81b06388f652e2ac), built 2026-06-04T13:18:11Z
```

## Usage

Start a server (in development mode):

```console
$ vault server -dev -dev-root-token-id root -dev-tls -dev-listen-address=0.0.0.0:8200
==> Vault server configuration:

Administrative Namespace: 
             Api Address: https://0.0.0.0:8200
                     Cgo: disabled
         Cluster Address: https://0.0.0.0:8201
   Environment Variables: BASH_ENV, BASH_FUNC_ml%%, BASH_FUNC_module%%, DBUS_SESSION_BUS_ADDRESS, FPATH, GOTRACEBACK, GPG_TTY, HADOOP_CLASSPATH, HADOOP_HOME, HOME, HTTPS_PROXY, HTTP_PROXY, JAVA_HOME, LANG, LESSCLOSE, LESSOPEN, LMOD_CMD, LMOD_DIR, LMOD_PKG, LMOD_ROOT, LMOD_SETTARG_FULL_SUPPORT, LMOD_VERSION, LMOD_sys, LOGNAME, LS_COLORS, MANPATH, MODULEPATH, MODULEPATH_ROOT, MODULESHOME, MOTD_SHOWN, NO_PROXY, OLDPWD, PATH, PWD, SHELL, SHLVL, SPACK_USER_CACHE_PATH, SSH_AUTH_SOCK, SSH_CLIENT, SSH_CONNECTION, SSH_TTY, SYSTEMD_EDITOR, TERM, USER, XDG_RUNTIME_DIR, XDG_SESSION_CLASS, XDG_SESSION_ID, XDG_SESSION_TYPE, _
              Go Version: go1.26.4
              Listener 1: tcp (addr: "0.0.0.0:8200", cluster address: "0.0.0.0:8201", disable_request_limiter: "false", max_json_array_element_count: "10000", max_json_depth: "300", max_json_object_entry_count: "10000", max_json_string_value_length: "1048576", max_request_duration: "1m30s", max_request_size: "33554432", tls: "enabled")
               Log Level: 
                   Mlock: supported: true, enabled: false
           Recovery Mode: false
                 Storage: inmem
                 Version: Vault v2.0.2, built 2026-06-04T13:18:11Z
             Version Sha: a71d5add7ef4111ec4015e9a81b06388f652e2ac

==> Vault server started! Log data will stream in below:
...
WARNING! dev mode is enabled! In this mode, Vault runs entirely in-memory
and starts unsealed with a single unseal key. The root token is already
authenticated to the CLI, so you can immediately begin using Vault.

You may need to set the following environment variables:

    $ export VAULT_ADDR='https://0.0.0.0:8200'
    $ export VAULT_CACERT='/tmp/vault-tls980794796/vault-ca.pem'


The unseal key and root token are displayed below in case you want to
seal/unseal the Vault or re-authenticate.

Unseal Key: 07S81uZhEUl8ivUz7GRrA9/awbIOfRVb3KULe0n2MnI=
Root Token: root

Development mode should NOT be used in production installations!
```

In another console, export the environments mentioned above, then:

```console
$ vault status
Key             Value
---             -----
Seal Type       shamir
Initialized     true
Sealed          false
Total Shares    1
Threshold       1
Version         2.0.2
Build Date      2026-06-04T13:18:11Z
Storage Type    inmem
Cluster Name    vault-cluster-8aaeb4a0
Cluster ID      1eda1913-6056-d1c4-120e-52812f742647
HA Enabled      false
```

Vault in development mode shipped with a KV engine named `secret`:

```console
$ vault kv list -mount=secret
No value found at secret/metadata
```

Create a new secret:

```console
$ vault kv put -mount=secret foo bar=baz
= Secret Path =
secret/data/foo

======= Metadata =======
Key                Value
---                -----
created_time       2026-06-05T10:06:37.975872355Z
custom_metadata    <nil>
deletion_time      n/a
destroyed          false
version            1
```

Get the secret:

```console
$ vault kv get -mount=secret foo
= Secret Path =
secret/data/foo

======= Metadata =======
Key                Value
---                -----
created_time       2026-06-05T10:06:37.975872355Z
custom_metadata    <nil>
deletion_time      n/a
destroyed          false
version            1

=== Data ===
Key    Value
---    -----
bar    baz
```

Now list the secrets again, you can see it:

```console
$ vault kv list -mount=secret
Keys
----
foo
```

Add new key/value pairs to the secrets:

```console
$ vault kv patch -mount=secret foo name=Alice
= Secret Path =
secret/data/foo

======= Metadata =======
Key                Value
---                -----
created_time       2026-06-05T10:10:45.578453101Z
custom_metadata    <nil>
deletion_time      n/a
destroyed          false
version            2
```

Get the new version of the secret:

```console
$ vault kv get -mount=secret foo
= Secret Path =
secret/data/foo

======= Metadata =======
Key                Value
---                -----
created_time       2026-06-05T10:10:45.578453101Z
custom_metadata    <nil>
deletion_time      n/a
destroyed          false
version            2

==== Data ====
Key     Value
---     -----
bar     baz
name    Alice
```
