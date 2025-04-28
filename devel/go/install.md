# Install GO Development Environment

## By package manager

::::{tabs}
:::{tab} CentOS 8.5

Install Go using `dnf` (The version is quite old, so it is not recommended):

```console
$ sudo dnf install go-toolset
```

:::
::::

## By release tar ball

Donwload and install Go manually:

```console
$ curl -LO https://go.dev/dl/go1.22.1.linux-amd64.tar.gz
$ sudo rm -rf /usr/local/go
$ sudo tar -C /usr/local -xzf go1.22.1.linux-amd64.tar.gz
$ echo "PATH=\"/usr/local/go/bin:\${PATH}\"" | sudo tee /etc/profile.d/go.sh
```
