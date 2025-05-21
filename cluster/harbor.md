# Harbor

<https://goharbor.io/>

## Prerequistes

Intall [docker](project:docker/install.md) first.

## Install

Download:

```console
$ curl -LO https://github.com/goharbor/harbor/releases/download/v2.12.3/harbor-offline-installer-v2.12.3.tgz
```

Extract:

```console
$ tar -C ~/workspace/ -xzf harbor-offline-installer-v2.12.3.tgz
$ cd ~/workspace/harbor
```

Copy file `harbor.yml.tmpl` to `harbor.yml` and edit it:

:::{literalinclude} /_files/ubuntu/workspace/harbor/harbor.yml
:diff: /_files/ubuntu/workspace/harbor/harbor.yml.tmpl
:::

The configurations use `HTTPS`, so you may need to "<#configure-https>" first. Then start to install:

```console
$ sudo ./install.sh

[Step 0]: checking if docker is installed ...

Note: docker version: 28.1.1

[Step 1]: checking docker-compose is installed ...

Note: Docker Compose version v2.35.1

[Step 2]: loading Harbor images ...
...
[Step 3]: preparing environment ...

[Step 4]: preparing harbor configs ...
...
[Step 5]: starting Harbor ...
[+] Running 10/10
 ✔ Network harbor_harbor        Created                                0.1s 
 ✔ Container harbor-log         Started                                0.6s 
 ✔ Container harbor-portal      Started                                0.7s 
 ✔ Container harbor-db          Started                                0.9s 
 ✔ Container registry           Started                                0.8s 
 ✔ Container registryctl        Started                                0.8s 
 ✔ Container redis              Started                                0.7s 
 ✔ Container harbor-core        Started                                1.0s 
 ✔ Container nginx              Started                                1.2s 
 ✔ Container harbor-jobservice  Started                                1.2s 
✔ ----Harbor has been installed and started successfully.----
```

After successful installation, open the url and login by user `admin` and the configured `harbor_admin_password`.

Push an image to the harbor:

```console
$ docker tag busybox:1.37.0-glibc las3\:443/busybox:1.37.0-glibc
$ docker login las3\:443 -u admin -p admin-password
WARNING! Using --password via the CLI is insecure. Use --password-stdin.
Login Succeeded
$ docker push las3\:443/library/busybox:1.37.0-glibc
The push refers to repository [las3:443/library/busybox]
068f50152bbc: Pushed 
1.37.0-glibc: digest: sha256:f2e98ad37e4970f48e85946972ac4acb5574c39f27c624efbd9b17a3a402bfe4 size: 527
$ docker logout las3\:443
Removing login credentials for las3:443
```

:::{note}
You need always put the port number after your simple hostname, for `docker` try to add `docker.io` prefix before your hostname, which is awful design.
:::

:::{caution}
The project `library` is public, which means anyone can pull from it.
:::

## Configure HTTPS

Generate a Certificate Authority Certificate:

```console
$ openssl genrsa -out ca.key 4096
$ openssl req -x509 -new -nodes -sha512 -days 3650 -subj "/C=CN/ST=Beijing/L=Beijing/O=Lasyard/OU=Lasy/CN=las3" -key ca.key -out ca.crt
```

The subject fields are explained below (by GitHub Copilot):

- `C`: Country — The country code (ISO 3166-1 alpha-2), here "CN" stands for China
- `ST`: State or Province — The state or province within the country, here "Beijing"
- `L`: Locality — The city or locality, again "Beijing"
- `O`: Organization — The name of the organization, here "Lasyard"
- `OU`: Organizational Unit — A sub-division or department within the organization, here "Lasy"
- `CN`: Common Name — The name of the entity, typically the server name for SSL/TLS certificates or the name of the Certificate Authority (CA). Here, it is "las3"

Create x509 v3 extension file `v3.ext`:

:::{literalinclude} /_files/ubuntu/workspace/harbor/v3.ext
:language: ini
:::

Generate a Server Certificate:

```console
$ openssl genrsa -out las3.key 4096
$ openssl req -sha512 -new -subj "/C=CN/ST=Beijing/L=Beijing/O=Lasyard/OU=Lasy/CN=las3" -key las3.key -out las3.csr
$ openssl x509 -req -sha512 -days 3650 -extfile v3.ext -CA ca.crt -CAkey ca.key -CAcreateserial -in las3.csr -out las3.crt
Certificate request self-signature ok
subject=C = CN, ST = Beijing, L = Beijing, O = Lasyard, OU = Lasy, CN = las3
```

Copy the certs to the path configured in `harbor.yml`:

```console
$ sudo mkdir /srv/data/cert
$ sudo cp las3.crt las3.key /srv/data/cert/
```

## Trust CA

If we pull images from our new Harbor, we will get:

```console
$ docker pull las3:443/library/busybox:1.37.0-glibc
Error response from daemon: Get "https://las3:443/v2/": tls: failed to verify certificate: x509: certificate signed by unknown authority
```

Because our CA is not trusted by the system.

You can install the `ca.crt` into the system to make it trusted:

```console
$ sudo cp ca.crt /usr/local/share/ca-certificates/
$ sudo update-ca-certificates 
Updating certificates in /etc/ssl/certs...
rehash: warning: skipping ca-certificates.crt,it does not contain exactly one certificate or CRL
1 added, 0 removed; done.
Running hooks in /etc/ca-certificates/update.d...
done.
```

Alternatively, the `ca.crt` can be copied to `docker` config dir to make it trusted only by `docker`:

```console
$ openssl x509 -inform PEM -in las3.crt -out las3.cert
$ sudo mkdir -p /etc/docker/certs.d/las3\:443
$ sudo cp ca.crt /etc/docker/certs.d/las3\:443
```

Anyway, the `docker` daemon need to be restarted:

```console
$ sudo systemctl restart docker
```

:::{tip}
Harbor containers were stopped during restarting of docker, start them by:

```console
$ docker start $(docker ps -a | grep goharbor | cut -d' ' -f1)
```

:::

:::{important}
To make a kubernetes cluster trust the self signed CA, it need to be added to the system before restarting the container runtime service, e.g. `containerd`:

```console
$ sudo systemctl restart containerd
```

:::
