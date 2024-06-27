# docker

<https://www.docker.com/>

{{ for_centos }}

## Install

Add `docker` repository:

```sh
dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
```

Install:

```sh
dnf install docker-ce
```

```sh
systemctl enable docker --now
```

Check version:

```sh
docker version
```

:::{literalinclude} /_files/centos/output/docker/version.txt
:language: text
:class: cli-output
:::

More detailed information:

```sh
docker info
```

## Usage

### Hello world

Pull the image:

```sh
docker pull hello-world
```

:::{literalinclude} /_files/centos/output/docker/pull_hello_world.txt
:language: text
:class: cli-output
:::

List images:

```sh
docker images
```

:::{literalinclude} /_files/centos/output/docker/images_hello_world.txt
:language: text
:class: cli-output
:::

Inspect the image:

```sh
docker inspect hello-world
```

:::{literalinclude} /_files/centos/output/docker/inspect_hello_world.txt
:language: json
:class: cli-output
:::

Run the image as a container:

```sh
docker run hello-world
```

List all (including stopped) containers:

```sh
docker ps -a
```

:::{literalinclude} /_files/centos/output/docker/ps_a_hello_world.txt
:language: text
:class: cli-output
:::

### Run interactively

Find the image:

```sh
docker search ubuntu
```

It seems there is no command to list all tags of an image, go to <https://hub.docker.com/> for information.

Pull the image with specified tag:

```sh
docker pull ubuntu:22.04
```

:::{literalinclude} /_files/centos/output/docker/pull_ubuntu.txt
:language: text
:class: cli-output
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

:::{literalinclude} /_files/centos/output/docker/ps_ubuntu_it.txt
:language: text
:class: cli-output
:::

Attach to it:

```sh
docker attach laughing_hellman
```

:::{tip}
The container will stop if you exit the shell, and can be started and attached by

```sh
docker start -ai laughing_hellman
```

:::

### Run as a daemon

Run the image with a specific command in background:

```sh
docker run -d ubuntu:22.04 /bin/sh -c "while true; do date; sleep 5; done"
```

See the running containers:

```sh
docker ps
```

:::{literalinclude} /_files/centos/output/docker/ps_ubuntu_d.txt
:language: text
:class: cli-output
:::

Watch the output of the container:

```sh
docker logs zealous_leavitt
docker logs -f zealous_leavitt
```

Stop/start the container:

```sh
docker stop zealous_leavitt
docker start zealous_leavitt
```

Pause/unpause the container:

```sh
docker pause zealous_leavitt
docker unpause zealous_leavitt
```

### Run an image with overriden entrypoint

```sh
docker run -it --entrypoint /bin/bash slurm-ubuntu-client
```

### Build images

If there are a `Dockerfile` in the current directory, build the image:

```sh
docker build -t slurm-ubuntu-client:22.04_23.11.7 .
docker tag slurm-ubuntu-client:22.04_23.11.7 slurm-ubuntu-client
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

Create a directory for the local registry:

```sh
mkdir /opt/docker_images
```

Start the registry service (v2):

```sh
docker run -d -p 5000:5000 --restart=always --name registry -v /opt/docker_images:/var/lib/registry registry:2
```

See the running registry container:

```sh
docker ps
```

{.cli-output}

```text
CONTAINER ID   IMAGE        COMMAND                   CREATED       STATUS         PORTS                                       NAMES
bd4ed095dc7f   registry:2   "/entrypoint.sh /etc…"   4 hours ago   Up 3 minutes   0.0.0.0:5000->5000/tcp, :::5000->5000/tcp   registry
```

Re tag an image and push it to the local registry:

```sh
docker tag slurm-ubuntu-client:latest las1:5000/slurm-ubuntu-client
docker push las1:5000/slurm-ubuntu-client
```

See there is something in the local registry:

```sh
ls /opt/docker_images/docker/registry/v2/
```

{.cli-output}

```text
blobs  repositories
```

Our new registry is not secure, so we need to add it to docker daemon's config:

```sh
vi /etc/docker/daemon.json
```

{.file-content}

```json
{
  "insecure-registries": [
    "las1:5000"
  ]
}
```

Remove the local copy of the image:

```sh
docker rmi las1:5000/slurm-ubuntu-client
```

Now we can pull the image from the local registry:

```sh
docker pull las1:5000/slurm-ubuntu-client
```
