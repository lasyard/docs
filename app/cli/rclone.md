# rclone

<https://rclone.org/>

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
