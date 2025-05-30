# Install GO Development Environment

## By package manager

::::{tab-set}
:::{tab-item} CentOS 8.5

Install Go by `dnf`:

```console
$ sudo dnf install go-toolset
```

:::
:::{tab-item} Ubuntu 22.04

Install Go by `apt`:

```console
$ sudo apt install -y golang
```

Show the version:

```console
$ go version
go version go1.18.1 linux/amd64
```

:::
::::

The packaged version is quite old, so it is not recommended.

## By release tar balls

Donwload and install Go manually:

```console
$ curl -LO https://go.dev/dl/go1.24.2.linux-amd64.tar.gz
$ sudo rm -rf /usr/local/go
$ sudo tar -C /usr/local -xzf go1.24.2.linux-amd64.tar.gz
$ echo "PATH=\"/usr/local/go/bin:\${PATH}\"" | sudo tee /etc/profile.d/go.sh
```
