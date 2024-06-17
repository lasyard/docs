# ssh

## Usage

### Generate pub key from private key

```sh
ssh-keygen -y -f id_rsa > id_rsa.pub
```

### Create password free login

```sh
ssh-copy-id xxxx-host
```
