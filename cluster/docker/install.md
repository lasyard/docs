# Install Docker

## Add docker repository

::::{tabs}
:::{group-tab} Ubuntu

```console
$ sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
$ echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | sudo tee /etc/apt/sources.list.d/docker.list
```

:::
::::

## install

::::{tabs}
:::{group-tab} Ubuntu

```console
$ sudo apt update
$ sudo apt install -y docker-ce
```

:::
::::

## Check the version

```console
$ docker version
Client: Docker Engine - Community
 Version:           28.0.4
 API version:       1.48
 Go version:        go1.23.7
 Git commit:        b8034c0
 Built:             Tue Mar 25 15:07:11 2025
 OS/Arch:           linux/amd64
 Context:           default

Server: Docker Engine - Community
 Engine:
  Version:          28.0.4
  API version:      1.48 (minimum version 1.24)
  Go version:       go1.23.7
  Git commit:       6430e49
  Built:            Tue Mar 25 15:07:11 2025
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.7.27
  GitCommit:        05044ec0a9a75232cad458027ca83437aae3f4da
 runc:
  Version:          1.2.5
  GitCommit:        v1.2.5-0-g59923ef
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
```

More detailed information:

```console
$ docker info
Client: Docker Engine - Community
 Version:    28.0.4
 Context:    default
 Debug Mode: false
 Plugins:
  buildx: Docker Buildx (Docker Inc.)
    Version:  v0.22.0
    Path:     /usr/libexec/docker/cli-plugins/docker-buildx
  compose: Docker Compose (Docker Inc.)
    Version:  v2.34.0
    Path:     /usr/libexec/docker/cli-plugins/docker-compose

Server:
 Containers: 10
  Running: 0
  Paused: 0
  Stopped: 10
 Images: 12
 Server Version: 28.0.4
 Storage Driver: overlay2
  Backing Filesystem: extfs
  Supports d_type: true
  Using metacopy: false
  Native Overlay Diff: true
  userxattr: false
 Logging Driver: json-file
 Cgroup Driver: systemd
 Cgroup Version: 2
 Plugins:
  Volume: local
  Network: bridge host ipvlan macvlan null overlay
  Log: awslogs fluentd gcplogs gelf journald json-file local splunk syslog
 Swarm: inactive
 Runtimes: io.containerd.runc.v2 nvidia runc
 Default Runtime: runc
 Init Binary: docker-init
 containerd version: 05044ec0a9a75232cad458027ca83437aae3f4da
 runc version: v1.2.5-0-g59923ef
 init version: de40ad0
 Security Options:
  apparmor
  seccomp
   Profile: builtin
  cgroupns
 Kernel Version: 5.15.0-136-generic
 Operating System: Ubuntu 22.04.5 LTS
 OSType: linux
 Architecture: x86_64
 CPUs: 8
 Total Memory: 7.749GiB
 Name: gpu
 ID: 26673a31-3df0-437f-b4b4-43b3713e85b1
 Docker Root Dir: /var/lib/docker
 Debug Mode: false
 Experimental: false
 Insecure Registries:
  ::1/128
  127.0.0.0/8
 Registry Mirrors:
  https://docker.m.daocloud.io/
 Live Restore Enabled: false
```

## Run hello-world

:::{tip}
To use docker as current user, add it to group `docker`:

```console
$ sudo usermod -aG docker $(whoami)
```

After adding group, you need to relogin.
:::

Pull the image:

```console
$ docker pull hello-world
Using default tag: latest
latest: Pulling from library/hello-world
e6590344b1a5: Pull complete 
Digest: sha256:c41088499908a59aae84b0a49c70e86f4731e588a737f1637e73c8c09d995654
Status: Downloaded newer image for hello-world:latest
docker.io/library/hello-world:latest
```

List images:

```console
$ docker images
REPOSITORY    TAG                              IMAGE ID       CREATED         SIZE
hello-world   latest                           74cc54e27dc4   2 months ago    10.1kB
```

Inspect the image:

```console
$ docker inspect hello-world
[
    {
        "Id": "sha256:74cc54e27dc41bb10dc4b2226072d469509f2f22f1a3ce74f4a59661a1d44602",
        "RepoTags": [
            "hello-world:latest"
        ],
        "RepoDigests": [
            "hello-world@sha256:c41088499908a59aae84b0a49c70e86f4731e588a737f1637e73c8c09d995654"
        ],
        "Parent": "",
        "Comment": "buildkit.dockerfile.v0",
        "Created": "2025-01-21T23:32:32Z",
        "DockerVersion": "",
        "Author": "",
        "Config": {
            "Hostname": "",
            "Domainname": "",
            "User": "",
            "AttachStdin": false,
            "AttachStdout": false,
            "AttachStderr": false,
            "Tty": false,
            "OpenStdin": false,
            "StdinOnce": false,
            "Env": [
                "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
            ],
            "Cmd": [
                "/hello"
            ],
            "Image": "",
            "Volumes": null,
            "WorkingDir": "/",
            "Entrypoint": null,
            "OnBuild": null,
            "Labels": null
        },
        "Architecture": "amd64",
        "Os": "linux",
        "Size": 10072,
        "GraphDriver": {
            "Data": {
                "MergedDir": "/var/lib/docker/overlay2/73005a260320a98b0ea688377afd4923b2b3044fe5c74a825834c569b2c8221c/merged",
                "UpperDir": "/var/lib/docker/overlay2/73005a260320a98b0ea688377afd4923b2b3044fe5c74a825834c569b2c8221c/diff",
                "WorkDir": "/var/lib/docker/overlay2/73005a260320a98b0ea688377afd4923b2b3044fe5c74a825834c569b2c8221c/work"
            },
            "Name": "overlay2"
        },
        "RootFS": {
            "Type": "layers",
            "Layers": [
                "sha256:63a41026379f4391a306242eb0b9f26dc3550d863b7fdbb97d899f6eb89efe72"
            ]
        },
        "Metadata": {
            "LastTagTime": "0001-01-01T00:00:00Z"
        }
    }
]
```

Run the image as a container:

```console
$ docker run hello-world

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

List all (including stopped) containers:

```console
$ docker ps -a
CONTAINER ID   IMAGE                  COMMAND                  CREATED              STATUS                          PORTS     NAMES
d8fb9ed77f39   hello-world            "/hello"                 About a minute ago   Exited (0) About a minute ago             interesting_lichterman
```
