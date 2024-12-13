# ffmpeg

<https://ffmpeg.org/>

## Install

::::{plat} macos

```sh
brew install ffmpeg
```

Check the version:

:::{literalinclude} /_files/macos/console/ffmpeg/version.txt
:language: console
:::

::::

## Usage

### Trim

```sh
ffmpeg -i input.mp4 -ss 00:02:22 -to 00:03:33 -c copy out.mp4
```

### Scale

```sh
ffmpeg -i input.mp4 -vf scale=1920:1080 out.mp4
```

### Rotate

```sh
ffmpeg -i input.mp4 -c copy -metadata:s:v:0 rotate=90 out.mp4
```

### Change FPS

```sh
ffmpeg -i input.mp4 -vf fps=25 out.mp4
```

### Check

```sh
ffmpeg -v error -i input.mp4 -f null
```

### mkv to mp4

```sh
ffmpeg -i input.mkv -c:a copy -c:v copy -f mp4 out.mp4
```

:::{note}
`mp4` cannot contain `ass` subtitles.
:::

### Extract subtitle

```sh
ffmpeg -i input.mkv -map 0:s:1 -c:s copy -f ass out.ass
```

### Concat files

```sh
vi confiles.txt
```

{.file-content}

```text
file 'a.mp3'
file 'b.mp3'
```

```sh
ffmpeg -f concat -safe 0 -i confiles.txt -c copy out.mp3
```
