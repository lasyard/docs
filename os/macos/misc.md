# Miscellaneous

## Property list utility

Read property list files:

```sh
plutil -p *.plist
```

## xcode-select

Print the path of the active developer directory:

```sh
xcode-select -p
```

Open a dialog for installation of the command line developer tools:

```sh
xcode-select --install
```

## Create disk image

```sh
hdiutil makehybrid -o "dir.udf" -udf "dir/"
```

## Manage Spotlight indexes

Print indexing status:

```sh
sudo mdutil -s "/Volumes/LAS_256G"
```

Turn off indexing:

```sh
sudo mdutil -i off -d "/Volumes/LAS_256G"
sudo mdutil -X "/Volumes/LAS_256G"
```

## See cloud docs

```sh
cd ~/Library/Mobile\ Documents/com\~apple\~CloudDocs/
```

## chflags

See flags of files:

```sh
ls -lO
```

Remove hidden (hide from GUI) flag:

```sh
chflags nohidden xxxx-file
```
