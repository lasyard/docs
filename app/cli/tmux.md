# tmux

<https://github.com/tmux/tmux/wiki>

tmux is a terminal multiplexer. It lets you switch easily between several programs in one terminal, detach them (they keep running in the background) and reattach them to a different terminal.

:::{include} /_frags/plats/centos.txt
:::

## Install

```sh
dnf install tmux
```

Show version:

```sh
tmux -V
```

{.cli-output}

```text
tmux 2.7
```

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
