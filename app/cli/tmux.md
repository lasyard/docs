# tmux

<https://github.com/tmux/tmux/wiki>

## Install

:::{plat} centos
:vers: CentOS 8.5

```sh
sudo dnf install tmux
```

Check the version:

```console
$ tmux -V
tmux 2.7
```

:::

## Usage

Create a new session:

```sh
tmux new -s xxxx-session
```

Attach to a session:

```sh
tmux attach -t xxxx-session
```

Press {kbd}`Ctrl+B`, {kbd}`d` to detach from the session.

Press {kbd}`Ctrl+B`, {kbd}`?` to show help information.

Press {kbd}`Ctrl+B`, {kbd}`c` to create a new window.

Press {kbd}`Ctrl+B`, {kbd}`n` to switch to the next window.
