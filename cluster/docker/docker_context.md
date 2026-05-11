# Use Docker Context

Create a context using SSH to connect to the remote server with Docker Engine installed (make it password-less first):

```console
$ docker context create las0 --docker host=ssh://ubuntu@las0
las0
Successfully created context "las0"
```

Switch to the new context:

```console
$ docker context use las0
las0
Current context is now "las0"
```

Show all the docker contexts:

```console
$ docker context ls
NAME      DESCRIPTION                               DOCKER ENDPOINT               ERROR
default   Current DOCKER_HOST based configuration   unix:///var/run/docker.sock   
las0 *                                              ssh://ubuntu@las0
```

You will notice that the defaut context is totally useless for the endpoint doesn't exist at all. But it is a reserved context that cannot be deleted or updated.

:::{note}
当你把 Docker context 切到远端主机后，执行 docker build 时：

- 你的本地客户端会先收集本地构建上下文，把这个上下文传给远端 Docker Engine 或 BuildKit, 远端再根据 Dockerfile 执行构建
- Dockerfile 里的 COPY 是从这份已上传的构建上下文里取文件，不是从远端主机读文件
- 被 .dockerignore 排除的文件不会上传，所以 COPY 不到
- 构建产生的映像在远端，执行 `docker images` 列出的也是远端的映像
- `docker save` 保存映像产生的文件在本地
- `docker run` 挂载的文件在远端
:::

See the versions:

```console
$ docker version
Client: Docker Engine - Community
 Version:           29.4.3
 API version:       1.54
 Go version:        go1.26.2
 Git commit:        055a478ea9
 Built:             Mon Apr 20 14:57:44 2026
 OS/Arch:           darwin/arm64
 Context:           las0

Server: Docker Engine - Community
 Engine:
  Version:          29.4.1
  API version:      1.54 (minimum version 1.40)
  Go version:       go1.26.2
  Git commit:       6c91b92
  Built:            Mon Apr 20 16:32:36 2026
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          v2.2.1
  GitCommit:        dea7da592f5d1d2b7755e3a161be07f43fad8f75
 runc:
  Version:          1.3.4
  GitCommit:        v1.3.4-0-gd6d73eb8
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
```
