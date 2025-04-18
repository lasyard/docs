# Miscellaneous

## Property list utility

Read property list files:

```console
$ plutil -p *.plist
```

## xcode-select

Print the path of the active developer directory:

```console
$ xcode-select -p
```

Open a dialog for installation of the command line developer tools:

```console
$ xcode-select --install
```

## Create disk image

```console
$ hdiutil makehybrid -o "dir.udf" -udf "dir/"
```

## Manage Spotlight indexes

Print indexing status:

```console
$ sudo mdutil -s "/Volumes/LAS_256G"
```

Turn off indexing:

```console
$ sudo mdutil -i off -d "/Volumes/LAS_256G"
$ sudo mdutil -X "/Volumes/LAS_256G"
```

## See cloud docs

```console
$ cd ~/Library/Mobile\ Documents/com\~apple\~CloudDocs/
```

## chflags

See flags of files:

```console
$ ls -lO
```

Remove hidden (hide from GUI) flag:

```console
$ chflags nohidden xxxx-file
```

Add hidden flag:

```console
$ chflags hidden .msdb
```
