# journalctl

Monitor system logs:

```console
$ journalctl -f
```

Just like `tail -f`.

If you have admin previlege, you can see the kernel messages.

Monitor only kernel messages:

```console
$ sudo journalctl -k -f
```

Show full messages of a service(unit):

```console
$ journalctl -eu slurmd
```

`-e` makes the pager scroll to the end.

Show long lines (long lines are truncated by pager):

```console
$ journalctl -u slurmd -o cat --no-pager
```
