# Install GO Development Environment

:::{plat} centos
:vers: CentOS 8.5

Install Go using `dnf` (The version is quite old, so it is not recommended):

```sh
sudo dnf install go-toolset
```

Donwload and install Go manually:

```sh
wget https://go.dev/dl/go1.22.1.linux-amd64.tar.gz
rm -rf /usr/local/go
tar -C /usr/local -xzf go1.22.1.linux-amd64.tar.gz
echo "PATH=\"/usr/local/go/bin:\${PATH}\"" > /etc/profile.d/go.sh
```

:::
