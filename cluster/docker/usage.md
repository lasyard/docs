# Use Docker

## Run interactively

It seems there is no command to list all tags of an image, go to <https://hub.docker.com/> to search for images.

Pull the image with specified tag:

```console
$ docker pull busybox:1.37.0-glibc
1.37.0-glibc: Pulling from library/busybox
97e70d161e81: Pull complete 
Digest: sha256:45fb3214fa75ede765da7fa85a18a96d0973c26d84dac49b1af23923e627a219
Status: Downloaded newer image for busybox:1.37.0-glibc
docker.io/library/busybox:1.37.0-glibc
```

Run it interactively:

```console
$ docker run -it busybox:1.37.0-glibc
```

:::{note}
If the tag `1.37.0-glibc` is omitted, the default `latest` is used.
:::

In shell of the container, press {kbd}`Ctrl+P`, {kbd}`Ctrl+Q` to detach.

List the running containers:

```console
$ docker ps
CONTAINER ID   IMAGE                  COMMAND   CREATED         STATUS         PORTS     NAMES
960f96e93349   busybox:1.37.0-glibc   "sh"      9 seconds ago   Up 9 seconds             zealous_kapitsa
```

Attach to it:

```console
$ docker attach zealous_kapitsa
```

The id of the container can also be used to specify the container.

:::{tip}
The container will stop if you exit the shell, and can be started and attached by:

```console
$ docker start -ai zealous_kapitsa
```

:::

## Run as daemons

Run the image with a specific command in background:

```console
$ docker run -d busybox:1.37.0-glibc /bin/sh -c "while true; do date; sleep 5; done"
8c2157b50bd7cc1e062f95421c61e3eaec411af5a166bead4355b90040fa0e0b
```

See the running containers:

```console
$ docker ps
CONTAINER ID   IMAGE                  COMMAND                  CREATED          STATUS          PORTS     NAMES
8c2157b50bd7   busybox:1.37.0-glibc   "/bin/sh -c 'while t…"   33 seconds ago   Up 33 seconds             hungry_elgamal
```

Watch the output of the container:

```console
$ docker logs -f hungry_elgamal
Wed Apr 23 06:18:45 UTC 2025
Wed Apr 23 06:18:50 UTC 2025
Wed Apr 23 06:18:55 UTC 2025
Wed Apr 23 06:19:00 UTC 2025
Wed Apr 23 06:19:05 UTC 2025
...
```

Stop and start the container:

```console
$ docker stop hungry_elgamal
hungry_elgamal
$ docker start hungry_elgamal
hungry_elgamal
```

The running process of the container doesn't response to SIGINT, so it may takes a while to stop it.

Pause and unpause the container:

```console
$ docker pause hungry_elgamal
hungry_elgamal
$ docker unpause hungry_elgamal
hungry_elgamal
```

## Override entrypoint

Run an image with overriden entrypoint:

```console
$ docker run -it --entrypoint /bin/sh xxxx-image
```

## Build images

If there are a `Dockerfile` in the current directory, build the image:

```console
$ docker build -t xxxx-image .
$ docker tag xxxx-image xxxx-image:1.0.0
```

## Clean up

Remove all stopped containers:

```console
$ docker container prune -f
Deleted Containers:
8c2157b50bd7cc1e062f95421c61e3eaec411af5a166bead4355b90040fa0e0b

Total reclaimed space: 0B
```

Remove all dangling images:

```console
$ docker image prune -f
Deleted Images:
deleted: sha256:fb6b8c2a8ea14b2ba1674eaa716b4eecaa0c0b6eac70be6b077a06959a46bd4b

Total reclaimed space: 0B
```

## Use a local registry

Start the registry service (v2):

```console
$ docker run -d -p 5000:5000 --restart=always --name registry -v /opt/docker_images:/var/lib/registry registry:2
Unable to find image 'registry:2' locally
2: Pulling from library/registry
44cf07d57ee4: Pull complete 
bbbdd6c6894b: Pull complete 
8e82f80af0de: Pull complete 
3493bf46cdec: Pull complete 
6d464ea18732: Pull complete 
Digest: sha256:a3d8aaa63ed8681a604f1dea0aa03f100d5895b6a58ace528858a7b332415373
Status: Downloaded newer image for registry:2
f0819ec56c5862f00027d08313d7ac954381c81589b2425de63baee9783c0609
```

The dir `/opt/docker_images` is bound to the container to store the images in the registry.

See the running registry container:

```console
$ docker ps
CONTAINER ID   IMAGE        COMMAND                  CREATED              STATUS              PORTS                                         NAMES
f0819ec56c58   registry:2   "/entrypoint.sh /etc…"   About a minute ago   Up About a minute   0.0.0.0:5000->5000/tcp, [::]:5000->5000/tcp   registry
```

Re tag an image and push it to the local registry:

```console
$ docker tag busybox:1.37.0-glibc las3:5000/busybox:1.37.0-glibc
ubuntu@las3:~/workspace$ docker push las3:5000/busybox:1.37.0-glibc
The push refers to repository [las3:5000/busybox]
Get "https://las3:5000/v2/": http: server gave HTTP response to HTTPS client
```

Alas! It seems docker try to access the registry via https, but the registry only support http.

Edit file `/etc/docker/daemon.json` to set our registry as in-secure:

```json
{
    "insecure-registries": [
        "las3:5000"
    ]
}
```

::::{tip}
If you want to use the registry in `containerd`, create a file `las3:5000/hosts.toml` in dir `/etc/containerd/certs.d/`:

:::{literalinclude} /_files/ubuntu/etc/containerd/certs.d/las3:5000/hosts.toml
:language: toml
:::

See "<project:/cluster/k8s/deploy.md#configure-containerd>".

::::

Restart `docker` service to make the config effective:

```console
$ sudo systemctl restart docker
```

Now do the pushing again:

```console
$ docker push las3:5000/busybox:1.37.0-glibc
The push refers to repository [las3:5000/busybox]
068f50152bbc: Pushed 
1.37.0-glibc: digest: sha256:f2e98ad37e4970f48e85946972ac4acb5574c39f27c624efbd9b17a3a402bfe4 size: 527
```

We can see the uploaded images in the bound dir:

```console
$ ls /opt/docker_images/docker/registry/v2/repositories/
busybox
```

:::{tip}
For more advanced functions, use [Harbor](project:/cluster/harbor.md) instead of this. Before installing Harbor, be sure to remove the container of this for name confliction.
:::

### Save images to file

```console
$ docker image save busybox:1.37.0-glibc -o busybox-1.37.0-glibc.tar
```
