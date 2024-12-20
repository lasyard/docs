# docker

<https://www.docker.com/>

## Install

::::{plat} centos
:vers: CentOS 8.5

Add `docker` repository:

```sh
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
```

Install:

```sh
sudo dnf install docker-ce
```

```sh
sudo systemctl enable docker --now
```

Check the version:

:::{literalinclude} /_files/centos/console/docker/version.txt
:language: console
:::

More detailed information:

:::{literalinclude} /_files/centos/console/docker/info.txt
:language: console
:::

:::{tip}
To use docker as current user, add it to group `docker`.
:::

::::

::::{plat} ubuntu
:vers: Ubuntu 22.04

Download deb packages from <https://download.docker.com/linux/ubuntu/dists/jammy/pool/stable/amd64/>.

Install:

```sh
sudo dpkg -i containerd.io_1.7.19-1_amd64.deb \
    docker-ce_27.1.1-1~ubuntu.22.04~jammy_amd64.deb \
    docker-ce-cli_27.1.1-1~ubuntu.22.04~jammy_amd64.deb
```

::::

## Usage

Add current user to `docker` group to get previlige to use docker command.

### Hello world

Pull the image:

:::{literalinclude} /_files/centos/console/docker/pull_hello_world.txt
:language: console
:::

List images:

:::{literalinclude} /_files/centos/console/docker/images_hello_world.txt
:language: console
:::

Inspect the image:

:::{literalinclude} /_files/centos/console/docker/inspect_hello_world.txt
:language: console
:::

Run the image as a container:

:::{literalinclude} /_files/centos/console/docker/run_hello_world.txt
:language: console
:::

List all (including stopped) containers:

:::{literalinclude} /_files/centos/console/docker/ps_a_hello_world.txt
:language: console
:::

### Run interactively

Find the image:

```sh
docker search ubuntu
```

It seems there is no command to list all tags of an image, go to <https://hub.docker.com/> for information.

Pull the image with specified tag:

:::{literalinclude} /_files/centos/console/docker/pull_ubuntu.txt
:language: console
:::

Run it interactively:

```sh
docker run -it ubuntu:22.04
```

:::{note}
The tag is always needed, or it will pull the latest version.
:::

In shell of the container, press {kbd}`Ctrl+P`, {kbd}`Ctrl+Q` to detach.

List the running containers:

```sh
docker ps
```

:::{literalinclude} /_files/centos/console/docker/ps_ubuntu.txt
:language: console
:::

Attach to it:

```sh
docker attach adoring_driscoll
```

:::{tip}
The container will stop if you exit the shell, and can be started and attached by

```sh
docker start -ai adoring_driscoll
```

:::

### Run as a daemon

Run the image with a specific command in background:

```console
$ docker run -d ubuntu:22.04 /bin/sh -c "while true; do date; sleep 5; done"
09ced91733fec07bdc67587dce2f44aec74d05a595427ed9dfa6c40c020d66c7
```

See the running containers:

:::{literalinclude} /_files/centos/console/docker/ps_ubuntu_d.txt
:language: console
:::

Watch the output of the container:

:::{literalinclude} /_files/centos/console/docker/logs_ubuntu_d.txt
:language: console
:::

Or watch it continously:

```sh
docker logs -f flamboyant_payne
```

Stop the container:

```console
$ docker stop flamboyant_payne
flamboyant_payne
```

Start the container:

```console
$ docker start flamboyant_payne
flamboyant_payne
```

Pause the container:

```console
$ docker pause flamboyant_payne
flamboyant_payne
```

Unpause the container:

```console
$ docker unpause flamboyant_payne
flamboyant_payne
```

### Overriden entrypoint

Run an image with overriden entrypoint:

```sh
docker run -it --entrypoint /bin/bash xxxx-image
```

### Build images

If there are a `Dockerfile` in the current directory, build the image:

```sh
docker build -t xxxx-image .
docker tag xxxx-image xxxx-image:1.0.0
```

### Clean up

Remove all stopped containers:

```sh
docker container prune
```

Remove all dangling images:

```sh
docker image prune
```

### Use local registry

Start the registry service (v2):

:::{literalinclude} /_files/centos/console/docker/run_registry.txt
:language: console
:::

See the running registry container:

:::{literalinclude} /_files/centos/console/docker/ps_registry.txt
:language: console
:::

Re tag an image and push it to the local registry:

:::{literalinclude} /_files/centos/console/docker/push_busybox.txt
:language: console
:::

See there is something in the local registry:

:::{literalinclude} /_files/centos/console/ls/docker_images.txt
:language: console
:::

Our new registry is not secure, so we need to add it to docker daemon's config:

```sh
sudo vi /etc/docker/daemon.json
```

{.file-content}

```json
{
  "insecure-registries": [
    "las0:5000"
  ]
}
```

Remove the local copy of the image:

```sh
docker rmi las0:5000/busybox
```

Now we can pull the image from the local registry:

```sh
docker pull las0:5000/busybox
```

### Save images to file

```sh
docker image save busybox -o busybox.tar
```
