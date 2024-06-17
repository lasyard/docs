# scutil

`scutil` is a command-line tool that allows you to configure system services and network settings on macOS.

## Usage

### Hostname

Get hostname:

```sh
scutil --get HostName
scutil --get LocalHostName
scutil --get ComputerName
```

Set hostname:

```sh
scutil --set HostName my-mac
scutil --set LocalHostName my-mac
scutil --set ComputerName my-mac
```
