# kompose

<https://kompose.io/>

Kompose is a conversion tool for Docker Compose to container orchestrators such as Kubernetes (or OpenShift).

## Install

:::{plat} linux
:vers: CentOS 8.5, Ubuntu 22.04

```sh
curl -L https://github.com/kubernetes/kompose/releases/download/v1.33.0/kompose-linux-amd64 -o kompose
chmod +x kompose
sudo cp ./kompose /usr/local/bin
```

:::

## Usage

Convert `docker-compose.yml` in current directory:

```sh
kompose convert
```

Or specify the path of `docker-compose.yml`:

```sh
kompose -f path/to/docker-compose.yml convert
```

Covert to helm chart:

```sh
kompose convert -c
```
