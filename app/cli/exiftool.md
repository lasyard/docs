# exiftool

<https://exiftool.org/>

## Usage

### Show version

:::{plat} macos
:vers: macOS Monterey

```console
$ exiftool -ver
12.85
```

:::

### Rename files

Rename `jpg` files according to its taken time:

```sh
exiftool -fast2 -ext jpg -if '${DateTimeOriginal}' "-Filename<IMG_\${DateTimeOriginal#;DateFmt('%Y%m%d_%H%M%S')}%+3c.jpg" *
```

### Modify time

Set time to the file modification time if no time is set in EXIF:

```sh
exiftool -ext jpg -if 'not ${DateTimeOriginal}' '-AllDates<FileModifyDate' −overwrite_original *
```

Set time to a specified time:

```sh
exiftool -ext jpg '-AllDates=2025:01:01 00:00:00' −overwrite_original *
exiftool -ext jpg "-AllDates=$(date -j -f "%s" "+%Y:%m:%d %H:%M:%S" 1735660800)" −overwrite_original *
```

Set time to one day before the original time:

```sh
exiftool -ext jpg -if '${DateTimeOriginal}' -DateTimeOriginal-='1 00:00:00' −overwrite_original *
```

### Modify Camera Model

Set camera model to `UNKNOWN` if it is not set in EXIF:

```sh
exiftool -ext jpg -if 'not ${Model}' '-Model=UNKNOWN' -overwrite_original *
```

Some cameras write `Software` instead of `Model`, so set camera model accordingly:

```sh
exiftool -ext jpg -if 'not ${Model}' -if '${Software}' '-Model<${Software;$_=substr($_, 0, 8)}' -overwrite_original *
```

### Copy tags

For example, copy `Model`:

```sh
exiftool -TagsFromFile source.jpg -Model -overwrite_original target.jpg
```

### Remove thumbnail image

```sh
exiftool -ext jpg -if '${ThumbnailImage}' -ThumbnailImage= -overwrite_original -R .
```
