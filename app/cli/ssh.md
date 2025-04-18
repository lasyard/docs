# ssh

## Usage

### Generate key

`rsa` type is depracated, so:

```sh
ssh-keygen -t ed25519 -C "xxxx-comments"
```

### Generate pub key from private key

```sh
ssh-keygen -y -f id_rsa > id_rsa.pub
```

### Create password free login

```sh
ssh-copy-id xxxx-host
```
