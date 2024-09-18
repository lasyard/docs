# rclone

<https://rclone.org/>

Rclone is a command-line program to manage files on cloud storage. It is a feature-rich alternative to cloud vendors' web storage interfaces.

## Usage

Config remotes:

```sh
rclone config
```

List remotes:

```sh
rclone listremotes
```

List files on `xxxx-s3`:

```sh
rclone ls xxxx-s3:
```

Sync dir to local:

```sh
rclone sync xxxx-s3:/xxxx-dir ./
```
